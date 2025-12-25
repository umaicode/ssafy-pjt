from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    # 주식 검색 (종목명 또는 심볼로 검색)
    path('search/', views.search_stocks, name='search_stocks'),
    
    # 주요 지표 (나스닥, S&P500, 환율 등)
    path('indices/', views.get_market_indices, name='market_indices'),
    
    # 인기 종목 (기존 API 호환)
    path('popular/', views.get_popular_stocks, name='popular_stocks'),
    
    # 국내 주식 (DB에서 조회, 페이지네이션)
    path('kr/', views.get_kr_stocks, name='kr_stocks'),
    
    # 해외 주식 (DB에서 조회, 페이지네이션)
    path('us/', views.get_us_stocks, name='us_stocks'),
    
    # 데이터 갱신 API (30분 제한)
    path('refresh/', views.refresh_stocks, name='refresh_stocks'),
    
    # 갱신 상태 조회
    path('update-status/', views.get_update_status, name='update_status'),
    
    # 북마크 주식 (조회/추가/삭제)
    path('bookmarks/', views.bookmarked_stocks, name='bookmarked_stocks'),
    
    # 북마크 주식 갱신 (실시간 가격 업데이트)
    path('bookmarks/refresh/', views.refresh_bookmarked_stocks, name='refresh_bookmarked_stocks'),
    
    # 북마크 여부 확인
    path('bookmarks/<str:symbol>/check/', views.check_bookmark, name='check_bookmark'),
    
    # 기업설명 번역 (AI)
    path('translate/', views.translate_description, name='translate_description'),
    
    # 종목 상세 정보
    path('<str:symbol>/', views.get_stock_detail, name='stock_detail'),
    
    # 종목 차트 데이터 (기간별)
    path('<str:symbol>/chart/', views.get_stock_chart, name='stock_chart'),
    
    # 종목 뉴스 (네이버 뉴스 API)
    path('<str:symbol>/news/', views.get_stock_news, name='stock_news'),
]
