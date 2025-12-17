from django.contrib import admin
from django.urls import path
from products import views


urlpatterns = [
    path('save-deposits/', views.save_deposit_products, name="save_deposit_products"),
    path('deposits/', views.deposit_products, name="deposit_products"),
    path('save-savings/', views.save_saving_products, name="save_saving_products"),
    path('savings/', views.saving_products, name="saving_products"),
]
