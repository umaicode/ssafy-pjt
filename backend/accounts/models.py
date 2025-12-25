"""
파일명: accounts/models.py
설명: 사용자 계정 관련 모델 정의

모델 목록:
- User: 커스텀 사용자 모델 (Django AbstractUser 확장)
- UserProfile: 사용자 추가 프로필 정보
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    커스텀 사용자 모델
    
    AbstractUser를 확장하여 추가 필드를 정의합니다.
    기본 필드: username, email, password, first_name, last_name 등
    
    Attributes:
        nickname (str): 사용자 닉네임 (최대 30자)
        bookmarked_news (ManyToMany): 북마크한 뉴스 목록
    """
    nickname = models.CharField(max_length=30, blank=True)
    bookmarked_news = models.ManyToManyField(
        "news.News", related_name="bookmarked_by", blank=True
    )


class UserProfile(models.Model):
    """
    사용자 추가 프로필 정보
    
    User 모델과 1:1 관계로 추가 정보를 저장합니다.
    
    Attributes:
        user (OneToOne): 연결된 사용자
        income_range (str): 소득 구간
        created_at (datetime): 생성 일시
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    income_range = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
