"""
파일명: news/serializers.py
설명: 뉴스 시리얼라이저

클래스:
    - NewsSerializer: 뉴스 시리얼라이저

주요 기능:
    - 북마크 여부(is_bookmarked) 자동 계산
    - 현재 로그인한 사용자 기준으로 판단
"""

from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = "__all__"

    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user.bookmarked_news.filter(pk=obj.pk).exists()
        return False
