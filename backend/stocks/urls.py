from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    # 주식 검색 (종목명 또는 심볼로 검색)
    path('search/', views.search_stocks, name='search_stocks'),
    
    # 주요 지표 (나스닥, S&P500, 환율 등)
    path('indices/', views.get_market_indices, name='market_indices'),
    
    # 인기 종목 (한국/미국 주요 종목)
    path('popular/', views.get_popular_stocks, name='popular_stocks'),
    
    # 기업설명 번역 (AI)
    path('translate/', views.translate_description, name='translate_description'),
    
    # 종목 상세 정보
    path('<str:symbol>/', views.get_stock_detail, name='stock_detail'),
    
    # 종목 차트 데이터 (기간별)
    path('<str:symbol>/chart/', views.get_stock_chart, name='stock_chart'),
    
    # 종목 뉴스 (네이버 뉴스 API)
    path('<str:symbol>/news/', views.get_stock_news, name='stock_news'),
]
