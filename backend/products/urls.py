from django.contrib import admin
from django.urls import path
from products import views


urlpatterns = [
    path('save/', views.save_deposit_products, name="save_deposit_products"),
    path('deposits/', views.deposit_products, name="deposit_products"),
]
