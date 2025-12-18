from rest_framework import serializers
from .models import AnalysisRequest, RecommendationResult


class AnalysisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisRequest
        fields = ["purpose", "period_months", "target_amount", "monthly_amount"]


class RecommendationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationResult
        fields = ["summary", "items", "created_at"]