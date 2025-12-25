"""
파일명: recommendations/serializers.py
설명: AI 추천 시스템 시리얼라이저

클래스:
    - AnalysisCreateSerializer: 분석 요청 생성 시리얼라이저
    - RecommendationResultSerializer: 추천 결과 시리얼라이저

목적별 필드:
    - housing: 주거 관련 (housing_type, target_region, apartment_price)
    - travel: 여행 관련 (travel_destination, travel_country_code)
    - savings: 목돈 관련 (savings_purpose_detail)
"""

from rest_framework import serializers
from .models import AnalysisRequest, RecommendationResult


class AnalysisCreateSerializer(serializers.ModelSerializer):
    """분석 요청 생성 시리얼라이저 - 목적별 필드 검증"""

    class Meta:
        model = AnalysisRequest
        fields = [
            "purpose",
            "period_months",
            "target_amount",
            "monthly_amount",
            "current_savings",
            # 주택 관련
            "housing_type",
            "target_region",
            "target_apartment",
            "apartment_price",
            # 여행 관련
            "travel_destination",
            "travel_country_code",
            # 목돈 관련
            "savings_purpose_detail",
        ]

    def validate(self, data):
        purpose = data.get("purpose")

        # 주택 목적일 때 housing_type 필수
        if purpose == "housing":
            if not data.get("housing_type"):
                raise serializers.ValidationError(
                    {"housing_type": "주택 목적일 때 주거 유형을 선택해주세요."}
                )

        # 여행 목적일 때 travel_destination 권장
        if purpose == "travel":
            if not data.get("travel_destination"):
                # 필수는 아니지만 입력 권장
                pass

        return data


class RecommendationResultSerializer(serializers.ModelSerializer):
    """추천 결과 시리얼라이저 - 확장된 필드 포함"""

    class Meta:
        model = RecommendationResult
        fields = [
            "summary",
            "items",
            "strategy",
            "alternative_plans",
            "combination_strategy",
            "goal_math",
            # 주택 관련
            "real_estate_analysis",
            "recommended_properties",
            # 여행 관련
            "travel_analysis",
            "exchange_rate_info",
            "recommended_destinations",
            "final_amount_in_currency",
            # 뉴스/유튜브
            "related_news",
            "related_videos",
            # AI 판단
            "ai_verdict",
            "created_at",
        ]


class AnalysisDetailSerializer(serializers.ModelSerializer):
    """분석 요청 상세 조회 시리얼라이저"""

    result = RecommendationResultSerializer(read_only=True)
    purpose_display = serializers.SerializerMethodField()
    housing_type_display = serializers.SerializerMethodField()

    class Meta:
        model = AnalysisRequest
        fields = "__all__"

    def get_purpose_display(self, obj):
        return obj.get_purpose_display() if obj.purpose else None

    def get_housing_type_display(self, obj):
        return obj.get_housing_type_display() if obj.housing_type else None
