from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404

from .models import Article, Comment
from .serializers import (
    ArticleListSerializer,
    ArticleSerializer,
    ArticleCreateSerializer,
    CommentSerializer,
)

# --------------------------------------------------
# 게시글 목록 / 생성
# GET    /api/v1/articles/
# POST   /api/v1/articles/
# --------------------------------------------------
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------
# 게시글 상세 / 삭제 / 수정
# GET    /api/v1/articles/<article_pk>/
# DELETE /api/v1/articles/<article_pk>/
# PATCH  /api/v1/articles/<article_pk>/
# --------------------------------------------------
@api_view(['GET', 'DELETE', 'PATCH'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



# --------------------------------------------------
# 댓글 목록 (게시글 기준)
# GET /api/v1/articles/<article_pk>/comments/
# --------------------------------------------------
@api_view(['GET'])
def comment_list(request, article_pk):
    # 게시글 존재 여부도 같이 보장
    get_object_or_404(Article, pk=article_pk)

    comments = Comment.objects.filter(article_id=article_pk)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


# --------------------------------------------------
# 댓글 단건 (조회 / 수정 / 삭제)
# GET    /api/v1/comments/<comment_pk>/
# PUT    /api/v1/comments/<comment_pk>/
# DELETE /api/v1/comments/<comment_pk>/
# --------------------------------------------------
@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------------------------------
# 댓글 생성
# POST /api/v1/articles/<article_pk>/comments/create/
# --------------------------------------------------
@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(article=article)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
