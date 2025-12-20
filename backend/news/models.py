from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    link = models.URLField()
    pubDate = models.CharField(max_length=50)
    is_bookmarked = models.BooleanField(default=False)