"""
stocks/views.py
주식 관련 API 뷰

주요 기능:
- 국내/해외 주식 데이터 DB 저장 및 조회
- 데이터 갱신 API (가격, 등락율 포함)
- 북마크 주식 관리
- 주식 검색, 상세정보, 차트, 뉴스
"""

import yfinance as yf
import requests
import pandas as pd
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from openai import OpenAI
from html import unescape
from django.utils.html import strip_tags
from pykrx import stock as pykrx_stock

from .models import Stock, StockDataUpdate, BookmarkedStock
from .serializers import StockDetailSerializer, StockNewsSerializer, PopularStockSerializer


# ============================================================
# 상수 정의
# ============================================================
PAGE_SIZE = 20


# ============================================================
# 헬퍼 함수
# ============================================================
def get_openai_client():
    """OpenAI API 클라이언트 생성"""
    return OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=getattr(settings, "OPENAI_BASE_URL", None),
    )


def calculate_change_percent(current: float, previous: float) -> float:
    """등락률 계산"""
    if current and previous and previous != 0:
        return round(((current - previous) / previous) * 100, 2)
    return 0.0


# ============================================================
# 주요 시장 지표 API
# ============================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_market_indices(request):
    """
    주요 시장 지표 조회 (나스닥, S&P500, 환율 등)
    실시간 데이터를 yfinance에서 가져옴
    """
    period = request.GET.get('period', '5d')
    
    indices = {
        '^IXIC': {'name': '나스닥', 'symbol': 'NASDAQ'},
        '^GSPC': {'name': 'S&P 500', 'symbol': 'S&P500'},
        '^DJI': {'name': '다우존스', 'symbol': 'DOW'},
        '^KS11': {'name': '코스피', 'symbol': 'KOSPI'},
        '^KQ11': {'name': '코스닥', 'symbol': 'KOSDAQ'},
        'KRW=X': {'name': '원/달러', 'symbol': 'USD/KRW'},
        'GC=F': {'name': '금', 'symbol': 'GOLD'},
        'BTC-USD': {'name': '비트코인', 'symbol': 'BTC'},
    }
    
    result = []
    for ticker_symbol, info in indices.items():
        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period)
            
            if len(hist) >= 1:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[0] if len(hist) >= 2 else current
                change = current - previous
                change_percent = (change / previous * 100) if previous else 0
                
                # 미니 차트용 데이터 (최근 데이터 포인트들)
                chart_data = [round(float(price), 2) for price in hist['Close'].tolist()[-20:]]
                
                result.append({
                    'symbol': info['symbol'],
                    'name': info['name'],
                    'current_price': round(current, 2),
                    'value': round(current, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'chart_data': chart_data,
                })
        except Exception as e:
            print(f"Error fetching {ticker_symbol}: {e}")
            continue
    
    return Response({'indices': result})


# ============================================================
# 데이터 갱신 함수 (국내/해외)
# ============================================================
def refresh_kr_stocks():
    """국내 주식 데이터 갱신 (pykrx)"""
    try:
        update_record, _ = StockDataUpdate.objects.get_or_create(market='KR')
        update_record.status = 'in_progress'
        update_record.save()

        # 최근 유효 거래일 찾기
        today = datetime.today()
        date_str, df_cap = None, None

        for i in range(14):
            check_date = (today - timedelta(days=i)).strftime("%Y%m%d")
            try:
                df = pykrx_stock.get_market_cap_by_ticker(check_date, market="ALL")
                if df is not None and not df.empty:
                    df_valid = df[(df['시가총액'] > 0) & (df['종가'] > 0)]
                    if len(df_valid) > 100:
                        date_str, df_cap = check_date, df_valid
                        break
            except Exception:
                continue

        if df_cap is None or df_cap.empty:
            update_record.status = 'failed'
            update_record.save()
            return False, '유효한 거래일을 찾을 수 없습니다.', 0

        # OHLCV 데이터 (등락률)
        try:
            df_ohlcv = pykrx_stock.get_market_ohlcv_by_ticker(date_str, market="ALL")
        except Exception:
            df_ohlcv = None

        # 시가총액순 정렬 및 상위 500개
        df_cap = df_cap.sort_values('시가총액', ascending=False).head(500)

        # 종목명 조회
        ticker_names = {}
        for ticker in df_cap.index:
            try:
                name = pykrx_stock.get_market_ticker_name(ticker)
                if name:
                    ticker_names[ticker] = name
            except Exception:
                continue

        # DB 저장
        count = 0
        for ticker in df_cap.index:
            name = ticker_names.get(ticker)
            if not name:
                continue

            change_percent = 0.0
            if df_ohlcv is not None and ticker in df_ohlcv.index:
                try:
                    change_percent = float(df_ohlcv.loc[ticker, '등락률'])
                except Exception:
                    pass

            Stock.objects.update_or_create(
                symbol=f"{ticker}.KS",
                defaults={
                    'code': ticker,
                    'name': name,
                    'market': 'KR',
                    'current_price': int(df_cap.loc[ticker, '종가']),
                    'change_percent': round(change_percent, 2),
                    'market_cap': int(df_cap.loc[ticker, '시가총액']),
                }
            )
            count += 1

        # 갱신 완료
        update_record.last_updated = timezone.now()
        update_record.stock_count = count
        update_record.status = 'success'
        update_record.save()

        return True, f'국내 주식 {count}개 갱신 완료', count

    except Exception as e:
        StockDataUpdate.objects.filter(market='KR').update(status='failed')
        return False, f'갱신 오류: {str(e)}', 0


def refresh_us_stocks():
    """
    해외 주식 데이터 갱신 (Wikipedia S&P 500 + yfinance)
    모든 종목의 가격, 등락율을 업데이트
    """
    try:
        update_record, _ = StockDataUpdate.objects.get_or_create(market='US')
        update_record.status = 'in_progress'
        update_record.save()

        # Wikipedia에서 S&P 500 종목 목록 가져오기
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tables = pd.read_html(response.text)
        sp500_df = tables[0]

        # 종목 정보 수집
        tickers_info = []
        for _, row in sp500_df.iterrows():
            symbol = row['Symbol'].replace('.', '-')  # BRK.B -> BRK-B
            name = row['Security']
            sector = row.get('GICS Sector', '')
            tickers_info.append((symbol, name, sector))

        # 1단계: 전체 종목 기본 정보 저장
        for symbol, name, sector in tickers_info:
            Stock.objects.update_or_create(
                symbol=symbol,
                defaults={
                    'code': symbol,
                    'name': name,
                    'market': 'US',
                    'sector': sector,
                }
            )

        # 2단계: 모든 종목 가격/등락율 업데이트 (배치 처리)
        all_symbols = [t[0] for t in tickers_info]
        batch_size = 50
        updated_count = 0

        for i in range(0, len(all_symbols), batch_size):
            batch = all_symbols[i:i + batch_size]
            batch_str = ' '.join(batch)

            try:
                tickers = yf.Tickers(batch_str)
                for symbol in batch:
                    try:
                        info = tickers.tickers[symbol].info
                        current_price = info.get('regularMarketPrice') or info.get('currentPrice')
                        previous_close = info.get('previousClose')
                        market_cap = info.get('marketCap', 0)

                        if current_price:
                            Stock.objects.filter(symbol=symbol).update(
                                current_price=round(current_price, 2),
                                change_percent=calculate_change_percent(current_price, previous_close),
                                market_cap=market_cap or 0,
                            )
                            updated_count += 1
                    except Exception:
                        continue
            except Exception:
                continue

        # 갱신 완료
        update_record.last_updated = timezone.now()
        update_record.stock_count = len(tickers_info)
        update_record.status = 'success'
        update_record.save()

        return True, f'해외 주식 {len(tickers_info)}개 갱신 완료 ({updated_count}개 가격 업데이트)', len(tickers_info)

    except Exception as e:
        StockDataUpdate.objects.filter(market='US').update(status='failed')
        return False, f'갱신 오류: {str(e)}', 0


# ============================================================
# API 엔드포인트
# ============================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_kr_stocks(request):
    """국내 주식 목록 조회 API (DB에서 조회, 페이지네이션)"""
    page = int(request.GET.get('page', 1))
    size = min(int(request.GET.get('size', request.GET.get('page_size', PAGE_SIZE))), 100)

    stocks = Stock.objects.filter(market='KR')
    total_count = stocks.count()

    if total_count == 0:
        return Response({
            'market': 'KR', 'count': 0, 'total_count': 0, 'page': page,
            'total_pages': 0, 'stocks': [],
            'message': '데이터가 없습니다. 갱신 버튼을 눌러주세요.'
        })

    offset = (page - 1) * size
    stocks_page = stocks[offset:offset + size]
    update_info = StockDataUpdate.objects.filter(market='KR').first()

    stocks_data = [
        {
            'rank': offset + i + 1, 'symbol': s.symbol, 'code': s.code,
            'name': s.name, 'current_price': s.current_price,
            'change_percent': s.change_percent, 'market_cap': s.market_cap, 'market': 'KR',
        }
        for i, s in enumerate(stocks_page)
    ]

    return Response({
        'market': 'KR', 'count': len(stocks_data), 'total_count': total_count,
        'page': page, 'total_pages': (total_count + size - 1) // size,
        'stocks': stocks_data,
        'last_updated': update_info.last_updated.isoformat() if update_info else None,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_us_stocks(request):
    """해외(미국) 주식 목록 조회 API (DB에서 조회, 페이지네이션)"""
    page = int(request.GET.get('page', 1))
    size = min(int(request.GET.get('size', request.GET.get('page_size', PAGE_SIZE))), 100)

    stocks = Stock.objects.filter(market='US')
    total_count = stocks.count()

    if total_count == 0:
        return Response({
            'market': 'US', 'count': 0, 'total_count': 0, 'page': page,
            'total_pages': 0, 'stocks': [],
            'message': '데이터가 없습니다. 갱신 버튼을 눌러주세요.'
        })

    offset = (page - 1) * size
    stocks_page = stocks[offset:offset + size]
    update_info = StockDataUpdate.objects.filter(market='US').first()

    stocks_data = [
        {
            'rank': offset + i + 1, 'symbol': s.symbol, 'code': s.code,
            'name': s.name, 'current_price': s.current_price,
            'change_percent': s.change_percent, 'market_cap': s.market_cap,
            'market': 'US', 'sector': s.sector,
        }
        for i, s in enumerate(stocks_page)
    ]

    return Response({
        'market': 'US', 'count': len(stocks_data), 'total_count': total_count,
        'page': page, 'total_pages': (total_count + size - 1) // size,
        'stocks': stocks_data,
        'last_updated': update_info.last_updated.isoformat() if update_info else None,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_stocks(request):
    """주식 데이터 갱신 API"""
    market = request.data.get('market', '').upper()

    if market not in ['KR', 'US']:
        return Response({'error': 'market은 KR 또는 US여야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    if market == 'KR':
        success, message, count = refresh_kr_stocks()
    else:
        success, message, count = refresh_us_stocks()

    if success:
        return Response({'success': True, 'message': message, 'count': count})
    else:
        return Response({'success': False, 'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_update_status(request):
    """데이터 갱신 상태 조회 API"""
    result = {}

    for market in ['KR', 'US']:
        update_info = StockDataUpdate.objects.filter(market=market).first()
        if update_info:
            result[market] = {
                'last_updated': update_info.last_updated.isoformat(),
                'stock_count': update_info.stock_count,
                'status': update_info.status,
            }
        else:
            result[market] = {'last_updated': None, 'stock_count': 0, 'status': 'never'}

    return Response(result)


@api_view(["GET"])
@permission_classes([AllowAny])
def search_stocks(request):
    """주식 종목 검색 API"""
    query = request.GET.get("query", "").strip()
    if not query:
        return Response({"error": "검색어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    results = []

    # DB에서 검색
    db_results = Stock.objects.filter(
        Q(name__icontains=query) | Q(code__icontains=query) | Q(symbol__icontains=query)
    ).order_by('-market_cap')[:10]

    for stock in db_results:
        results.append({
            "symbol": stock.symbol, "name": stock.name,
            "exchange": "KRX" if stock.market == 'KR' else "NYSE/NASDAQ",
            "type": "EQUITY", "market": stock.market,
        })

    # DB에 없으면 yfinance 검색
    if len(results) < 5:
        if query.isdigit() and len(query) == 6:
            for suffix in [".KS", ".KQ"]:
                try:
                    info = yf.Ticker(f"{query}{suffix}").info
                    if info.get("regularMarketPrice"):
                        results.append({
                            "symbol": f"{query}{suffix}",
                            "name": info.get("longName") or info.get("shortName"),
                            "exchange": info.get("exchange", "KRX"), "type": "EQUITY",
                        })
                        break
                except Exception:
                    continue

        if len(results) < 5:
            try:
                for q in yf.Search(query, max_results=10).quotes:
                    symbol = q.get("symbol")
                    if symbol and not any(r['symbol'] == symbol for r in results):
                        results.append({
                            "symbol": symbol,
                            "name": q.get("longname") or q.get("shortname") or symbol,
                            "exchange": q.get("exchange"), "type": q.get("quoteType"),
                        })
            except Exception:
                pass

    return Response({"results": results[:10]})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def bookmarked_stocks(request):
    """북마크한 주식 관리 API"""
    user = request.user

    if request.method == 'GET':
        bookmarks = BookmarkedStock.objects.filter(user=user).order_by('-created_at')
        stocks = []

        for bookmark in bookmarks:
            db_stock = Stock.objects.filter(symbol=bookmark.symbol).first()

            if db_stock:
                stocks.append({
                    'symbol': db_stock.symbol, 'code': db_stock.code, 'name': db_stock.name,
                    'current_price': db_stock.current_price, 'change_percent': db_stock.change_percent,
                    'market': db_stock.market, 'bookmarked_at': bookmark.created_at.isoformat(),
                })
            else:
                try:
                    info = yf.Ticker(bookmark.symbol).info
                    current_price = info.get('regularMarketPrice') or info.get('currentPrice')
                    previous_close = info.get('previousClose')

                    stocks.append({
                        'symbol': bookmark.symbol,
                        'code': bookmark.symbol.replace('.KS', '').replace('.KQ', ''),
                        'name': bookmark.name, 'current_price': current_price,
                        'change_percent': calculate_change_percent(current_price, previous_close),
                        'market': 'KR' if '.KS' in bookmark.symbol or '.KQ' in bookmark.symbol else 'US',
                        'bookmarked_at': bookmark.created_at.isoformat(),
                    })
                except Exception:
                    stocks.append({
                        'symbol': bookmark.symbol,
                        'code': bookmark.symbol.replace('.KS', '').replace('.KQ', ''),
                        'name': bookmark.name, 'current_price': None, 'change_percent': None,
                        'market': 'KR' if '.KS' in bookmark.symbol or '.KQ' in bookmark.symbol else 'US',
                        'bookmarked_at': bookmark.created_at.isoformat(),
                    })

        return Response({'count': len(stocks), 'stocks': stocks})

    elif request.method == 'POST':
        symbol = request.data.get('symbol')
        name = request.data.get('name', '')

        if not symbol:
            return Response({'error': '종목 심볼이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if BookmarkedStock.objects.filter(user=user, symbol=symbol).exists():
            return Response({'error': '이미 북마크한 종목입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if not name:
            db_stock = Stock.objects.filter(symbol=symbol).first()
            if db_stock:
                name = db_stock.name
            else:
                try:
                    info = yf.Ticker(symbol).info
                    name = info.get('longName') or info.get('shortName') or symbol
                except Exception:
                    name = symbol

        bookmark = BookmarkedStock.objects.create(user=user, symbol=symbol, name=name)
        return Response({'message': '북마크에 추가되었습니다.', 'symbol': bookmark.symbol, 'name': bookmark.name}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        symbol = request.data.get('symbol')
        if not symbol:
            return Response({'error': '종목 심볼이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        deleted, _ = BookmarkedStock.objects.filter(user=user, symbol=symbol).delete()
        if deleted:
            return Response({'message': '북마크가 삭제되었습니다.'})
        return Response({'error': '북마크를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_bookmark(request, symbol):
    """특정 종목의 북마크 여부 확인"""
    is_bookmarked = BookmarkedStock.objects.filter(user=request.user, symbol=symbol).exists()
    return Response({'is_bookmarked': is_bookmarked})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_bookmarked_stocks(request):
    """
    북마크한 주식들의 실시간 가격 갱신
    북마크 개수가 적어서 빠르게 갱신 가능
    """
    user = request.user
    bookmarks = BookmarkedStock.objects.filter(user=user)
    
    if not bookmarks.exists():
        return Response({'success': False, 'message': '북마크한 종목이 없습니다.'})
    
    updated_count = 0
    symbols = [b.symbol for b in bookmarks]
    
    # 배치로 한번에 가격 조회 (yfinance Tickers)
    try:
        batch_str = ' '.join(symbols)
        tickers = yf.Tickers(batch_str)
        
        for symbol in symbols:
            try:
                ticker_obj = tickers.tickers.get(symbol) or tickers.tickers.get(symbol.upper())
                if not ticker_obj:
                    continue
                
                info = ticker_obj.info
                if not info:
                    continue
                
                current_price = info.get('regularMarketPrice') or info.get('currentPrice')
                previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
                market_cap = info.get('marketCap', 0)
                
                if current_price:
                    change_pct = calculate_change_percent(current_price, previous_close) if previous_close else 0
                    
                    # DB에 해당 종목이 있으면 업데이트
                    Stock.objects.filter(symbol=symbol).update(
                        current_price=round(current_price, 2),
                        change_percent=change_pct,
                        market_cap=market_cap or 0,
                    )
                    updated_count += 1
            except Exception as e:
                print(f"Error updating {symbol}: {e}")
                continue
                
    except Exception as e:
        return Response({'success': False, 'message': f'갱신 중 오류: {str(e)}'})
    
    return Response({
        'success': True,
        'message': f'북마크 {updated_count}개 종목 가격 갱신 완료',
        'updated_count': updated_count,
        'total_count': len(symbols),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_popular_stocks(request):
    """인기 종목 목록 조회"""
    market = request.GET.get('market', '').upper()
    limit = min(int(request.GET.get('limit', 20)), 50)

    if market == 'KR':
        stocks = Stock.objects.filter(market='KR')[:limit]
    elif market == 'US':
        stocks = Stock.objects.filter(market='US')[:limit]
    else:
        kr_stocks = list(Stock.objects.filter(market='KR')[:limit // 2])
        us_stocks = list(Stock.objects.filter(market='US')[:limit // 2])
        stocks = kr_stocks + us_stocks

    results = [
        {
            'symbol': s.symbol, 'code': s.code, 'name': s.name,
            'current_price': s.current_price, 'change_percent': s.change_percent,
            'market_cap': s.market_cap, 'market': s.market,
        }
        for s in stocks
    ]

    serializer = PopularStockSerializer(results, many=True)
    return Response({'stocks': serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_stock_detail(request, symbol):
    """주식 종목 상세 정보 조회"""
    try:
        info = yf.Ticker(symbol).info

        if not info or info.get('regularMarketPrice') is None:
            return Response({'error': '종목을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        current_price = info.get('regularMarketPrice') or info.get('currentPrice')
        previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
        change = (current_price - previous_close) if current_price and previous_close else None

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
            'change_percent': calculate_change_percent(current_price, previous_close),
        }

        serializer = StockDetailSerializer(data)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': f'데이터를 가져오는 중 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_stock_chart(request, symbol):
    """주식 차트 데이터 조회"""
    period = request.GET.get('period', '1mo')
    interval = request.GET.get('interval', '1d')

    valid_periods = {'1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'}
    valid_intervals = {'1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'}

    if period not in valid_periods:
        return Response({'error': '유효하지 않은 기간입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    if interval not in valid_intervals:
        return Response({'error': '유효하지 않은 간격입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        hist = yf.Ticker(symbol).history(period=period, interval=interval)

        if hist.empty:
            return Response({'error': '차트 데이터를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        chart_data = [
            {
                'date': date.isoformat(),
                'open': round(row['Open'], 2) if row['Open'] else None,
                'high': round(row['High'], 2) if row['High'] else None,
                'low': round(row['Low'], 2) if row['Low'] else None,
                'close': round(row['Close'], 2) if row['Close'] else None,
                'volume': int(row['Volume']) if row['Volume'] else 0,
            }
            for date, row in hist.iterrows()
        ]

        return Response({'symbol': symbol, 'period': period, 'interval': interval, 'data': chart_data})

    except Exception as e:
        return Response({'error': f'차트 데이터 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_stock_news(request, symbol):
    """주식 종목 관련 뉴스 조회"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        stock_name = info.get('longName') or info.get('shortName', symbol)

        naver_client_id = getattr(settings, 'NAVER_CLIENT_ID', None)
        naver_client_secret = getattr(settings, 'NAVER_CLIENT_SECRET', None)

        if not naver_client_id or not naver_client_secret:
            news = ticker.news or []
            news_list = [
                {
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'publisher': item.get('publisher'),
                    'published_date': item.get('providerPublishTime'),
                    'thumbnail': item.get('thumbnail', {}).get('resolutions', [{}])[0].get('url') if item.get('thumbnail') else None,
                }
                for item in news[:10]
            ]
            serializer = StockNewsSerializer(news_list, many=True)
            return Response({'news': serializer.data})

        res = requests.get(
            "https://openapi.naver.com/v1/search/news.json",
            headers={"X-Naver-Client-Id": naver_client_id, "X-Naver-Client-Secret": naver_client_secret},
            params={"query": f"{stock_name} 주식", "display": 10, "sort": "date"},
        )

        if res.status_code != 200:
            return Response({'news': []})

        news_list = [
            {
                'title': unescape(strip_tags(item.get("title", ""))),
                'link': item.get('originallink') or item.get('link'),
                'publisher': None, 'published_date': item.get('pubDate'), 'thumbnail': None,
                'description': unescape(strip_tags(item.get("description", ""))),
            }
            for item in res.json().get("items", [])
        ]

        return Response({'news': news_list})

    except Exception as e:
        return Response({'error': f'뉴스 조회 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def translate_description(request):
    """영문 기업 설명을 한글로 번역"""
    text = request.data.get('text', '')

    if not text:
        return Response({'error': '번역할 텍스트가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        client = get_openai_client()

        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "당신은 금융/비즈니스 전문 번역가입니다. 영어로 된 기업 설명을 자연스러운 한국어로 번역해주세요. 전문 용어는 적절한 한국어로, 기업명은 원문 유지, 존댓말 사용."
                },
                {"role": "user", "content": f"다음 기업 설명을 한국어로 번역해주세요:\n\n{text}"}
            ],
            max_tokens=1000,
            temperature=0.3,
        )

        return Response({'translated': response.choices[0].message.content.strip()})

    except Exception as e:
        return Response({'error': f'번역 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
