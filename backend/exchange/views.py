import os
import requests
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ExchangeRate
from .serializers import ExchangeRateSerializer


@api_view(['POST'])
def fetch_exchange_rates(request):
    """
    한국 수출입은행 API에서 환율 정보를 가져와서 DB에 저장합니다.
    """
    api_key = os.getenv('EXCHANGE_API_KEY')
    
    if not api_key:
        return Response(
            {'error': 'EXCHANGE_API_KEY가 설정되지 않았습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # 오늘 날짜 (YYYYMMDD 형식)
    search_date = datetime.now().strftime('%Y%m%d')
    
    # 주요 통화 리스트 (API에서 실제 제공하는 통화)
    currencies = ['USD', 'EUR', 'JPY(100)', 'CNH', 'GBP', 'THB', 'SGD', 'HKD']
    
    base_url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    
    created_count = 0
    updated_count = 0
    
    try:
        # API 호출
        params = {
            'authkey': api_key,
            'searchdate': search_date,
            'data': 'AP01'
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 디버깅: API 응답 확인
        print(f"API 응답 데이터 개수: {len(data)}")
        if len(data) == 0:
            # 주말/공휴일인 경우 가장 최근 영업일 데이터 조회 시도
            # 최대 7일 전까지 시도
            from datetime import timedelta
            for days_back in range(1, 8):
                past_date = datetime.now() - timedelta(days=days_back)
                params['searchdate'] = past_date.strftime('%Y%m%d')
                response = requests.get(base_url, params=params, timeout=10)
                data = response.json()
                if len(data) > 0:
                    search_date = params['searchdate']
                    print(f"영업일 데이터 발견: {search_date}")
                    break
        
        # 주요 통화만 필터링하여 DB에 저장/업데이트
        for item in data:
            cur_unit = item.get('cur_unit', '')
            
            if cur_unit in currencies:
                exchange_rate = ExchangeRate.objects.filter(cur_unit=cur_unit).first()
                
                save_data = {
                    'cur_unit': cur_unit,
                    'cur_nm': item.get('cur_nm', ''),
                    'ttb': item.get('ttb', ''),
                    'tts': item.get('tts', ''),
                    'deal_bas_r': item.get('deal_bas_r', ''),
                    'bkpr': item.get('bkpr', ''),
                    'kftc_deal_bas_r': item.get('kftc_deal_bas_r', ''),
                    'kftc_bkpr': item.get('kftc_bkpr', ''),
                    'search_date': search_date,
                }
                
                if exchange_rate:
                    for key, value in save_data.items():
                        setattr(exchange_rate, key, value)
                    exchange_rate.save()
                    updated_count += 1
                else:
                    ExchangeRate.objects.create(**save_data)
                    created_count += 1
        
        return Response({
            'message': '환율 정보를 성공적으로 가져왔습니다.',
            'created': created_count,
            'updated': updated_count,
            'date': search_date
        }, status=status.HTTP_201_CREATED)
    
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': f'환율 정보를 가져오는데 실패했습니다: {str(e)}'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        return Response(
            {'error': f'예상치 못한 오류가 발생했습니다: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_exchange_rates(request):
    """
    DB에 저장된 환율 정보를 조회합니다.
    """
    exchange_rates = ExchangeRate.objects.all()
    serializer = ExchangeRateSerializer(exchange_rates, many=True)
    
    return Response({
        'count': exchange_rates.count(),
        'rates': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_exchange_rate_detail(request, cur_unit):
    """
    특정 통화의 환율 정보를 조회합니다.
    """
    try:
        exchange_rate = ExchangeRate.objects.get(cur_unit=cur_unit)
        serializer = ExchangeRateSerializer(exchange_rate)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ExchangeRate.DoesNotExist:
        return Response(
            {'error': f'{cur_unit} 통화의 환율 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )
