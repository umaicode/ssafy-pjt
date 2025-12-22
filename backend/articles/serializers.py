from rest_framework import serializers
from .models import Article, Comment


# 게시글 생성/수정용 (POST, PATCH)
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'content')


# 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author_nickname', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author_nickname', 'created_at', 'updated_at')


# 게시글 상세 조회용 (GET)
class ArticleSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'views',
            'author_nickname', 'created_at', 'updated_at',
            'comment_set', 'comments_count'
        )

    def get_comments_count(self, obj):
        return obj.comment_set.count()


# 게시글 목록용
class ArticleListSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'author_nickname', 'views', 'created_at', 'comments_count')

    def get_comments_count(self, obj):
        return obj.comment_set.count()
