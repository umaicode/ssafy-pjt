"""
파일명: exchange/serializers.py
설명: 환율 시리얼라이저

클래스:
    - ExchangeRateSerializer: 환율 정보 시리얼라이저

필드:
    - cur_unit: 통화 코드 (USD, EUR, JPY 등)
    - cur_nm: 통화명
    - ttb: 송금 받을 때 환율
    - tts: 송금 보낼 때 환율
    - deal_bas_r: 매매 기준율
"""

from rest_framework import serializers
from .models import ExchangeRate


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = "__all__"
