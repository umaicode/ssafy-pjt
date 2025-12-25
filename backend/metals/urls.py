"""
파일명: metals/urls.py
설명: 금/은 현물 시세 API URL 패턴

URL 패턴:
- GET /api/metals/ : 금속 가격 조회
    - Query Params:
        - metal: 'gold' 또는 'silver'
        - start: 시작일 (YYYY-MM-DD)
        - end: 종료일 (YYYY-MM-DD)

데이터 출처: 외부 금속 시세 API
"""

from django.urls import path
from . import views


urlpatterns = [
    # 금/은 가격 데이터 조회
    path("", views.metal_prices, name="metal_prices"),
]