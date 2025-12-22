from django.db import models
from django.conf import settings


# Create your models here.
class News(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="news"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField()
    pubDate = models.CharField(max_length=50)

    class Meta:
        unique_together = ["user", "title"]  # 사용자별로 동일한 제목의 뉴스는 하나만
