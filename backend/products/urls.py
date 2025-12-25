"""
파일명: products/urls.py
설명: 금융 상품 API URL 패턴

URL 패턴:
- POST /api/products/save-deposits/ : 예금 상품 데이터 저장 (금감원 API → DB)
- GET /api/products/deposits/ : 예금 상품 목록 조회
- POST /api/products/save-savings/ : 적금 상품 데이터 저장 (금감원 API → DB)
- GET /api/products/savings/ : 적금 상품 목록 조회
- GET /api/products/deposit/<fin_prdt_cd>/ : 예금 상품 상세 조회
- GET /api/products/saving/<fin_prdt_cd>/ : 적금 상품 상세 조회
- POST /api/products/likes/toggle/ : 좋아요 토글
- GET /api/products/likes/me/ : 내 좋아요 목록
"""

from django.urls import path
from products import views


urlpatterns = [
    # ========================================
    # 예금 상품
    # ========================================
    path("save-deposits/", views.save_deposit_products, name="save_deposit_products"),
    path("deposits/", views.deposit_products, name="deposit_products"),
    path("deposit/<str:fin_prdt_cd>/", views.deposit_product_detail),
    
    # ========================================
    # 적금 상품
    # ========================================
    path("save-savings/", views.save_saving_products, name="save_saving_products"),
    path("savings/", views.saving_products, name="saving_products"),
    path("saving/<str:fin_prdt_cd>/", views.saving_product_detail),
    
    # ========================================
    # 좋아요 기능
    # ========================================
    path("likes/toggle/", views.toggle_like),
    path("likes/me/", views.my_likes),
]
