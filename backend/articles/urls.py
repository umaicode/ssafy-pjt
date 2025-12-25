"""
파일명: articles/urls.py
설명: 커뮤니티 게시판 API URL 패턴

URL 패턴:
- GET/POST /api/v1/articles/ : 게시글 목록/생성
- GET/PATCH/DELETE /api/v1/articles/<pk>/ : 게시글 상세/수정/삭제
- GET /api/v1/articles/<pk>/comments/ : 댓글 목록
- POST /api/v1/articles/<pk>/comments/create/ : 댓글 생성
- PATCH/DELETE /api/v1/comments/<pk>/ : 댓글 수정/삭제
- POST /api/v1/articles/<pk>/like/ : 게시글 좋아요 토글
- POST /api/v1/comments/<pk>/like/ : 댓글 좋아요 토글
"""

from django.urls import path
from . import views

urlpatterns = [
    # ========================================
    # 게시글 API
    # ========================================
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path("articles/<int:article_pk>/like/", views.toggle_article_like),
    
    # ========================================
    # 댓글 API
    # ========================================
    path('articles/<int:article_pk>/comments/', views.comment_list),
    path('articles/<int:article_pk>/comments/create/', views.comment_create), 
    path('comments/<int:comment_pk>/', views.comment_detail),
    path("comments/<int:comment_pk>/like/", views.toggle_comment_like),
]
