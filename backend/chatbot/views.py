"""
파일명: chatbot/views.py
설명: AI 챗봇 API 뷰

기능:
    - OpenAI GPT를 활용한 의도 분류 및 응답 생성
    - 다양한 의도 처리 (은행 위치, 상품 검색, 여행 예산, 뉴스, 투자 조언)
    - 카카오맵 API 연동 (은행 위치 검색)
    - 네이버 뉴스 API 연동 (뉴스 검색)

API 엔드포인트:
    - POST /chatbot/chat/ : AI 채팅 메시지 처리

외부 API:
    - OpenAI GPT API: 의도 분류 및 응답 생성
    - Kakao Maps API: 은행 위치 검색
    - Naver News API: 뉴스 검색

의도 분류 카테고리:
    - bank_location: 은행 위치 찾기
    - product_search: 금융 상품 검색
    - travel_budget: 여행 예산 문의
    - news_search: 뉴스 검색
    - investment_advice: 투자 조언
    - general_chat: 일반 대화
"""

import json
import re
import requests
import os
from html import unescape
from django.conf import settings
from django.utils.html import strip_tags
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI

from products.models import DepositProduct, DepositOption, SavingProduct, SavingOption


# OpenAI 클라이언트 초기화
def get_openai_client():
    return OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=getattr(settings, "OPENAI_BASE_URL", None),
    )


# 의도 분류 시스템 프롬프트
INTENT_CLASSIFICATION_PROMPT = """당신은 사용자의 질문을 분류하는 AI입니다.
사용자의 질문을 분석하여 다음 카테고리 중 하나로 분류하세요:

1. "bank_location" - 은행 위치/지점 찾기 (예: "가까운 국민은행", "근처 신한은행 지점", "주변 은행 어디")
2. "product_search" - 금융 상품 검색 (예: "12개월 적금 최고 금리", "예금 추천", "적금 상품")
3. "travel_budget" - 여행 예산/준비 (예: "일본 여행 비용", "태국 여행 얼마", "해외여행 예산")
4. "news_search" - 뉴스/시사 검색 (예: "오늘 증시 뉴스", "해외 증시", "경제 뉴스", "부동산 뉴스")
5. "investment_advice" - 투자/부동산 조언 (예: "지금 집 사는게 좋아?", "주식 투자 어때?", "부동산 전망")
6. "stock_sentiment" - 특정 종목 매수/매도 의견 (예: "삼성전자 사야할까?", "테슬라 팔아야해?", "애플 지금 매수?", "카카오 전망 어때?")
7. "general_chat" - 일반 대화 (예: "오늘 날씨 어때?", "점심 뭐 먹을까", "안녕", 일상적인 대화)

반드시 다음 JSON 형식으로만 응답하세요:
{
  "intent": "카테고리명",
  "entities": {
    "bank_name": "은행명 (있을 경우)",
    "term_months": "기간(개월) (있을 경우, 숫자만)",
    "product_type": "deposit 또는 saving (있을 경우)",
    "destination": "여행지 (있을 경우)",
    "news_topic": "뉴스 주제 (있을 경우)",
    "stock_name": "종목명 (있을 경우, 예: 삼성전자, 테슬라, 애플)",
    "keywords": ["추출된 키워드들"]
  },
  "confidence": 0.0~1.0
}
"""


def classify_intent(user_message: str) -> dict:
    """사용자 메시지의 의도를 분류합니다."""
    client = get_openai_client()

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {"role": "system", "content": INTENT_CLASSIFICATION_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=300,
            temperature=0.1,
        )

        result_text = response.choices[0].message.content.strip()

        # JSON 파싱 시도
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()

        return json.loads(result_text)

    except Exception as e:
        print(f"의도 분류 오류: {e}")
        return {
            "intent": "general_chat",
            "entities": {"keywords": []},
            "confidence": 0.5,
        }


# ==================== 카카오맵 API로 은행 검색 ====================
def search_nearby_bank(bank_name: str, lat: float, lng: float) -> dict:
    """카카오맵 API로 현재 위치에서 가장 가까운 은행을 검색합니다."""
    kakao_api_key = getattr(settings, "KAKAO_REST_API_KEY", None)

    if not kakao_api_key:
        return {"error": "카카오 API 키가 설정되지 않았습니다."}

    try:
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
        params = {
            "query": f"{bank_name} 지점",
            "x": str(lng),
            "y": str(lat),
            "radius": 5000,  # 5km 반경
            "sort": "distance",  # 거리순 정렬
            "size": 5,
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            documents = data.get("documents", [])

            if documents:
                nearest = documents[0]
                return {
                    "found": True,
                    "place_name": nearest.get("place_name", ""),
                    "address": nearest.get("address_name", ""),
                    "road_address": nearest.get("road_address_name", ""),
                    "phone": nearest.get("phone", ""),
                    "distance": nearest.get("distance", ""),
                    "lat": float(nearest.get("y", 0)),
                    "lng": float(nearest.get("x", 0)),
                    "place_url": nearest.get("place_url", ""),
                    "all_results": [
                        {
                            "place_name": doc.get("place_name", ""),
                            "address": doc.get("address_name", ""),
                            "distance": doc.get("distance", ""),
                            "lat": float(doc.get("y", 0)),
                            "lng": float(doc.get("x", 0)),
                        }
                        for doc in documents[:3]
                    ],
                }
            else:
                return {
                    "found": False,
                    "message": "주변에 해당 은행을 찾을 수 없습니다.",
                }
        else:
            return {"error": f"카카오 API 오류: {response.status_code}"}

    except Exception as e:
        print(f"카카오맵 검색 오류: {e}")
        return {"error": str(e)}


def generate_bank_location_response(entities: dict, user_location: dict = None) -> dict:
    """은행 위치 관련 응답을 생성합니다."""
    bank_name = entities.get("bank_name", "")
    keywords = entities.get("keywords", [])

    # 은행명 추출
    bank_keywords = [
        "국민은행",
        "신한은행",
        "우리은행",
        "하나은행",
        "농협",
        "기업은행",
        "SC제일은행",
        "씨티은행",
    ]
    detected_bank = bank_name

    if not detected_bank:
        for kw in keywords:
            for bank in bank_keywords:
                if bank in kw or kw in bank:
                    detected_bank = bank
                    break
            if detected_bank:
                break

    if not detected_bank:
        for kw in keywords:
            if "은행" in kw or "농협" in kw:
                detected_bank = kw
                break

    # 사용자 위치가 있으면 카카오맵으로 검색
    if user_location and detected_bank:
        lat = user_location.get("lat")
        lng = user_location.get("lng")

        if lat and lng:
            search_result = search_nearby_bank(detected_bank, lat, lng)

            if search_result.get("found"):
                distance_m = int(search_result.get("distance", 0))
                distance_text = (
                    f"{distance_m}m"
                    if distance_m < 1000
                    else f"{distance_m/1000:.1f}km"
                )

                message = f"📍 가장 가까운 {detected_bank}을 찾았어요!\n\n"
                message += f"🏦 **{search_result['place_name']}**\n"
                message += f"📍 {search_result.get('road_address') or search_result.get('address')}\n"
                message += f"📏 현재 위치에서 약 {distance_text}\n"
                if search_result.get("phone"):
                    message += f"📞 {search_result['phone']}\n"

                return {
                    "type": "bank_location",
                    "bank_name": detected_bank,
                    "message": message,
                    "bank_info": search_result,
                    "show_map": True,
                    "map_center": {
                        "lat": search_result["lat"],
                        "lng": search_result["lng"],
                    },
                }
            elif search_result.get("error"):
                # API 키가 없거나 오류인 경우 위치 요청 모드로
                return {
                    "type": "bank_location",
                    "bank_name": detected_bank,
                    "message": f"'{detected_bank}' 지점을 찾으시는군요! 위치 정보를 허용해 주시면 가장 가까운 지점을 찾아드릴게요. 🗺️",
                    "need_location": True,
                    "action": {
                        "type": "request_location",
                        "bank_name": detected_bank,
                    },
                }

    # 위치 정보가 없으면 위치 요청
    return {
        "type": "bank_location",
        "bank_name": detected_bank or "은행",
        "message": f"'{detected_bank or '은행'}' 지점을 찾으시는군요! 위치 정보를 허용해 주시면 가장 가까운 지점을 찾아드릴게요. 🗺️",
        "need_location": True,
        "action": {
            "type": "request_location",
            "bank_name": detected_bank or "",
        },
    }


# ==================== 뉴스 검색 ====================
def search_news(query: str, display: int = 5) -> list:
    """네이버 뉴스 API로 뉴스를 검색합니다."""
    client_id = getattr(settings, "NAVER_CLIENT_ID", None)
    client_secret = getattr(settings, "NAVER_CLIENT_SECRET", None)

    if not client_id or not client_secret:
        return []

    try:
        url = "https://openapi.naver.com/v1/search/news.json"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        }
        params = {
            "query": query,
            "display": display,
            "sort": "date",  # 최신순
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])

            def clean_html(text):
                text = unescape(text or "")
                return strip_tags(text)

            return [
                {
                    "title": clean_html(item.get("title", "")),
                    "description": clean_html(item.get("description", ""))[:150],
                    "link": item.get("link", ""),
                    "pub_date": item.get("pubDate", ""),
                }
                for item in items
            ]
        return []

    except Exception as e:
        print(f"뉴스 검색 오류: {e}")
        return []


def generate_news_response(entities: dict, user_message: str) -> dict:
    """뉴스 검색 결과로 응답을 생성합니다."""
    client = get_openai_client()
    keywords = entities.get("keywords", [])
    news_topic = entities.get("news_topic", "")

    # 검색어 구성
    search_query = news_topic or " ".join(keywords) or "경제 금융"

    # 여러 검색어로 뉴스 검색
    all_news = []
    search_queries = [search_query]

    if "증시" in user_message or "주식" in user_message:
        search_queries.append("증시")
    if "해외" in user_message:
        search_queries.append("해외 증시")
    if "부동산" in user_message:
        search_queries.append("부동산 시장")

    for q in search_queries[:2]:
        news = search_news(q, display=3)
        all_news.extend(news)

    # 중복 제거
    seen_titles = set()
    unique_news = []
    for n in all_news:
        if n["title"] not in seen_titles:
            seen_titles.add(n["title"])
            unique_news.append(n)

    unique_news = unique_news[:5]

    if not unique_news:
        return {
            "type": "news_search",
            "message": "죄송해요, 관련 뉴스를 찾지 못했어요. 다른 키워드로 검색해 보시겠어요? 📰",
            "news": [],
        }

    # AI로 뉴스 요약 생성
    news_summary = "\n".join(
        [f"- {n['title']}: {n['description']}" for n in unique_news[:3]]
    )

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "당신은 금융 뉴스 전문가입니다. 제공된 뉴스를 바탕으로 사용자에게 친절하게 요약해서 알려주세요. 이모지를 적절히 사용하세요.",
                },
                {
                    "role": "user",
                    "content": f"사용자 질문: {user_message}\n\n관련 뉴스:\n{news_summary}\n\n위 뉴스들을 바탕으로 간단히 요약해서 알려주세요.",
                },
            ],
            max_tokens=400,
            temperature=0.7,
        )
        ai_message = response.choices[0].message.content.strip()
    except Exception as e:
        ai_message = f"📰 '{search_query}' 관련 최신 뉴스를 찾았어요!"

    return {
        "type": "news_search",
        "message": ai_message,
        "news": unique_news,
    }


# ==================== 투자/부동산 조언 ====================
def search_youtube(query: str, max_results: int = 3) -> list:
    """유튜브에서 영상을 검색합니다."""
    api_key = getattr(settings, "YOUTUBE_API_KEY", None)
    if not api_key:
        return []

    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": api_key,
            "part": "snippet",
            "type": "video",
            "maxResults": max_results,
            "q": query,
            "relevanceLanguage": "ko",
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [
                {
                    "video_id": item.get("id", {}).get("videoId"),
                    "title": unescape(item.get("snippet", {}).get("title", "")),
                    "thumbnail": item.get("snippet", {})
                    .get("thumbnails", {})
                    .get("medium", {})
                    .get("url", ""),
                    "channel": unescape(item.get("snippet", {}).get("channelTitle", "")),
                    "url": f"https://www.youtube.com/watch?v={item.get('id', {}).get('videoId')}",
                }
                for item in data.get("items", [])
            ]
        return []
    except Exception as e:
        print(f"유튜브 검색 오류: {e}")
        return []


def generate_investment_advice_response(entities: dict, user_message: str) -> dict:
    """투자/부동산 조언 응답을 생성합니다."""
    client = get_openai_client()
    keywords = entities.get("keywords", [])

    # 뉴스 검색
    news_queries = []
    if "집" in user_message or "부동산" in user_message or "아파트" in user_message:
        news_queries = ["부동산 시장 전망", "아파트 매매"]
    elif "주식" in user_message or "투자" in user_message:
        news_queries = ["주식 시장 전망", "투자 전략"]
    else:
        news_queries = ["부동산 전망", "경제 전망"]

    all_news = []
    for q in news_queries:
        news = search_news(q, display=3)
        all_news.extend(news)
    all_news = all_news[:4]

    # 유튜브 검색
    youtube_query = (
        "부동산 전망 2025"
        if "집" in user_message or "부동산" in user_message
        else "투자 전략 2025"
    )
    youtube_videos = search_youtube(youtube_query, max_results=3)

    # 뉴스 요약
    news_summary = ""
    if all_news:
        news_summary = "최근 관련 뉴스:\n" + "\n".join(
            [f"- {n['title']}" for n in all_news[:3]]
        )

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {
                    "role": "system",
                    "content": """당신은 금융 전문가입니다. 사용자의 투자/부동산 관련 질문에 대해:
1. 현재 시장 상황을 객관적으로 설명하세요
2. 장단점을 균형있게 제시하세요
3. "투자는 본인의 판단"이라는 점을 언급하세요
4. 이모지를 적절히 사용하세요
5. 최근 뉴스 트렌드를 참고하세요""",
                },
                {
                    "role": "user",
                    "content": f"사용자 질문: {user_message}\n\n{news_summary}\n\n이 정보를 바탕으로 조언해주세요.",
                },
            ],
            max_tokens=600,
            temperature=0.7,
        )
        ai_message = response.choices[0].message.content.strip()
    except Exception as e:
        ai_message = "투자에 대한 조언을 드리기 어렵습니다. 전문가와 상담해 보시는 것을 추천드려요."

    return {
        "type": "investment_advice",
        "message": ai_message,
        "news": all_news,
        "youtube_videos": youtube_videos,
    }


# ==================== 종목 여론 분석 (토스증권 크롤링) ====================
def generate_stock_sentiment_response(entities: dict, user_message: str) -> dict:
    """
    토스증권 커뮤니티를 크롤링하여 종목에 대한 여론을 분석하고
    매수/매도 의견을 제시합니다.
    """
    from .toss_crawler import fetch_toss_comments, analyze_stock_sentiment
    
    client = get_openai_client()
    stock_name = entities.get("stock_name", "")
    keywords = entities.get("keywords", [])
    
    # 종목명 추출
    if not stock_name:
        # 키워드에서 종목명 추출 시도
        for kw in keywords:
            if kw and len(kw) >= 2:
                stock_name = kw
                break
    
    if not stock_name:
        return {
            "type": "stock_sentiment",
            "message": "어떤 종목에 대해 분석해 드릴까요? 종목명을 말씀해 주세요! 📊\n\n예: '삼성전자 사야할까?', '테슬라 전망 어때?'",
            "need_stock_name": True
        }
    
    # 사용자에게 분석 중임을 알리기 위한 초기 응답 (실제로는 크롤링 후 반환)
    print(f"[종목 분석] 분석 시작: {stock_name}")
    
    # 1. 토스증권 커뮤니티 크롤링
    crawl_result = fetch_toss_comments(stock_name, limit=20, max_scroll=5)
    
    if not crawl_result.get("success"):
        # 크롤링 실패 시 뉴스와 AI 의견으로 대체
        error_msg = crawl_result.get("error", "크롤링에 실패했습니다.")
        print(f"[종목 분석] 크롤링 실패: {error_msg}")
        
        # 뉴스로 대체 분석
        news = search_news(f"{stock_name} 주식", display=5)
        youtube_videos = search_youtube(f"{stock_name} 주식 분석", max_results=3)
        
        # AI로 뉴스 기반 분석
        news_summary = "\n".join([f"- {n['title']}" for n in news[:5]]) if news else "관련 뉴스 없음"
        
        try:
            response = client.chat.completions.create(
                model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 주식 투자 전문가입니다. 
뉴스를 바탕으로 종목에 대한 의견을 제시하세요.
매수/매도/보유 중 하나를 추천하되, 투자는 본인 판단이라는 점을 언급하세요."""
                    },
                    {
                        "role": "user",
                        "content": f"종목: {stock_name}\n\n관련 뉴스:\n{news_summary}\n\n이 종목에 대한 의견을 말해주세요."
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            ai_message = response.choices[0].message.content.strip()
        except:
            ai_message = f"'{stock_name}'에 대한 커뮤니티 여론을 수집하지 못했습니다. 관련 뉴스와 영상을 참고해 주세요."
        
        return {
            "type": "stock_sentiment",
            "message": ai_message,
            "stock_name": stock_name,
            "crawling_failed": True,
            "news": news,
            "youtube_videos": youtube_videos,
            "recommendation": "보유",
            "confidence": 30,
            "comments_count": 0,
            "analysis": "커뮤니티 데이터를 수집하지 못해 뉴스 기반으로 분석했습니다."
        }
    
    # 2. 댓글 감성 분석
    comments = crawl_result.get("comments", [])
    analysis = analyze_stock_sentiment(comments, stock_name, client)
    
    # 3. 관련 뉴스 검색
    news = search_news(f"{stock_name} 주식", display=5)
    
    # 4. 관련 유튜브 검색
    youtube_videos = search_youtube(f"{stock_name} 주식 분석", max_results=3)
    
    # 5. 종합 응답 생성
    sentiment_emoji = {
        "positive": "📈",
        "negative": "📉",
        "neutral": "➖"
    }
    
    recommendation_text = {
        "buy": "매수 🟢",
        "sell": "매도 🔴",
        "hold": "보유 🟡"
    }
    
    sentiment = analysis.get("sentiment", "neutral")
    recommendation = analysis.get("recommendation", "hold")
    confidence = analysis.get("confidence", 0.5)
    summary = analysis.get("summary", "")
    key_opinions = analysis.get("key_opinions", [])
    
    # 추천 텍스트 한글 매핑
    recommendation_korean = {
        "buy": "매수",
        "sell": "매도",
        "hold": "보유"
    }
    
    # 메시지 생성
    message = f"""## {stock_name} 여론 분석 결과 {sentiment_emoji.get(sentiment, '📊')}

### 📊 AI 추천: {recommendation_text.get(recommendation, '보유 🟡')}
**신뢰도**: {int(confidence * 100)}%

### 💬 커뮤니티 여론 요약
{summary}

"""
    
    if key_opinions:
        message += "### 🔍 주요 의견\n"
        for i, opinion in enumerate(key_opinions[:3], 1):
            message += f"{i}. {opinion}\n"
        message += "\n"
    
    if analysis.get("positive_points"):
        message += "**✅ 긍정적 요소**: " + ", ".join(analysis["positive_points"][:3]) + "\n"
    
    if analysis.get("negative_points"):
        message += "**⚠️ 부정적 요소**: " + ", ".join(analysis["negative_points"][:3]) + "\n"
    
    message += "\n---\n⚠️ *본 분석은 투자자 커뮤니티 여론을 AI가 분석한 것으로, 투자 판단은 본인의 책임입니다.*"
    
    return {
        "type": "stock_sentiment",
        "message": message,
        "stock_name": stock_name,
        "stock_code": crawl_result.get("stock_code"),
        "comments_count": len(comments),
        "recommendation": recommendation_korean.get(recommendation, "보유"),
        "confidence": int(confidence * 100),
        "analysis": summary,
        "news": news,
        "youtube_videos": youtube_videos
    }


# ==================== 금융 상품 검색 ====================
def search_products(entities: dict) -> dict:
    """금융 상품을 검색합니다."""
    term_months = entities.get("term_months")
    product_type = entities.get("product_type", "").lower()

    results = {"deposits": [], "savings": [], "best_deposit": None, "best_saving": None}

    term = None
    if term_months:
        try:
            term = int(re.sub(r"[^0-9]", "", str(term_months)))
        except ValueError:
            pass

    # 적금 검색
    if not product_type or product_type in ["saving", "적금"]:
        saving_query = SavingOption.objects.select_related("product")
        if term:
            saving_query = saving_query.filter(save_trm=term)

        saving_opts = saving_query.order_by("-intr_rate2")[:10]

        for opt in saving_opts:
            results["savings"].append(
                {
                    "type": "적금",
                    "bank": opt.product.kor_co_nm,
                    "name": opt.product.fin_prdt_nm,
                    "term": opt.save_trm,
                    "base_rate": float(opt.intr_rate),
                    "max_rate": float(opt.intr_rate2),
                    "product_id": opt.product.id,
                    "fin_prdt_cd": opt.product.fin_prdt_cd,
                }
            )

        if saving_opts.exists():
            best = saving_opts.first()
            results["best_saving"] = {
                "type": "적금",
                "bank": best.product.kor_co_nm,
                "name": best.product.fin_prdt_nm,
                "term": best.save_trm,
                "base_rate": float(best.intr_rate),
                "max_rate": float(best.intr_rate2),
                "product_id": best.product.id,
            }

    # 예금 검색
    if not product_type or product_type in ["deposit", "예금"]:
        deposit_query = DepositOption.objects.select_related("product")
        if term:
            deposit_query = deposit_query.filter(save_trm=term)

        deposit_opts = deposit_query.order_by("-intr_rate2")[:10]

        for opt in deposit_opts:
            results["deposits"].append(
                {
                    "type": "예금",
                    "bank": opt.product.kor_co_nm,
                    "name": opt.product.fin_prdt_nm,
                    "term": opt.save_trm,
                    "base_rate": float(opt.intr_rate),
                    "max_rate": float(opt.intr_rate2),
                    "product_id": opt.product.id,
                    "fin_prdt_cd": opt.product.fin_prdt_cd,
                }
            )

        if deposit_opts.exists():
            best = deposit_opts.first()
            results["best_deposit"] = {
                "type": "예금",
                "bank": best.product.kor_co_nm,
                "name": best.product.fin_prdt_nm,
                "term": best.save_trm,
                "base_rate": float(best.intr_rate),
                "max_rate": float(best.intr_rate2),
                "product_id": best.product.id,
            }

    return results


def generate_product_response(entities: dict, search_results: dict) -> dict:
    """금융 상품 검색 결과로 응답을 생성합니다."""
    client = get_openai_client()

    term = entities.get("term_months", "")
    product_type = entities.get("product_type", "")

    best_saving = search_results.get("best_saving")
    best_deposit = search_results.get("best_deposit")

    product_info = ""
    if best_saving:
        product_info += f"""
[적금 최고 금리 상품]
- 은행: {best_saving['bank']}
- 상품명: {best_saving['name']}
- 기간: {best_saving['term']}개월
- 최고금리: {best_saving['max_rate']}%
"""

    if best_deposit:
        product_info += f"""
[예금 최고 금리 상품]
- 은행: {best_deposit['bank']}
- 상품명: {best_deposit['name']}
- 기간: {best_deposit['term']}개월
- 최고금리: {best_deposit['max_rate']}%
"""

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "당신은 친절한 금융 상담사입니다. 제공된 상품 정보를 바탕으로 사용자에게 친근하고 이해하기 쉽게 설명해주세요. 이모지를 적절히 사용하세요.",
                },
                {
                    "role": "user",
                    "content": f"사용자 질문: {term}개월 {product_type or '예적금'} 상품 추천\n\n검색 결과:\n{product_info}",
                },
            ],
            max_tokens=500,
            temperature=0.7,
        )
        ai_message = response.choices[0].message.content.strip()
    except Exception as e:
        ai_message = f"금융 상품을 검색했습니다. {product_info}"

    return {
        "type": "product_search",
        "message": ai_message,
        "products": {
            "best_saving": best_saving,
            "best_deposit": best_deposit,
            "savings": search_results.get("savings", [])[:5],
            "deposits": search_results.get("deposits", [])[:5],
        },
        "action": {"type": "view_products", "link": "/products"},
    }


# ==================== 여행 예산 ====================
def search_youtube_for_travel(destination: str) -> list:
    """유튜브에서 여행 관련 정보를 검색합니다."""
    api_key = getattr(settings, "YOUTUBE_API_KEY", None)
    if not api_key:
        return []

    search_queries = [
        f"{destination} 여행 비용",
        f"{destination} 여행 예산",
        f"{destination} 호캉스",
    ]

    all_videos = []
    seen_ids = set()

    for query in search_queries[:2]:
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "key": api_key,
                "part": "snippet",
                "type": "video",
                "maxResults": 4,
                "q": query,
                "relevanceLanguage": "ko",
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    video_id = item.get("id", {}).get("videoId")
                    if video_id and video_id not in seen_ids:
                        seen_ids.add(video_id)
                        snippet = item.get("snippet", {})
                        all_videos.append(
                            {
                                "video_id": video_id,
                                "title": unescape(snippet.get("title", "")),
                                "thumbnail": snippet.get("thumbnails", {})
                                .get("medium", {})
                                .get("url", ""),
                                "channel": unescape(snippet.get("channelTitle", "")),
                                "url": f"https://www.youtube.com/watch?v={video_id}",
                            }
                        )
        except Exception as e:
            print(f"유튜브 검색 오류: {e}")

    return all_videos[:6]


def generate_travel_response(entities: dict, youtube_results: list) -> dict:
    """여행 예산 관련 응답을 생성합니다."""
    client = get_openai_client()
    destination = entities.get("destination", "")
    keywords = entities.get("keywords", [])

    if not destination:
        travel_keywords = [
            "일본",
            "태국",
            "베트남",
            "미국",
            "유럽",
            "중국",
            "대만",
            "홍콩",
            "싱가포르",
            "호주",
        ]
        for kw in keywords:
            for tk in travel_keywords:
                if tk in kw:
                    destination = tk
                    break

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {
                    "role": "system",
                    "content": """당신은 여행 전문가이자 금융 상담사입니다. 
여행 예산에 대해 물어보면:
1. 대략적인 예산 범위를 알려주세요 (항공, 숙박, 식비, 기타)
2. 호캉스/럭셔리 여행의 경우 더 높은 예산을 제시하세요
3. 적금을 통한 여행 자금 마련 팁도 제공하세요
4. 이모지를 사용해서 친근하게 설명하세요""",
                },
                {
                    "role": "user",
                    "content": f"{destination or '해외'} 여행 예산과 준비에 대해 알려주세요.",
                },
            ],
            max_tokens=600,
            temperature=0.7,
        )
        ai_message = response.choices[0].message.content.strip()
    except Exception as e:
        ai_message = f"{destination or '해외'} 여행을 계획하고 계시군요! 여행 예산은 스타일에 따라 달라질 수 있어요."

    return {
        "type": "travel_budget",
        "destination": destination,
        "message": ai_message,
        "youtube_videos": youtube_results,
        "action": {"type": "view_analysis", "link": "/analysis"},
    }


# ==================== 일반 대화 (LLM 직접 응답) ====================
def generate_general_chat_response(user_message: str) -> dict:
    """일반적인 대화에 대해 LLM이 직접 응답합니다."""
    client = get_openai_client()

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {
                    "role": "system",
                    "content": """당신의 이름은 "핑프"이고, F!NK 금융 서비스의 친근한 AI 챗봇입니다.
사용자와 자연스럽게 대화하세요. 일상적인 질문(날씨, 음식, 인사 등)에도 친절하게 답변합니다.

성격:
- 친근하고 유머러스함
- 이모지를 적절히 사용
- 금융 관련 질문이면 F!NK 기능을 자연스럽게 안내

F!NK 기능:
- 예금/적금 상품 비교
- AI 맞춤 금융 분석
- 은행 지점 찾기
- 금융 뉴스
- 환율/금시세 정보""",
                },
                {"role": "user", "content": user_message},
            ],
            max_tokens=500,
            temperature=0.8,
        )
        ai_message = response.choices[0].message.content.strip()
    except Exception as e:
        ai_message = "음... 잠깐 생각이 멈췄어요! 😅 다시 한번 말씀해 주시겠어요?"

    return {
        "type": "general_chat",
        "message": ai_message,
    }


# ==================== 메인 API ====================
@api_view(["POST"])
@permission_classes([AllowAny])
def chat(request):
    """
    챗봇 메인 엔드포인트
    """
    user_message = request.data.get("message", "").strip()
    user_location = request.data.get("location")  # {lat, lng}

    if not user_message:
        return Response(
            {"error": "메시지를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # 1. 의도 분류
        intent_result = classify_intent(user_message)
        intent = intent_result.get("intent", "general_chat")
        entities = intent_result.get("entities", {})

        print(f"🤖 의도 분류: {intent}")
        print(f"📦 엔티티: {entities}")

        # 2. 의도별 처리
        if intent == "bank_location":
            response_data = generate_bank_location_response(entities, user_location)

        elif intent == "product_search":
            search_results = search_products(entities)
            response_data = generate_product_response(entities, search_results)

        elif intent == "travel_budget":
            destination = entities.get("destination", "")
            if not destination:
                for kw in entities.get("keywords", []):
                    if kw in [
                        "일본",
                        "태국",
                        "베트남",
                        "미국",
                        "유럽",
                        "중국",
                        "대만",
                        "홍콩",
                        "싱가포르",
                        "호주",
                    ]:
                        destination = kw
                        break
            youtube_results = search_youtube_for_travel(destination or "해외")
            response_data = generate_travel_response(entities, youtube_results)

        elif intent == "news_search":
            response_data = generate_news_response(entities, user_message)

        elif intent == "investment_advice":
            response_data = generate_investment_advice_response(entities, user_message)

        elif intent == "stock_sentiment":
            response_data = generate_stock_sentiment_response(entities, user_message)

        else:  # general_chat
            response_data = generate_general_chat_response(user_message)

        # 공통 필드 추가
        response_data["intent"] = intent
        response_data["original_message"] = user_message

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"❌ 챗봇 오류: {e}")
        import traceback

        traceback.print_exc()

        return Response(
            {
                "type": "error",
                "message": "죄송합니다. 처리 중 오류가 발생했어요. 다시 시도해 주세요. 🙏",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def search_bank_with_location(request):
    """
    위치 정보를 받아 가까운 은행을 검색합니다.
    """
    bank_name = request.data.get("bank_name", "")
    lat = request.data.get("lat")
    lng = request.data.get("lng")

    if not bank_name or not lat or not lng:
        return Response(
            {"error": "은행명과 위치 정보가 필요합니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        result = search_nearby_bank(bank_name, float(lat), float(lng))

        if result.get("found"):
            distance_m = int(result.get("distance", 0))
            distance_text = (
                f"{distance_m}m" if distance_m < 1000 else f"{distance_m/1000:.1f}km"
            )

            message = f"📍 가장 가까운 {bank_name}을 찾았어요!\n\n"
            message += f"🏦 **{result['place_name']}**\n"
            message += f"📍 {result.get('road_address') or result.get('address')}\n"
            message += f"📏 현재 위치에서 약 {distance_text}\n"
            if result.get("phone"):
                message += f"📞 {result['phone']}"

            return Response(
                {
                    "type": "bank_location",
                    "message": message,
                    "bank_info": result,
                    "show_map": True,
                    "map_center": {
                        "lat": result["lat"],
                        "lng": result["lng"],
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "type": "bank_location",
                    "message": f"주변에서 {bank_name}을 찾지 못했어요. 😢 다른 은행을 찾아볼까요?",
                    "found": False,
                },
                status=status.HTTP_200_OK,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def chat_suggestions(request):
    """
    챗봇 추천 질문 목록을 반환합니다.
    """
    suggestions = [
        {
            "category": "금융 상품",
            "questions": [
                "12개월 적금 중 최고 금리 상품은?",
                "6개월 예금 추천해줘",
            ],
        },
        {
            "category": "은행 찾기",
            "questions": [
                "가까운 국민은행 어디야?",
                "근처 신한은행 지점 찾아줘",
            ],
        },
        {
            "category": "뉴스",
            "questions": [
                "오늘 증시 뉴스 알려줘",
                "부동산 뉴스 있어?",
            ],
        },
        {
            "category": "투자 조언",
            "questions": [
                "지금 집 사는게 좋을까?",
                "주식 투자 어떻게 생각해?",
            ],
        },
        {
            "category": "여행",
            "questions": [
                "일본 여행 얼마나 준비해야 해?",
                "태국 호캉스 비용 알려줘",
            ],
        },
        {
            "category": "일상 대화",
            "questions": [
                "오늘 점심 뭐 먹을까?",
                "넌 뭐 할 수 있어?",
            ],
        },
    ]

    return Response({"suggestions": suggestions}, status=status.HTTP_200_OK)
