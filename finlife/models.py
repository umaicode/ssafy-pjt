from django.db import models


# Create your models here.
class DepositProducts(models.Model):
    # 금융 상품 코드
    # PRIMARY KEY
    fin_prdt_cd = models.CharField(max_length=50, primary_key=True)
    # 금융회사명
    kor_co_nm = models.CharField(max_length=100)
    # 상품명
    fin_prdt_nm = models.CharField(max_length=100)
    # 기타 참고사항
    etc_note = models.TextField()
    # 금리 (default = -1)
    max_limit = models.IntegerFIeld(default=-1)
    # # 가입 제한
    # join_deny = models.IntegerField()
    # # 가입 대상
    # join_member = models.TextField()
    # # 가입방법
    # join_way = models.TextField()
    # # 우대조건
    # spcl_cnd = models.TextField()


class DepositOptions(models.Model):
    # 상품 코드
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    # 저축 기간 (월)
    save_trm = models.IntegeField()
    # 이자율
    intr_rate = models.FloatField()
    # 최고 우대 금리
    intr_rate2 = models.FloatField()
