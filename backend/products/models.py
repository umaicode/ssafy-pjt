"""
파일명: products/models.py
설명: 금융 상품(예금/적금) 관련 모델 정의

모델 목록:
- DepositProduct: 예금 상품 정보
- DepositOption: 예금 상품의 옵션(기간별 금리)
- SavingProduct: 적금 상품 정보
- SavingOption: 적금 상품의 옵션(기간별 금리)
- Like: 사용자의 상품 좋아요 정보

데이터 출처: 금융감독원 금융상품비교공시 API
"""

from django.conf import settings
from django.db import models


class DepositProduct(models.Model):
    """
    예금 상품 모델
    
    금융감독원 API에서 가져온 예금 상품 기본 정보를 저장합니다.
    
    Attributes:
        fin_prdt_cd: 금융 상품 코드 (고유값)
        kor_co_nm: 금융회사명
        fin_prdt_nm: 상품명
        join_deny: 가입 제한 여부 (1: 제한없음, 2: 서민전용, 3: 일부제한)
        join_member: 가입 대상
        join_way: 가입 방법
        spcl_cnd: 우대 조건
        etc_note: 기타 유의사항
    """
    fin_prdt_cd = models.CharField(max_length=50, unique=True)
    kor_co_nm = models.CharField(max_length=100)
    fin_prdt_nm = models.CharField(max_length=150)
    join_deny = models.IntegerField()
    join_member = models.CharField(max_length=200)
    join_way = models.CharField(max_length=100)
    spcl_cnd = models.TextField(blank=True, default="")
    etc_note = models.TextField(blank=True, default="")


class DepositOption(models.Model):
    """
    예금 상품 옵션 모델
    
    예금 상품의 기간별 금리 정보를 저장합니다.
    하나의 예금 상품은 여러 개의 옵션을 가질 수 있습니다.
    
    Attributes:
        product: 연결된 예금 상품 (FK)
        save_trm: 저축 기간 (개월)
        intr_rate: 기본 금리
        intr_rate2: 최고 우대금리
        rsrv_type: 적립 유형
        max_limit: 최고 한도
        intr_rate_type_nm: 금리 유형명 (단리/복리)
    """
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    save_trm = models.IntegerField()
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    rsrv_type = models.CharField(max_length=30)
    max_limit = models.IntegerField(null=True, blank=True)
    intr_rate_type_nm = models.CharField(max_length=50)


class SavingProduct(models.Model):
    """
    적금 상품 모델
    
    금융감독원 API에서 가져온 적금 상품 기본 정보를 저장합니다.
    
    Attributes:
        fin_prdt_cd: 금융 상품 코드 (고유값)
        kor_co_nm: 금융회사명
        fin_prdt_nm: 상품명
        join_deny: 가입 제한 여부
        join_member: 가입 대상
        join_way: 가입 방법
        spcl_cnd: 우대 조건
        etc_note: 기타 유의사항
    """
    fin_prdt_cd = models.CharField(max_length=50, unique=True)
    kor_co_nm = models.CharField(max_length=100)
    fin_prdt_nm = models.CharField(max_length=150)
    join_deny = models.IntegerField()
    join_member = models.CharField(max_length=200)
    join_way = models.CharField(max_length=100)
    spcl_cnd = models.TextField(blank=True, default="")
    etc_note = models.TextField(blank=True, default="")


class SavingOption(models.Model):
    """
    적금 상품 옵션 모델
    
    적금 상품의 기간별 금리 정보를 저장합니다.
    
    Attributes:
        product: 연결된 적금 상품 (FK)
        save_trm: 저축 기간 (개월)
        intr_rate: 기본 금리
        intr_rate2: 최고 우대금리
        rsrv_type: 적립 유형 (자유적립식/정액적립식)
        max_limit: 최고 한도
        intr_rate_type_nm: 금리 유형명
    """
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='options')
    save_trm = models.IntegerField()
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    rsrv_type = models.CharField(max_length=30)
    max_limit = models.IntegerField(null=True, blank=True)
    intr_rate_type_nm = models.CharField(max_length=50)


# 커스텀 User 모델 참조
User = settings.AUTH_USER_MODEL


class Like(models.Model):
    """
    상품 좋아요 모델
    
    사용자가 좋아요한 금융 상품 정보를 저장합니다.
    
    Attributes:
        user: 사용자 (FK)
        fin_prdt_cd: 금융 상품 코드
        product_type: 상품 유형 ('deposit' 또는 'saving')
        created_at: 좋아요 생성 일시
        
    Meta:
        unique_together: 같은 상품에 중복 좋아요 방지
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    fin_prdt_cd = models.CharField(max_length=50)
    product_type = models.CharField(max_length=10, choices=[("deposit", "예금"), ("saving", "적금")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "fin_prdt_cd", "product_type")