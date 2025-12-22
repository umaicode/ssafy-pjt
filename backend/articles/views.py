from rest_framework.decorators import api_view
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

        # 페이지네이션 적용
        paginator = ArticlePagination()
        paginated = paginator.paginate_queryset(articles, request)
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

        serializer = ArticleSerializer(article)
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

        # 수정 후 전체 데이터 반환
        return Response(ArticleSerializer(article).data)


# --------------------------------------------------
# 댓글 목록 (게시글 기준)
# GET /api/v1/articles/<article_pk>/comments/
# --------------------------------------------------
@api_view(["GET"])
def comment_list(request, article_pk):
    get_object_or_404(Article, pk=article_pk)
    comments = Comment.objects.filter(article_id=article_pk).order_by("-created_at")
    serializer = CommentSerializer(comments, many=True)
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
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == "PATCH":
        # 작성자만 수정 가능
        if comment.user != request.user:
            return Response(
                {"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = CommentSerializer(comment, data=request.data, partial=True)
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
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(article=article, user=request.user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
