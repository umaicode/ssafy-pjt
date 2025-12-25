"""
파일명: news/models.py
설명: 금융 뉴스 모델 정의

모델 목록:
- News: 네이버 API에서 가져온 금융 뉴스 정보

데이터 출처: 네이버 검색 API
"""

from django.db import models
from django.conf import settings


class News(models.Model):
    """
    금융 뉴스 모델
    
    네이버 검색 API에서 가져온 금융 관련 뉴스를 저장합니다.
    사용자별로 뉴스를 저장하여 북마크 기능을 제공합니다.
    
    Attributes:
        user: 뉴스를 저장한 사용자 (FK)
        title: 뉴스 제목
        description: 뉴스 내용 요약
        link: 뉴스 원문 URL
        pubDate: 발행일
        
    Meta:
        unique_together: 사용자별 동일 제목 뉴스 중복 방지
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="news"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField()
    pubDate = models.CharField(max_length=50)

    class Meta:
        unique_together = ["user", "title"]
