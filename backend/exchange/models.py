from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    """환율 정보 모델"""
    # 통화 코드 (예: USD, EUR, JPY(100) 등)
    cur_unit = models.CharField(max_length=20, unique=True)
    # 국가/통화명 (예: 미국 달러, 유럽연합 유로 등)
    cur_nm = models.CharField(max_length=100)
    # 외화 → 원화 (외화를 팔 때, 여행 후 남은 외화를 원화로 바꿀 때)
    ttb = models.CharField(max_length=20, blank=True)
    # 원화 → 외화 (외화를 살 때, 환전할 때)
    tts = models.CharField(max_length=20, blank=True)
    # 매매기준율
    deal_bas_r = models.CharField(max_length=20, blank=True)
    # 장부가격
    bkpr = models.CharField(max_length=20, blank=True)
    # 서울외국환중개 매매기준율
    kftc_deal_bas_r = models.CharField(max_length=20, blank=True)
    # 서울외국환중개 장부가격
    kftc_bkpr = models.CharField(max_length=20, blank=True)
    # 환율 적용일 (YYYYMMDD)
    search_date = models.CharField(max_length=10)
    # 마지막 업데이트 시간
    updated_at = models.DateTimeField(auto_now=True)
    # 생성 시간
    created_at = models.DateTimeField(auto_now_add=True)
