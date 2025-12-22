from django.urls import path
from . import  views

urlpatterns = [
    # 회원 탈퇴 URL 추가
    path('delete/', views.delete, name='account_delete'),
    path('update/', views.update_user, name='account_update')
]
