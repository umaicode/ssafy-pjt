from django.urls import path
from . import views


urlpatterns = [
    path("", views.news_list, name="news_list"),
    path("fetch/", views.fetch_news, name="fetch_news"),
    path("<int:pk>/", views.news_detail, name="news_detail"),
    path("<int:pk>/bookmark/", views.toggle_bookmark, name="toggle_bookmark",),
]