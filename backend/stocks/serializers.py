"""
stocks/serializers.py
주식 관련 시리얼라이저

실제 사용 중인 시리얼라이저만 유지:
- StockDetailSerializer: 종목 상세 정보
- StockNewsSerializer: 종목 뉴스
- PopularStockSerializer: 인기 종목 목록
"""
from rest_framework import serializers


class StockDetailSerializer(serializers.Serializer):
    """주식 상세 정보용 시리얼라이저"""
    symbol = serializers.CharField()
    name = serializers.CharField()
    currency = serializers.CharField(required=False, allow_null=True)
    exchange = serializers.CharField(required=False, allow_null=True)
    market_cap = serializers.IntegerField(required=False, allow_null=True)
    current_price = serializers.FloatField(required=False, allow_null=True)
    previous_close = serializers.FloatField(required=False, allow_null=True)
    open_price = serializers.FloatField(required=False, allow_null=True)
    day_high = serializers.FloatField(required=False, allow_null=True)
    day_low = serializers.FloatField(required=False, allow_null=True)
    volume = serializers.IntegerField(required=False, allow_null=True)
    avg_volume = serializers.IntegerField(required=False, allow_null=True)
    fifty_two_week_high = serializers.FloatField(required=False, allow_null=True)
    fifty_two_week_low = serializers.FloatField(required=False, allow_null=True)
    pe_ratio = serializers.FloatField(required=False, allow_null=True)
    eps = serializers.FloatField(required=False, allow_null=True)
    dividend_yield = serializers.FloatField(required=False, allow_null=True)
    beta = serializers.FloatField(required=False, allow_null=True)
    sector = serializers.CharField(required=False, allow_null=True)
    industry = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    website = serializers.CharField(required=False, allow_null=True)
    logo_url = serializers.CharField(required=False, allow_null=True)
    change = serializers.FloatField(required=False, allow_null=True)
    change_percent = serializers.FloatField(required=False, allow_null=True)


class StockNewsSerializer(serializers.Serializer):
    """주식 뉴스용 시리얼라이저"""
    title = serializers.CharField()
    link = serializers.CharField()
    publisher = serializers.CharField(required=False, allow_null=True)
    published_date = serializers.CharField(required=False, allow_null=True)
    thumbnail = serializers.CharField(required=False, allow_null=True)


class PopularStockSerializer(serializers.Serializer):
    """인기 종목용 시리얼라이저"""
    symbol = serializers.CharField()
    code = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField()
    current_price = serializers.FloatField(required=False, allow_null=True)
    change = serializers.FloatField(required=False, allow_null=True)
    change_percent = serializers.FloatField(required=False, allow_null=True)
    market_cap = serializers.IntegerField(required=False, allow_null=True)
    market = serializers.CharField()  # 'KR' or 'US'
