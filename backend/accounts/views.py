from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['PATCH'])
def update_user(request):
    user = request.user
    data = request.data

    # 닉네임변경
    nickname = data.get('nickname')
    if nickname is not None:
        nickname = nickname.strip()
        if not nickname:
            return Response(
                {"nickname": ["닉네임은 비어 있을 수 없습니다."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.nickname = nickname

    # 2️비밀번호 변경
    old_password = data.get('old_password')
    new_password1 = data.get('new_password1')
    new_password2 = data.get('new_password2')

    # 비밀번호 관련 필드가 하나라도 오면 → 비밀번호 변경 로직 실행
    if old_password or new_password1 or new_password2:
        # 필수 필드 체크
        if not all([old_password, new_password1, new_password2]):
            return Response(
                {"password": ["비밀번호 변경에는 모든 필드가 필요합니다."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 현재 비밀번호 검증
        if not user.check_password(old_password):
            return Response(
                {"old_password": ["현재 비밀번호가 올바르지 않습니다."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 새 비밀번호 일치 확인
        if new_password1 != new_password2:
            return Response(
                {"new_password": ["새 비밀번호가 서로 일치하지 않습니다."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호 변경 (중요: set_password 사용)
        user.set_password(new_password1)
        
    user.save()

    return Response(
        {
            "nickname": user.nickname,
            "detail": "회원정보가 수정되었습니다."
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def delete(request):
    request.user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

