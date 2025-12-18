from django.conf import settings
from django.db import models

# Create your models here.
class DepositProduct(models.Model):
    # 1. 금융 상품 코드(PK)
    fin_prdt_cd = models.CharField(max_length=50, unique=True)
    # 2. 회사명
    kor_co_nm = models.CharField(max_length=100)
    # 3. 상품명
    fin_prdt_nm = models.CharField(max_length=150)
    # 4. 가입 제한 여부
    join_deny = models.IntegerField()
    # 5. 가입 대상
    join_member = models.CharField(max_length=200)
    # 6. 가입 방법
    join_way = models.CharField(max_length=100)
    # 7. 우대 조건
    spcl_cnd = models.TextField(blank=True, default="")
    # 8. 기타 사항
    etc_note = models.TextField(blank=True, default="")


class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')

    # 1. 저축 기간
    save_trm = models.IntegerField()
    # 2. 기본 이자율
    intr_rate = models.FloatField()
    # 3. 최고 우대금리
    intr_rate2 = models.FloatField()
    # 4. 적립 유형(예: 자유/정액 등) - 예금이면 비거나 다른 값일 수도
    rsrv_type = models.CharField(max_length=30)
    # 5. 한도 금액
    max_limit = models.IntegerField(null=True, blank=True)
    # 6. 이자율 유형명
    intr_rate_type_nm = models.CharField(max_length=50)


class SavingProduct(models.Model):
    # 1. 금융 상품 코드(PK)
    fin_prdt_cd = models.CharField(max_length=50, unique=True)
    # 2. 회사명
    kor_co_nm = models.CharField(max_length=100)
    # 3. 상품명
    fin_prdt_nm = models.CharField(max_length=150)
    # 4. 가입 제한 여부
    join_deny = models.IntegerField()
    # 5. 가입 대상
    join_member = models.CharField(max_length=200)
    # 6. 가입 방법
    join_way = models.CharField(max_length=100)
    # 7. 우대 조건
    spcl_cnd = models.TextField(blank=True, default="")
    # 8. 기타 사항
    etc_note = models.TextField(blank=True, default="")


class SavingOption(models.Model):
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='options')

    # 1. 저축 기간
    save_trm = models.IntegerField()
    # 2. 기본 이자율
    intr_rate = models.FloatField()
    # 3. 최고 우대금리
    intr_rate2 = models.FloatField()
    # 4. 적립 유형(예: 자유/정액 등) - 예금이면 비거나 다른 값일 수도
    rsrv_type = models.CharField(max_length=30)
    # 5. 한도 금액
    max_limit = models.IntegerField(null=True, blank=True)
    # 6. 이자율 유형명
    intr_rate_type_nm = models.CharField(max_length=50)


User = settings.AUTH_USER_MODEL
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    fin_prdt_cd = models.CharField(max_length=50)
    product_type = models.CharField(max_length=10, choices=[("deposit", "예금"), ("saving", "적금")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "fin_prdt_cd")