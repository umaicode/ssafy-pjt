"""
stocks/models.py
주식 관련 모델 정의

모델 목록:
- Stock: 국내/해외 주식 데이터 (DB 캐싱)
- StockDataUpdate: 주식 데이터 갱신 기록
- BookmarkedStock: 사용자별 북마크한 주식
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Stock(models.Model):
    """
    주식 데이터 모델 (국내/해외 통합)
    
    DB에 캐싱하여 빠른 조회 지원
    """
    MARKET_CHOICES = [
        ('KR', '국내'),
        ('US', '해외'),
    ]
    
    symbol = models.CharField(max_length=20, unique=True, db_index=True)
    code = models.CharField(max_length=10, db_index=True)  # 종목코드 (KR: 005930, US: AAPL)
    name = models.CharField(max_length=100)
    market = models.CharField(max_length=2, choices=MARKET_CHOICES, db_index=True)
    
    current_price = models.FloatField(null=True, blank=True)
    change_percent = models.FloatField(default=0.0)
    market_cap = models.BigIntegerField(default=0, db_index=True)  # 시가총액순 정렬용
    
    sector = models.CharField(max_length=100, blank=True, default='')  # 섹터 (US)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-market_cap']  # 시가총액순 정렬
        indexes = [
            models.Index(fields=['market', '-market_cap']),  # 시장별 시가총액순 조회용
        ]
    
    def __str__(self):
        return f"[{self.market}] {self.name} ({self.symbol})"


class StockDataUpdate(models.Model):
    """
    주식 데이터 갱신 기록
    
    갱신 주기 제한 (30분)을 위한 모델
    """
    MARKET_CHOICES = [
        ('KR', '국내'),
        ('US', '해외'),
    ]
    
    market = models.CharField(max_length=2, choices=MARKET_CHOICES, unique=True)
    last_updated = models.DateTimeField(default=timezone.now)
    stock_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='success')  # success, failed, in_progress
    
    def __str__(self):
        return f"{self.market} - {self.last_updated}"
    
    def can_update(self, minutes=30):
        """갱신 가능 여부 확인 (기본 30분)"""
        if self.status == 'in_progress':
            return False
        elapsed = timezone.now() - self.last_updated
        return elapsed.total_seconds() >= minutes * 60


class BookmarkedStock(models.Model):
    """
    사용자별 북마크한 주식 모델
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarked_stocks'
    )
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'symbol')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.symbol}"
