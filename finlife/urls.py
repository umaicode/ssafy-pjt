from django.contrib import admin
from django.urls import path
from finlife import views


urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-products-options/<str:fin_prdt_cd>/', views.deposit_options),
    path('deposit-products/top-rate/', views.deposit_top_rate),
]
