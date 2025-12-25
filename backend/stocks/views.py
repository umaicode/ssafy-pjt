import yfinance as yf
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from openai import OpenAI
from html import unescape
from django.utils.html import strip_tags
from .serializers import (
    StockDetailSerializer,
    StockChartResponseSerializer,
    StockNewsSerializer,
    PopularStockSerializer,
)


# 인기 종목 (하드코딩)
POPULAR_STOCKS = {
    'KR': [
        {'symbol': '005930.KS', 'name': '삼성전자'},
        {'symbol': '000660.KS', 'name': 'SK하이닉스'},
        {'symbol': '373220.KS', 'name': 'LG에너지솔루션'},
        {'symbol': '207940.KS', 'name': '삼성바이오로직스'},
        {'symbol': '005380.KS', 'name': '현대차'},
        {'symbol': '000270.KS', 'name': '기아'},
        {'symbol': '068270.KS', 'name': '셀트리온'},
        {'symbol': '035420.KS', 'name': 'NAVER'},
        {'symbol': '035720.KS', 'name': '카카오'},
        {'symbol': '051910.KS', 'name': 'LG화학'},
        {'symbol': '006400.KS', 'name': '삼성SDI'},
        {'symbol': '003670.KS', 'name': '포스코퓨처엠'},
        {'symbol': '105560.KS', 'name': 'KB금융'},
        {'symbol': '055550.KS', 'name': '신한지주'},
        {'symbol': '086790.KS', 'name': '하나금융지주'},
        {'symbol': '012330.KS', 'name': '현대모비스'},
        {'symbol': '066570.KS', 'name': 'LG전자'},
        {'symbol': '028260.KS', 'name': '삼성물산'},
        {'symbol': '003550.KS', 'name': 'LG'},
        {'symbol': '034730.KS', 'name': 'SK'},
    ],
    'US': [
        {'symbol': 'AAPL', 'name': 'Apple'},
        {'symbol': 'MSFT', 'name': 'Microsoft'},
        {'symbol': 'GOOGL', 'name': 'Alphabet'},
        {'symbol': 'AMZN', 'name': 'Amazon'},
        {'symbol': 'NVDA', 'name': 'NVIDIA'},
        {'symbol': 'META', 'name': 'Meta'},
        {'symbol': 'TSLA', 'name': 'Tesla'},
        {'symbol': 'BRK-B', 'name': 'Berkshire Hathaway'},
        {'symbol': 'JPM', 'name': 'JPMorgan Chase'},
        {'symbol': 'V', 'name': 'Visa'},
        {'symbol': 'UNH', 'name': 'UnitedHealth'},
        {'symbol': 'JNJ', 'name': 'Johnson & Johnson'},
        {'symbol': 'WMT', 'name': 'Walmart'},
        {'symbol': 'MA', 'name': 'Mastercard'},
        {'symbol': 'PG', 'name': 'Procter & Gamble'},
        {'symbol': 'HD', 'name': 'Home Depot'},
        {'symbol': 'XOM', 'name': 'Exxon Mobil'},
        {'symbol': 'BAC', 'name': 'Bank of America'},
        {'symbol': 'COST', 'name': 'Costco'},
        {'symbol': 'KO', 'name': 'Coca-Cola'},
    ],
}


# OpenAI 클라이언트
def get_openai_client():
    return OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=getattr(settings, "OPENAI_BASE_URL", None),
    )


@api_view(["GET"])
def search_stocks(request):
    query = request.GET.get("query", "").strip()
    if not query:
        return Response({"error": "검색어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    results = []

    # (1) TODO: DB 종목 마스터에서 먼저 검색 (한글명/영문명/티커/별칭)
    # results.extend(db_results)

    # (2) Yahoo Finance 검색 (자동완성)
    try:
        s = yf.Search(query, max_results=10)
        for q in s.quotes:
            # q 예: {'symbol': 'NVDA', 'shortname': 'NVIDIA Corporation', 'exchange': 'NMS', ...}
            symbol = q.get("symbol")
            name = q.get("longname") or q.get("shortname") or symbol
            if symbol:
                results.append({
                    "symbol": symbol,
                    "name": name,
                    "exchange": q.get("exchange"),
                    "type": q.get("quoteType"),
                })
    except Exception:
        pass

    # (3) 6자리 숫자면 한국 심볼 보정
    if not results and query.isdigit() and len(query) == 6:
        for suffix in [".KS", ".KQ"]:
            sym = f"{query}{suffix}"
            try:
                info = yf.Ticker(sym).info
                if info and info.get("regularMarketPrice") is not None:
                    results.append({
                        "symbol": sym,
                        "name": info.get("longName") or info.get("shortName") or sym,
                        "exchange": info.get("exchange", "KRX"),
                        "type": info.get("quoteType", "EQUITY"),
                    })
                    break
            except Exception:
                continue

    return Response({"results": results[:10]})


@api_view(['GET'])
def get_market_indices(request):
    """
    주요 시장 지표 조회 (나스닥, S&P500, 다우존스, 환율 등)
    """
    period = request.GET.get('period', '5d')
    
    INDICES = {
        'NASDAQ': '^IXIC',
        'S&P500': '^GSPC',
        'DOW': '^DJI',
        'KOSPI': '^KS11',
        'USD/KRW': 'USDKRW=X',
        'EUR/KRW': 'EURKRW=X',
        'JPY/KRW': 'JPYKRW=X',
    }
    
    results = []
    
    for name, symbol in INDICES.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current_price = info.get('regularMarketPrice') or info.get('previousClose')
            previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
            
            change = None
            change_percent = None
            if current_price and previous_close:
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
            
            # 차트 데이터
            hist = ticker.history(period=period)
            chart_data = []
            if not hist.empty:
                for date, row in hist.iterrows():
                    chart_data.append({
                        'date': date.isoformat(),
                        'close': round(row['Close'], 2) if row['Close'] else None,
                    })
            
            results.append({
                'name': name,
                'symbol': symbol,
                'current_price': round(current_price, 2) if current_price else None,
                'change': round(change, 2) if change else None,
                'change_percent': round(change_percent, 2) if change_percent else None,
                'chart_data': chart_data[-30:],
            })
        except Exception as e:
            results.append({
                'name': name,
                'symbol': symbol,
                'current_price': None,
                'change': None,
                'change_percent': None,
                'chart_data': [],
            })
    
    return Response({'indices': results})


@api_view(['GET'])
def get_popular_stocks(request):
    """
    인기 종목 목록 조회 (yfinance 실시간 가격)
    market: 'KR' (한국) 또는 'US' (미국), 기본값은 둘 다
    """
    market = request.GET.get('market', '').upper()
    
    results = []
    markets_to_fetch = ['KR', 'US'] if not market else [market]
    
    for mkt in markets_to_fetch:
        stocks = POPULAR_STOCKS.get(mkt, [])
        
        for stock in stocks:
            try:
                ticker = yf.Ticker(stock['symbol'])
                info = ticker.info
                
                current_price = info.get('regularMarketPrice') or info.get('currentPrice')
                previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
                
                change = None
                change_percent = None
                
                if current_price and previous_close:
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100
                
                results.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'current_price': current_price,
                    'change': round(change, 2) if change else None,
                    'change_percent': round(change_percent, 2) if change_percent else None,
                    'market': mkt,
                })
            except Exception:
                results.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'current_price': None,
                    'change': None,
                    'change_percent': None,
                    'market': mkt,
                })
    
    serializer = PopularStockSerializer(results, many=True)
    return Response({'stocks': serializer.data})


@api_view(['GET'])
def get_stock_detail(request, symbol):
    """
    주식 종목 상세 정보 조회
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if not info or info.get('regularMarketPrice') is None:
            return Response(
                {'error': '종목을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        current_price = info.get('regularMarketPrice') or info.get('currentPrice')
        previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
        
        change = None
        change_percent = None
        
        if current_price and previous_close:
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
        
        data = {
            'symbol': info.get('symbol', symbol),
            'name': info.get('longName') or info.get('shortName', symbol),
            'currency': info.get('currency'),
            'exchange': info.get('exchange'),
            'market_cap': info.get('marketCap'),
            'current_price': current_price,
            'previous_close': previous_close,
            'open_price': info.get('open') or info.get('regularMarketOpen'),
            'day_high': info.get('dayHigh') or info.get('regularMarketDayHigh'),
            'day_low': info.get('dayLow') or info.get('regularMarketDayLow'),
            'volume': info.get('volume') or info.get('regularMarketVolume'),
            'avg_volume': info.get('averageVolume'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
            'pe_ratio': info.get('trailingPE'),
            'eps': info.get('trailingEps'),
            'dividend_yield': info.get('dividendYield'),
            'beta': info.get('beta'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'description': info.get('longBusinessSummary'),
            'website': info.get('website'),
            'logo_url': info.get('logo_url'),
            'change': round(change, 2) if change else None,
            'change_percent': round(change_percent, 2) if change_percent else None,
        }
        
        serializer = StockDetailSerializer(data)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': f'데이터를 가져오는 중 오류가 발생했습니다: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_stock_chart(request, symbol):
    """
    주식 차트 데이터 조회
    """
    period = request.GET.get('period', '1mo')
    interval = request.GET.get('interval', '1d')
    
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    
    if period not in valid_periods:
        return Response(
            {'error': f'유효하지 않은 기간입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if interval not in valid_intervals:
        return Response(
            {'error': f'유효하지 않은 간격입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        
        if hist.empty:
            return Response(
                {'error': '차트 데이터를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        chart_data = []
        for date, row in hist.iterrows():
            chart_data.append({
                'date': date.isoformat(),
                'open': round(row['Open'], 2) if row['Open'] else None,
                'high': round(row['High'], 2) if row['High'] else None,
                'low': round(row['Low'], 2) if row['Low'] else None,
                'close': round(row['Close'], 2) if row['Close'] else None,
                'volume': int(row['Volume']) if row['Volume'] else 0,
            })
        
        return Response({
            'symbol': symbol,
            'period': period,
            'interval': interval,
            'data': chart_data,
        })
        
    except Exception as e:
        return Response(
            {'error': f'차트 데이터를 가져오는 중 오류가 발생했습니다: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_stock_news(request, symbol):
    """
    주식 종목 관련 뉴스 조회 - 네이버 뉴스 API 사용
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        stock_name = info.get('longName') or info.get('shortName', symbol)
        
        # 인기 종목에서 한글명 찾기
        for mkt in ['KR', 'US']:
            for stock in POPULAR_STOCKS.get(mkt, []):
                if stock['symbol'] == symbol or stock['symbol'].replace('.KS', '') == symbol.replace('.KS', ''):
                    stock_name = stock['name']
                    break
        
        # 네이버 뉴스 API 호출
        naver_client_id = getattr(settings, 'NAVER_CLIENT_ID', None)
        naver_client_secret = getattr(settings, 'NAVER_CLIENT_SECRET', None)
        
        if not naver_client_id or not naver_client_secret:
            # yfinance 뉴스 사용
            news = ticker.news
            if not news:
                return Response({'news': []})
            
            news_list = []
            for item in news[:10]:
                news_list.append({
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'publisher': item.get('publisher'),
                    'published_date': item.get('providerPublishTime'),
                    'thumbnail': item.get('thumbnail', {}).get('resolutions', [{}])[0].get('url') if item.get('thumbnail') else None,
                })
            
            serializer = StockNewsSerializer(news_list, many=True)
            return Response({'news': serializer.data})
        
        # 네이버 뉴스 검색
        url = "https://openapi.naver.com/v1/search/news.json"
        headers = {
            "X-Naver-Client-Id": naver_client_id,
            "X-Naver-Client-Secret": naver_client_secret,
        }
        params = {
            "query": f"{stock_name} 주식",
            "display": 10,
            "sort": "date",
        }
        
        res = requests.get(url, headers=headers, params=params)
        
        if res.status_code != 200:
            return Response({'news': []})
        
        data = res.json()
        items = data.get("items", [])
        
        news_list = []
        for item in items:
            title = unescape(strip_tags(item.get("title", "")))
            description = unescape(strip_tags(item.get("description", "")))
            
            news_list.append({
                'title': title,
                'link': item.get('originallink') or item.get('link'),
                'publisher': None,
                'published_date': item.get('pubDate'),
                'thumbnail': None,
                'description': description,
            })
        
        return Response({'news': news_list})
        
    except Exception as e:
        return Response(
            {'error': f'뉴스를 가져오는 중 오류가 발생했습니다: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def translate_description(request):
    """
    영문 기업 설명을 한글로 번역
    """
    text = request.data.get('text', '')
    
    if not text:
        return Response(
            {'error': '번역할 텍스트가 없습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        client = get_openai_client()
        
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {
                    "role": "system",
                    "content": """당신은 금융/비즈니스 전문 번역가입니다. 
영어로 된 기업 설명을 자연스러운 한국어로 번역해주세요.
- 전문 용어는 적절한 한국어 표현으로 번역
- 기업명은 원문 유지
- 존댓말 사용
- 간결하고 명확하게 번역"""
                },
                {
                    "role": "user",
                    "content": f"다음 기업 설명을 한국어로 번역해주세요:\n\n{text}"
                }
            ],
            max_tokens=1000,
            temperature=0.3,
        )
        
        translated = response.choices[0].message.content.strip()
        
        return Response({'translated': translated})
        
    except Exception as e:
        return Response(
            {'error': f'번역 중 오류가 발생했습니다: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
