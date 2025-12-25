"""
파일명: accounts/urls.py
설명: 사용자 계정 관련 URL 패턴

URL 패턴:
- DELETE /accounts/delete/ : 회원 탈퇴
- PATCH /accounts/update/ : 회원정보 수정
"""

from django.urls import path
from . import views

urlpatterns = [
    # 회원 탈퇴
    path('delete/', views.delete, name='account_delete'),
    # 회원정보 수정 (닉네임, 비밀번호)
    path('update/', views.update_user, name='account_update')
]
