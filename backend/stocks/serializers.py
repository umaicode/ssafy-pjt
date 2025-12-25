from rest_framework import serializers


class StockSearchSerializer(serializers.Serializer):
    """주식 검색 결과용 시리얼라이저"""
    symbol = serializers.CharField()
    name = serializers.CharField()
    exchange = serializers.CharField(required=False, allow_null=True)
    type = serializers.CharField(required=False, allow_null=True)


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


class StockChartDataSerializer(serializers.Serializer):
    """주식 차트 데이터용 시리얼라이저"""
    date = serializers.DateTimeField()
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    close = serializers.FloatField()
    volume = serializers.IntegerField()


class StockChartResponseSerializer(serializers.Serializer):
    """주식 차트 응답용 시리얼라이저"""
    symbol = serializers.CharField()
    period = serializers.CharField()
    interval = serializers.CharField()
    data = StockChartDataSerializer(many=True)


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
    name = serializers.CharField()
    current_price = serializers.FloatField(required=False, allow_null=True)
    change = serializers.FloatField(required=False, allow_null=True)
    change_percent = serializers.FloatField(required=False, allow_null=True)
    market = serializers.CharField()  # 'KR' or 'US'
