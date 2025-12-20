from django.urls import path
from . import views


urlpatterns = [
    path("", views.metal_prices, name="metal_prices"),
]