"""
파일명: chatbot/urls.py
설명: AI 챗봇 (핑프) API URL 패턴

URL 패턴:
- POST /api/chatbot/ : 챗봇 메시지 전송/응답
- GET /api/chatbot/suggestions/ : 추천 질문 목록
- POST /api/chatbot/bank-search/ : 위치 기반 은행 검색

AI 모델: OpenAI GPT (GMS 프록시 사용)
"""

from django.urls import path
from . import views

urlpatterns = [
    # AI 챗봇 대화 API
    path("", views.chat, name="chat"),
    # 추천 질문 목록
    path("suggestions/", views.chat_suggestions, name="chat_suggestions"),
    # 위치 기반 은행 검색
    path(
        "bank-search/",
        views.search_bank_with_location,
        name="search_bank_with_location",
    ),
]
