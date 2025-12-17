from rest_framework import serializers
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption

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