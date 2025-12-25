"""
파일명: accounts/views.py
설명: 사용자 계정 관련 API 뷰

API 엔드포인트:
- PATCH /accounts/update/ : 회원정보 수정 (닉네임, 비밀번호)
- DELETE /accounts/delete/ : 회원 탈퇴
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    회원정보 수정 API
    
    사용자의 닉네임 또는 비밀번호를 수정합니다.
    
    Request Body:
        - nickname (str, optional): 변경할 닉네임
        - old_password (str, optional): 현재 비밀번호 (비밀번호 변경 시 필수)
        - new_password1 (str, optional): 새 비밀번호
        - new_password2 (str, optional): 새 비밀번호 확인
        
    Returns:
        200: 수정 성공
        400: 유효성 검사 실패
    """
    user = request.user
    data = request.data

    # ========================================
    # 닉네임 변경
    # ========================================
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

    # ========================================
    # 비밀번호 변경
    # ========================================
    old_password = data.get('old_password')
    new_password1 = data.get('new_password1')
    new_password2 = data.get('new_password2')

    # 비밀번호 관련 필드가 하나라도 오면 비밀번호 변경 로직 실행
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

        # 비밀번호 변경 (중요: set_password로 해싱 처리)
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
@permission_classes([IsAuthenticated])
def delete(request):
    """
    회원 탈퇴 API
    
    현재 로그인된 사용자의 계정을 삭제합니다.
    
    Returns:
        204: 삭제 성공 (No Content)
    """
    request.user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

