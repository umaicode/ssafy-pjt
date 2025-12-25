"""
파일명: products/serializers.py
설명: 금융 상품(예금/적금) 시리얼라이저

클래스:
    - DepositOptionSerializer: 예금 옵션(기간별 금리) 시리얼라이저
    - DepositProductSerializer: 예금 상품 시리얼라이저 (옵션 포함)
    - SavingOptionSerializer: 적금 옵션 시리얼라이저
    - SavingProductSerializer: 적금 상품 시리얼라이저 (옵션 포함)
    - LikeSerializer: 상품 좋아요 시리얼라이저

주요 필드:
    - fin_prdt_cd: 금융상품 코드 (PK)
    - kor_co_nm: 은행명
    - fin_prdt_nm: 상품명
    - intr_rate/intr_rate2: 기본금리/최고금리
    - save_trm: 저축 기간(개월)
"""

from rest_framework import serializers
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption, Like


class DepositOptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DepositOption
        fields = (
            "id",
            "save_trm",
            "intr_rate",
            "intr_rate2",
            "intr_rate_type_nm",
            "rsrv_type",
            "max_limit",
        )


class DepositProductSerializer(serializers.ModelSerializer):
    options = DepositOptionSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProduct
        fields = (
            "id",
            "fin_prdt_cd",
            "kor_co_nm",
            "fin_prdt_nm",
            "join_deny",
            "join_member",
            "join_way",
            "spcl_cnd",
            "etc_note",
            "options",
        )

class SavingOptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SavingOption
        fields = (
            "id",
            "save_trm",
            "intr_rate",
            "intr_rate2",
            "intr_rate_type_nm",
            "rsrv_type",
            "max_limit",
        )

class SavingProductSerializer(serializers.ModelSerializer):
    options = SavingOptionSerializer(many=True, read_only=True)

    class Meta:
        model = SavingProduct
        fields = (
            "id",
            "fin_prdt_cd",
            "kor_co_nm",
            "fin_prdt_nm",
            "join_deny",
            "join_member",
            "join_way",
            "spcl_cnd",
            "etc_note",
            "options",
        )

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "fin_prdt_cd", "product_type", "created_at")