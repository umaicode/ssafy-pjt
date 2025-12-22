import requests

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import News
from .serializers import NewsSerializer

# html 처리
from django.utils.html import strip_tags
from html import unescape

# 발행일 처리
from datetime import datetime


# html 엔티티 제거 함수
def clean_naver_html(s: str) -> str:
    s = unescape(s or "")
    s = strip_tags(s)

    return s


# 발행일 포맷 변경 함수
def format_pubdate(pubdate: str) -> str:
    dt = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
    return dt.strftime("%Y-%m-%d %H:%M")


# Create your views here.
@api_view(["POST"])
def fetch_news(request):
    query = request.data.get("query")

    if not query:
        return Response(
            {"detail": "검색어가 필요합니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    url = "https://openapi.naver.com/v1/search/news.json"

    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }

    params = {
        "query": query,
        "display": 20,
        "sort": "date",
    }

    res = requests.get(url, headers=headers, params=params)
    if res.status_code != 200:
        return Response(
            {"detail": "Naver API 호출 실패", "status_code": res.status_code},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    data = res.json()
    items = data.get("items", [])

    created_count = 0
    for item in items:
        title = clean_naver_html(item.get("title", ""))
        description = clean_naver_html(item.get("description", ""))
        link = item.get("link", "")
        pubDate = format_pubdate(item.get("pubDate", ""))

        if not News.objects.filter(title=title).exists():
            News.objects.create(
                title=title,
                link=link,
                description=description,
                pubDate=pubDate,
            )
            created_count += 1

    return Response(
        {
            "message": "뉴스 수집 완료",
            "created": created_count,
            "total_From_naver": len(items),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def news_list(request):
    mode = request.query_params.get("mode")

    news = News.objects.all().order_by("-id")

    if mode == "bookmark":
        news = news.filter(is_bookmarked=True)

    serializer = NewsSerializer(news, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    serializer = NewsSerializer(news)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def toggle_bookmark(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.is_bookmarked = not news.is_bookmarked
    news.save()

    serializer = NewsSerializer(news)

    return Response(serializer.data, status=status.HTTP_200_OK)
