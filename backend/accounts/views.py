
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['PATCH'])
def update_user(request):
    """
    사용자 정보(닉네임, 비밀번호) 수-정 API
    PATCH: /accounts/user
    - 닉네임 변경
    - 비밀번호 변경
    """
    user = request.user  # 현재 인증된 사용자 객체
    data = request.data  # 요청 데이터

    # 1. 닉네임 변경 처리
    nickname = data.get('nickname')
    if nickname is not None:
        nickname = nickname.strip()  # 앞뒤 공백 제거
        if not nickname:
            # 닉네임이 비어 있으면 에러 반환
            return Response(
                {"nickname": ["닉네임은 비어 있을 수 없습니다."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.nickname = nickname  # 닉네임 변경

    # 2. 비밀번호 변경 처리
    # 비밀번호 관련 필드 추출
    old_password = data.get('old_password')
    new_password1 = data.get('new_password1')
    new_password2 = data.get('new_password2')

    # 비밀번호 관련 필드가 하나라도 있으면 비밀번호 변경 로직 실행
    if old_password or new_password1 or new_password2:
        # 2-1. 모든 필드가 입력되었는지 확인
        if not all([old_password, new_password1, new_password2]):
            return Response(
                {"password": ["비밀번호 변경에는 모든 필드가 필요합니다."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2-2. 현재 비밀번호가 올바른지 검증
        if not user.check_password(old_password):
            return Response(
                {"old_password": ["현재 비밀번호가 올바르지 않습니다."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2-3. 새 비밀번호 두 개가 일치하는지 확인
        if new_password1 != new_password2:
            return Response(
                {"new_password": ["새 비밀번호가 서로 일치하지 않습니다."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2-4. 비밀번호 변경 (set_password: 해시 적용)
        user.set_password(new_password1)

    # 3. 변경된 정보 저장
    user.save()

    # 4. 응답 반환
    return Response(
        {
            "nickname": user.nickname,  # 변경된 닉네임
            "detail": "회원정보가 수정되었습니다."
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def delete(request):
    """
    회원 탈퇴(사용자 삭제) API
    DELETE: /accounts/user
    """
    request.user.delete()  # 현재 로그인한 사용자 삭제
    return Response(status=status.HTTP_204_NO_CONTENT)  # 성공 시 204 반환

