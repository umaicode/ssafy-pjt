from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = "__all__"

    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user.bookmarked_news.filter(pk=obj.pk).exists()
        return False
