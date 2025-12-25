"""
파일명: exchange/urls.py
설명: 환율 정보 API URL 패턴

URL 패턴:
- POST /api/exchange/fetch/ : 한국수출입은행 API에서 환율 가져오기
- GET /api/exchange/rates/ : DB에서 환율 목록 조회
- GET /api/exchange/rates/<cur_unit>/ : 특정 통화 환율 조회

데이터 출처: 한국수출입은행 환율 API
"""

from django.urls import path
from . import views

urlpatterns = [
    # 외부 API에서 환율 데이터 가져와서 DB에 저장
    path('fetch/', views.fetch_exchange_rates, name='fetch_exchange_rates'),
    # DB에서 환율 목록 조회
    path('rates/', views.get_exchange_rates, name='get_exchange_rates'),
    # 특정 통화의 환율 정보 조회
    path('rates/<str:cur_unit>/', views.get_exchange_rate_detail, name='exchange_rate_detail'),
]
