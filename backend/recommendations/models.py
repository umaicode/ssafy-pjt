from django.db import models
from django.conf import settings


# Create your models here.
class AnalysisRequest(models.Model):
    """사용자 분석 요청 모델 - 목적별 맞춤 정보 저장"""

    # 목적 선택
    PURPOSE_CHOICES = [
        ("housing", "주택"),
        ("savings", "목돈"),
        ("travel", "여행"),
    ]

    # 주택 세부 옵션
    HOUSING_TYPE_CHOICES = [
        ("purchase", "매매"),
        ("jeonse", "전세"),
        ("wolse_deposit", "월세 보증금"),
        ("wolse", "월세"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    period_months = models.PositiveIntegerField()
    target_amount = models.BigIntegerField()
    monthly_amount = models.BigIntegerField()

    # 현재 보유 금액 (예금 활용 가능 금액)
    current_savings = models.BigIntegerField(default=0)

    # === 주택 관련 필드 ===
    housing_type = models.CharField(
        max_length=20, choices=HOUSING_TYPE_CHOICES, blank=True, null=True
    )
    target_region = models.CharField(max_length=100, blank=True, null=True)  # 목표 지역
    target_apartment = models.CharField(
        max_length=200, blank=True, null=True
    )  # 목표 아파트명
    apartment_price = models.BigIntegerField(
        blank=True, null=True
    )  # 아파트 가격 (자동 설정 가능)

    # === 여행 관련 필드 ===
    travel_destination = models.CharField(
        max_length=100, blank=True, null=True
    )  # 여행지
    travel_country_code = models.CharField(
        max_length=10, blank=True, null=True
    )  # 통화 코드 (USD, JPY 등)

    # === 목돈 관련 필드 ===
    savings_purpose_detail = models.CharField(
        max_length=100, blank=True, null=True
    )  # 세부 목적 (결혼, 자동차 등)

    created_at = models.DateTimeField(auto_now_add=True)


class RecommendationResult(models.Model):
    analysis = models.OneToOneField(
        AnalysisRequest, on_delete=models.CASCADE, related_name="result"
    )
    # GPT 원문 응답
    gpt_raw = models.TextField(blank=True, default="")
    # 요약
    summary = models.TextField(blank=True, default="")
    # 선택 상품들 (예금/적금 추천)
    items = models.JSONField(default=list)

    # === 확장된 결과 필드 ===
    # 전략 설명
    strategy = models.TextField(blank=True, default="")
    # 대안 플랜들 (목표 달성 불가 시)
    alternative_plans = models.JSONField(default=list)
    # 예금/적금 조합 전략 (동시 가입 시 최적 조합)
    combination_strategy = models.JSONField(default=dict)
    # 목표 계산 결과
    goal_math = models.JSONField(default=dict)

    # === 주택 관련 결과 ===
    real_estate_analysis = models.JSONField(default=dict)  # 부동산 시장 분석
    recommended_properties = models.JSONField(default=list)  # 추천 매물

    # === 여행 관련 결과 ===
    travel_analysis = models.JSONField(default=dict)  # 여행지 분석
    exchange_rate_info = models.JSONField(default=dict)  # 환율 정보
    recommended_destinations = models.JSONField(default=list)  # 추천 여행지
    final_amount_in_currency = models.JSONField(default=dict)  # 외화 환산 금액

    # === 뉴스/유튜브 연동 결과 ===
    related_news = models.JSONField(default=list)
    related_videos = models.JSONField(default=list)

    # AI 최종 판단/조언
    ai_verdict = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)


class RecommendationCache(models.Model):
    cache_key = models.CharField(max_length=128, unique=True)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
