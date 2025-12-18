from django.urls import path
from . import views

urlpatterns = [
    path("analysis/", views.create_analysis),
    path("analysis/<int:analysis_id>/result/", views.get_analysis_result),
]
