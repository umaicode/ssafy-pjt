from django.urls import path
from . import views

urlpatterns = [
    # POST - API에서 환율 정보 가져와서 DB에 저장
    path('fetch/', views.fetch_exchange_rates, name='fetch_exchange_rates'),
    # GET - DB에서 환율 정보 조회
    path('rates/', views.get_exchange_rates, name='get_exchange_rates'),
    # GET - 특정 통화의 환율 정보 조회
    path('rates/<str:cur_unit>/', views.get_exchange_rate_detail, name='exchange_rate_detail'),
]
