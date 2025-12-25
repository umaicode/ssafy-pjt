"""
파일명: articles/models.py
설명: 커뮤니티 게시판 모델 정의

모델 목록:
- Article: 게시글
- Comment: 댓글

기능:
- 게시글/댓글 CRUD
- 조회수 카운트
- 좋아요 기능 (ManyToMany)
"""

from django.db import models
from django.conf import settings


class Article(models.Model):
    """
    게시글 모델
    
    커뮤니티 게시판의 게시글 정보를 저장합니다.
    
    Attributes:
        user: 작성자 (FK)
        title: 제목 (최대 30자)
        content: 내용
        views: 조회수
        created_at: 작성일
        updated_at: 수정일
        like_users: 좋아요한 사용자들 (ManyToMany)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    title = models.CharField(max_length=30)
    content = models.TextField()
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ManyToMany: 여러 사용자가 여러 게시글을 좋아요 가능
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="liked_articles"
    )


class Comment(models.Model):
    """
    댓글 모델
    
    게시글에 달린 댓글 정보를 저장합니다.
    
    Attributes:
        user: 작성자 (FK)
        article: 소속 게시글 (FK)
        content: 댓글 내용 (최대 200자)
        created_at: 작성일
        updated_at: 수정일
        like_users: 좋아요한 사용자들 (ManyToMany)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="liked_comments"
    )

