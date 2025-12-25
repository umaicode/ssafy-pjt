"""
파일명: accounts/serializers.py
설명: 사용자 계정 관련 시리얼라이저

클래스:
    - CustomRegisterSerializer: 회원가입 시리얼라이저 (nickname 필드 추가)
    - CustomUserDetailsSerializer: 사용자 정보 조회/수정 시리얼라이저

사용 위치:
    - dj-rest-auth 회원가입 API (/accounts/registration/)
    - 사용자 정보 API (/accounts/user/)
"""

from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField()

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname')
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname')
        user.save()
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    """
    /accounts/user/ 에서 GET(조회) + PATCH(수정) 둘 다 쓰려고
    nickname을 read_only=False로 둔 버전
    """
    # 기존엔 read_only=True 였는데, PATCH로 수정하려면 read_only 제거/변경 필요
    nickname = serializers.CharField(required=False)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('nickname',)
