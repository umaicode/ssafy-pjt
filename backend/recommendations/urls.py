"""
파일명: recommendations/urls.py
설명: AI 금융 분석 추천 API URL 패턴

URL 패턴:
- POST /api/v1/analysis/ : AI 분석 생성 요청
- GET /api/v1/analysis/<id>/result/ : 분석 결과 조회

AI 모델: OpenAI GPT (GMS 프록시 사용)
기능: 사용자 정보 기반 맞춤형 금융 상품 추천
"""

from django.urls import path
from . import views

urlpatterns = [
    # AI 분석 생성
    path("analysis/", views.create_analysis),
    # 분석 결과 조회
    path("analysis/<int:analysis_id>/result/", views.get_analysis_result),
]
