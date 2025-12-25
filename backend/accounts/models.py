from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """
    Custom User 모델.

    설계 의도:
    - AbstractUser를 확장해 nickname, bookmark 등 프로젝트 전용 필드를 추가한다.
    - nickname은 UI 표시용이므로 '공백만 입력' 같은 케이스는 serializer에서 엄격히 막는다.
    """
    nickname = models.CharField(max_length=30, blank=True)
    bookmarked_news = models.ManyToManyField(
        "news.News", related_name="bookmarked_by", blank=True
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    income_range = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
