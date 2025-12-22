from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Article, Comment
from .serializers import (
    ArticleListSerializer,
    ArticleSerializer,
    ArticleCreateSerializer,
    CommentSerializer,
)


# 페이지네이션 클래스
class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


# --------------------------------------------------
# 게시글 목록 / 생성
# GET    /api/v1/articles/
# POST   /api/v1/articles/
# --------------------------------------------------
@api_view(["GET", "POST"])
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all().order_by("-created_at")

        paginator = ArticlePagination()
        paginated = paginator.paginate_queryset(articles, request)

        # ✅ 목록에서도 (원하면) is_liked 같은 걸 계산하려면 context 넘기는 버전으로 바꿀 수 있음
        # 지금은 목록에서 is_liked 안 쓰는 구조면 그대로 둬도 OK
        serializer = ArticleListSerializer(paginated, many=True)

        return Response(
            {
                "results": serializer.data,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "total_count": paginator.page.paginator.count,
            }
        )

    elif request.method == "POST":
        # ✅ 게시글 작성은 로그인 필요
        # (프론트에서 로그인 체크를 안 하더라도, 서버는 막는 게 정상)
        if not request.user.is_authenticated:
            return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------
# 게시글 상세 / 삭제 / 수정
# GET    /api/v1/articles/<article_pk>/
# DELETE /api/v1/articles/<article_pk>/
# PATCH  /api/v1/articles/<article_pk>/
# --------------------------------------------------
@api_view(["GET", "DELETE", "PATCH"])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == "GET":
        # 조회수 증가
        article.views += 1
        article.save(update_fields=["views"])

        # ✅ is_liked 계산하려면 request context 필수
        serializer = ArticleSerializer(article, context={"request": request})
        return Response(serializer.data)

    elif request.method == "DELETE":
        # 작성자만 삭제 가능
        if article.user != request.user:
            return Response(
                {"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PATCH":
        # 작성자만 수정 가능
        if article.user != request.user:
            return Response(
                {"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = ArticleCreateSerializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # ✅ 수정 후 반환도 context 포함해서 (is_liked/likes_count 등 일관성 유지)
        return Response(ArticleSerializer(article, context={"request": request}).data)


# --------------------------------------------------
# 댓글 목록 (게시글 기준)
# GET /api/v1/articles/<article_pk>/comments/
# --------------------------------------------------
@api_view(["GET"])
def comment_list(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    qs = article.comment_set.all().order_by("-id")

    # ✅ 댓글도 is_liked 계산하려면 request context 필수
    serializer = CommentSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)


# --------------------------------------------------
# 댓글 단건 (조회 / 수정 / 삭제)
# GET    /api/v1/comments/<comment_pk>/
# PATCH  /api/v1/comments/<comment_pk>/
# DELETE /api/v1/comments/<comment_pk>/
# --------------------------------------------------
@api_view(["GET", "PATCH", "DELETE"])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == "GET":
        # ✅ 단건 조회도 context 포함
        serializer = CommentSerializer(comment, context={"request": request})
        return Response(serializer.data)

    elif request.method == "PATCH":
        # 작성자만 수정 가능
        if comment.user != request.user:
            return Response(
                {"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        # 작성자만 삭제 가능
        if comment.user != request.user:
            return Response(
                {"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------------------------------
# 댓글 생성
# POST /api/v1/articles/<article_pk>/comments/create/
# --------------------------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])  # ✅ 댓글 작성은 로그인 필요
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    serializer = CommentSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save(article=article, user=request.user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------
# 게시글 좋아요 토글
# POST /api/v1/articles/<article_pk>/like/
# --------------------------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])  # ✅ 좋아요는 로그인 필요
def toggle_article_like(request, article_pk):
    """
    게시글 좋아요 토글
    - 이미 좋아요면 remove
    - 아니면 add
    응답: liked(현재상태), likes_count
    """
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user

    if article.like_users.filter(pk=user.pk).exists():
        article.like_users.remove(user)
        liked = False
    else:
        article.like_users.add(user)
        liked = True

    return Response(
        {"liked": liked, "likes_count": article.like_users.count()},
        status=status.HTTP_200_OK,
    )


# --------------------------------------------------
# 댓글 좋아요 토글
# POST /api/v1/comments/<comment_pk>/like/
# --------------------------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])  # ✅ 좋아요는 로그인 필요
def toggle_comment_like(request, comment_pk):
    """댓글 좋아요 토글"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user

    if comment.like_users.filter(pk=user.pk).exists():
        comment.like_users.remove(user)
        liked = False
    else:
        comment.like_users.add(user)
        liked = True

    return Response(
        {"liked": liked, "likes_count": comment.like_users.count()},
        status=status.HTTP_200_OK,
    )
