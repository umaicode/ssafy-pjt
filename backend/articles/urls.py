from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:article_pk>/comments/', views.comment_list),
    path('articles/<int:article_pk>/comments/create/', views.comment_create), 
    path('comments/<int:comment_pk>/', views.comment_detail),
    path("articles/<int:article_pk>/like/", views.toggle_article_like),
    path("comments/<int:comment_pk>/like/", views.toggle_comment_like),
]
