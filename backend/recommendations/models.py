from django.db import models
from django.conf import settings

# Create your models here.
class AnalysisRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50)
    period_months = models.PositiveIntegerField()
    target_amount = models.BigIntegerField()
    monthly_amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class RecommendationResult(models.Model):
    analysis = models.OneToOneField(AnalysisRequest, on_delete=models.CASCADE, related_name='result')
    # GPT 원문 응답
    gpt_raw = models.TextField(blank=True, default="")
    # 요약
    summary = models.TextField(blank=True, default="")
    # 선택 상품들
    items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


class RecommendationCache(models.Model):
    cache_key = models.CharField(max_length=128, unique=True)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)