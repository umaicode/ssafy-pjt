"""
파일명: news/urls.py
설명: 금융 뉴스 API URL 패턴

URL 패턴:
- GET /api/news/ : 뉴스 목록 조회
- POST /api/news/fetch/ : 네이버에서 뉴스 검색/저장
- GET /api/news/<pk>/ : 뉴스 상세 조회
- POST /api/news/<pk>/bookmark/ : 북마크 토글
"""

from django.urls import path
from . import views


urlpatterns = [
    # 뉴스 목록 (mode=bookmark 파라미터로 북마크만 조회 가능)
    path("", views.news_list, name="news_list"),
    # 네이버 API에서 뉴스 검색 후 DB에 저장
    path("fetch/", views.fetch_news, name="fetch_news"),
    # 뉴스 상세 조회
    path("<int:pk>/", views.news_detail, name="news_detail"),
    # 북마크 토글
    path("<int:pk>/bookmark/", views.toggle_bookmark, name="toggle_bookmark"),
]