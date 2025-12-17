from rest_framework import serializers
from .models import DepositProducts, DepositOptions


class DepositProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositProducts
        fields = (
            "id",
            "fin_prdt_cd",
            "kor_co_nm",
            "fin_prdt_nm",
            "etc_note",
            "join_deny",
            "join_member",
            "join_way",
            "spcl_cnd",
        )


class DepositOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositOptions
        fields = (
            'id',
            'intr_rate_type_nm',
            'intr_rate',
            'intr_rate2',
            'save_trm',
            'fin_prdt_cd',
        )


class TopRateSerializer(serializers.Serializer):
    deposit_product = DepositProductsSerializer(source='product', read_only=True)
    options = DepositOptionsSerializer(source='*', read_only=True)