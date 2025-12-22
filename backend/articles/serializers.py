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
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author_nickname', 'created_at', 'updated_at',"likes_count", "is_liked")
        read_only_fields = ('id', 'author_nickname', 'created_at', 'updated_at')
    def get_likes_count(self, obj):
        return obj.like_users.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        # ✅ request가 없거나 로그인 안 했으면 False
        if not request or not request.user.is_authenticated:
            return False
        # ✅ 로그인 했으면 내가 좋아요 눌렀는지 체크
        return obj.like_users.filter(pk=request.user.pk).exists()


# 게시글 상세 조회용 (GET)
class ArticleSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'views',
            'author_nickname', 'created_at', 'updated_at',
            'comment_set', 'comments_count', "likes_count", "is_liked"
        ) 
        read_only_fields = ("user",)

    def get_comments_count(self, obj):
        return obj.comment_set.count()
    def get_likes_count(self, obj):
        return obj.like_users.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return obj.like_users.filter(pk=request.user.pk).exists()

# 게시글 목록용
class ArticleListSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'author_nickname', 'views', 'created_at', 'comments_count')

    def get_comments_count(self, obj):
        return obj.comment_set.count()
