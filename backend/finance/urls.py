"""
파일명: finance/urls.py
설명: F!NK 프로젝트 메인 URL 설정

이 파일은 Django 프로젝트의 루트 URL 설정 파일입니다.
각 앱의 URL 패턴을 include하여 라우팅을 관리합니다.

URL 패턴 구조:
- /admin/ : Django 관리자 페이지
- /api/products/ : 금융 상품 API (예금, 적금)
- /api/v1/ : 버전 1 API (추천, 커뮤니티)
- /api/news/ : 금융 뉴스 API
- /api/metals/ : 금/은 현물 시세 API
- /api/exchange/ : 환율 정보 API
- /api/chatbot/ : AI 챗봇 API
- /accounts/ : 사용자 인증 API
- /schema/ : API 문서 (Swagger, Redoc)
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # ========================================
    # 관리자
    # ========================================
    path("admin/", admin.site.urls),
    
    # ========================================
    # API 엔드포인트
    # ========================================
    # 금융 상품 (예금, 적금, 좋아요)
    path("api/products/", include("products.urls")),
    
    # AI 추천 분석
    path("api/v1/", include("recommendations.urls")),
    
    # 커뮤니티 게시판
    path("api/v1/", include("articles.urls")),
    
    # 금융 뉴스
    path("api/news/", include("news.urls")),
    
    # 금/은 현물 시세
    path("api/metals/", include("metals.urls")),
    
    # 환율 정보
    path("api/exchange/", include("exchange.urls")),
    
    # AI 챗봇
    path("api/chatbot/", include("chatbot.urls")),

    # 주식
    path("api/stocks/", include("stocks.urls")),
    
    # ========================================
    # API 문서 (drf-spectacular)
    # ========================================
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    
    # ========================================
    # 사용자 인증 (dj-rest-auth)
    # ========================================
    path("accounts/", include("dj_rest_auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/signup/", include("dj_rest_auth.registration.urls")),
]
