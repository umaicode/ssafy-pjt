"""
파일명: recommendations/views.py
설명: AI 금융 상품 추천 API 뷰

기능:
    - 사용자 재무 목표 분석
    - GPT 기반 맞춤형 상품 추천
    - 예금/적금 최적 조합 계산
    - 추천 결과 캐싱

API 엔드포인트:
    - POST /recommendations/analyze/       : 분석 요청 생성
    - GET /recommendations/<id>/result/    : 추천 결과 조회
    - GET /recommendations/history/        : 내 분석 이력

핵심 알고리즘:
    - 후보 상품 점수화 (pick_candidates_scored)
    - 예적금 조합 최적화 (optimize_deposit_saving_combination)
    - 목적별 맞춤 데이터 구성 (build_purpose_specific_data)
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import AnalysisRequest, RecommendationResult, RecommendationCache
from .serializers import AnalysisCreateSerializer, RecommendationResultSerializer

import traceback
import math

from .services import (
    compute_goal_math,
    build_alternative_plans,
    pick_candidates_scored,
    option_to_compact_dict,
    make_cache_key,
    validate_reco_payload,
    optimize_deposit_saving_combination,
    build_smart_alternative_plans,
    build_smart_alternative_plans_with_products,
    build_purpose_specific_data,
)

from .llm import SYSTEM_PROMPT, build_user_prompt, call_gpt_json


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_analysis(request):
    serializer = AnalysisCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    analysis = AnalysisRequest.objects.create(
        user=request.user, **serializer.validated_data
    )

    user_input = {
        "purpose": analysis.purpose,
        "period_months": int(analysis.period_months),
        "target_amount": int(analysis.target_amount),
        "monthly_amount": int(analysis.monthly_amount),
        "current_savings": int(getattr(analysis, "current_savings", 0) or 0),
    }

    scored = pick_candidates_scored(user_input, dep_limit=200, sav_limit=200, top_n=60)

    if not scored:
        return Response(
            {
                "detail": "추천 가능한 후보 상품(옵션)을 찾지 못했습니다. (기간/데이터 범위 확인 필요)"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    candidates = []
    for score, opt, kind, dbg in scored:
        c = option_to_compact_dict(opt, kind)
        c["pre_score"] = round(float(score), 4)
        candidates.append(c)

    cache_key = make_cache_key(user_input, candidates)
    cache = RecommendationCache.objects.filter(cache_key=cache_key).first()

    if cache:
        RecommendationResult.objects.create(
            analysis=analysis,
            summary=cache.payload.get("summary", ""),
            items=cache.payload.get("items", []),
            gpt_raw="",
        )
        return Response({"analysis_id": analysis.id}, status=status.HTTP_201_CREATED)

    try:
        prompt = build_user_prompt(user_input, candidates, top_k=5)
        raw = call_gpt_json(SYSTEM_PROMPT, prompt)

        cleaned = validate_reco_payload(raw, candidates, top_k=5)

        RecommendationCache.objects.create(
            cache_key=cache_key,
            payload={
                "summary": cleaned.get("summary", ""),
                "items": cleaned.get("items", []),
                # (선택) 스키마 확장했다면 저장
                "strategy": cleaned.get("strategy", ""),
                "goal_math": cleaned.get("goal_math", {}),
            },
        )

        RecommendationResult.objects.create(
            analysis=analysis,
            summary=cleaned.get("summary", ""),
            items=cleaned.get("items", []),
            gpt_raw=str(raw)[:5000],
        )

        return Response({"analysis_id": analysis.id}, status=status.HTTP_201_CREATED)

    except Exception as e:
        # GPT API 호출 실패 시 폴백(내부 점수 기반 추천) 처리
        # 개발/디버깅 시에만 traceback 확인 필요

        fallback_items = []
        for score, opt, kind, dbg in scored[:5]:
            fallback_items.append(
                {
                    "kind": kind,
                    "option_id": int(opt.id),
                    "product_id": int(opt.product.id),
                    "fit_score": 0.50,
                    "reason": "LLM 응답 오류로 인해 내부 점수 기반 추천으로 대체되었습니다.",
                }
            )

        RecommendationResult.objects.create(
            analysis=analysis,
            summary="내부 점수 기반으로 목표/기간/조건을 반영해 추천했습니다.",
            items=fallback_items,
            gpt_raw=f"ERROR: {str(e)[:2000]}",
        )

        return Response(
            {
                "analysis_id": analysis.id,
                "warning": "GPT 추천 생성에 실패하여 내부 점수 기반 추천으로 대체되었습니다.",
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_analysis_result(request, analysis_id: int):
    """
    [GET] /api/v1/analysis/<analysis_id>/result/
    items에 product/option 상세 + plan(목표 달성 계산) 포함해서 내려줌
    goal_math(전체 계획) + alternative_plans(기간별 필요 월납입) 포함
    combination_strategy(예금+적금 조합 최적화) 포함
    purpose_specific_data(목적별 분석 데이터) 포함
    """
    analysis = AnalysisRequest.objects.filter(id=analysis_id, user=request.user).first()
    if not analysis or not hasattr(analysis, "result"):
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    result = analysis.result
    stored_items = result.items or []

    deposit_option_ids = [
        it["option_id"] for it in stored_items if it.get("kind") == "deposit"
    ]
    saving_option_ids = [
        it["option_id"] for it in stored_items if it.get("kind") == "saving"
    ]

    from products.models import DepositOption, SavingOption

    deposit_opts = DepositOption.objects.select_related("product").filter(
        id__in=deposit_option_ids
    )
    saving_opts = SavingOption.objects.select_related("product").filter(
        id__in=saving_option_ids
    )

    deposit_map = {opt.id: opt for opt in deposit_opts}
    saving_map = {opt.id: opt for opt in saving_opts}

    # 사용자 입력 값 (정수)
    target = int(analysis.target_amount)
    monthly = int(analysis.monthly_amount)

    enriched_items = []
    for it in stored_items:
        kind = it.get("kind")
        option_id = it.get("option_id")

        opt = None
        if kind == "deposit":
            opt = deposit_map.get(option_id)
        elif kind == "saving":
            opt = saving_map.get(option_id)

        if opt is None:
            enriched_items.append(
                {
                    **it,
                    "detail": None,
                    "plan": None,
                    "missing": True,
                }
            )
            continue

        p = opt.product
        term = int(opt.save_trm)  # 이 추천 옵션의 기간

        # -------------------------
        # plan(추천 카드 하단용 계산)
        # -------------------------
        if kind == "saving":
            # 적금: 월납 기준 계산
            required_monthly = (
                math.ceil(target / term) if (target > 0 and term > 0) else None
            )
            extra_needed = (
                max(0, required_monthly - monthly)
                if (required_monthly is not None)
                else None
            )

            plan = {
                "type": "monthly",
                "term_months": term,
                "required_monthly_amount": required_monthly,
                "extra_needed_per_month": extra_needed,
                "planned_total_amount": monthly * term,
                "shortfall_amount": max(0, target - monthly * term),
                "message": (
                    ""
                    if (required_monthly is None)
                    else (
                        f"{term}개월 목표 달성에는 월 {required_monthly}원 필요"
                        + (
                            f"(현재보다 +{extra_needed}원/월)"
                            if extra_needed and extra_needed > 0
                            else ""
                        )
                    )
                ),
            }

        else:
            # 예금: 일시납 안내 (월납과 성격 다름)
            plan = {
                "type": "lump_sum",
                "term_months": term,
                "required_lump_sum": target if target > 0 else None,
                "message": "예금은 일반적으로 일시납(목돈 예치) 상품입니다. "
                "현재 월납 계획과 성격이 달라 목표금액에 가까운 목돈 예치가 필요합니다.",
            }

        # -------------------------
        # detail(기존 유지)
        # -------------------------
        detail = {
            "kind": kind,
            "option_id": opt.id,
            "product_id": p.id,
            "fin_prdt_cd": p.fin_prdt_cd,
            "bank": p.kor_co_nm,
            "name": p.fin_prdt_nm,
            "join_way": p.join_way,
            "join_member": p.join_member,
            "join_deny": p.join_deny,
            "spcl_cnd": p.spcl_cnd,
            "etc_note": p.etc_note,
            "save_trm": opt.save_trm,
            "intr_rate": opt.intr_rate,
            "intr_rate2": opt.intr_rate2,
            "intr_rate_type_nm": opt.intr_rate_type_nm,
            "rsrv_type": opt.rsrv_type,
            "max_limit": opt.max_limit,
        }

        enriched_items.append(
            {
                "kind": kind,
                "option_id": int(option_id),
                "product_id": int(it.get("product_id") or p.id),
                "fit_score": it.get("fit_score"),
                "reason": it.get("reason"),
                "detail": detail,
                "plan": plan,  # 핵심 추가
            }
        )

    # 전체 계획(사용자 입력 기간 기준)
    user_input = {
        "purpose": analysis.purpose,
        "period_months": analysis.period_months,
        "target_amount": analysis.target_amount,
        "monthly_amount": analysis.monthly_amount,
        "current_savings": getattr(analysis, "current_savings", 0) or 0,
        "housing_type": getattr(analysis, "housing_type", ""),
        "target_region": getattr(analysis, "target_region", ""),
        "target_apartment": getattr(analysis, "target_apartment", ""),
        "apartment_price": getattr(analysis, "apartment_price", 0),
        "travel_destination": getattr(analysis, "travel_destination", ""),
        "travel_country_code": getattr(analysis, "travel_country_code", ""),
        "savings_purpose_detail": getattr(analysis, "savings_purpose_detail", ""),
    }

    # GPT 추천 상품 중 최적 상품 찾기 (적합도 순위 기준)
    # stored_items는 GPT가 적합도 순으로 정렬한 것
    # 전략별 최적 상품 = 추천 상품 중 예금/적금 각각 적합도 1위
    best_deposit_opt = None
    best_deposit_rate = 0
    best_saving_opt = None
    best_saving_rate = 0

    # stored_items(적합도 순) 순서대로 순회하여 예금/적금 각각 첫 번째(=적합도 1위) 찾기
    for it in stored_items:
        kind = it.get("kind")
        option_id = it.get("option_id")

        if kind == "deposit" and best_deposit_opt is None:
            opt = deposit_map.get(option_id)
            if opt:
                best_deposit_opt = opt
                best_deposit_rate = float(opt.intr_rate2 or opt.intr_rate or 0)
        elif kind == "saving" and best_saving_opt is None:
            opt = saving_map.get(option_id)
            if opt:
                best_saving_opt = opt
                best_saving_rate = float(opt.intr_rate2 or opt.intr_rate or 0)

        # 둘 다 찾았으면 종료
        if best_deposit_opt and best_saving_opt:
            break

    # goal_math 계산 시 실제 상품 금리 적용
    goal_math = compute_goal_math(
        user_input,
        deposit_rate=best_deposit_rate if best_deposit_rate > 0 else 3.5,
        saving_rate=best_saving_rate if best_saving_rate > 0 else 4.0,
    )

    # 기간 대안표(목표/월납 기준) - 상품 포함된 스마트 대안
    alt_plans = build_smart_alternative_plans_with_products(user_input, goal_math)

    # 기존 대안도 포함 (fallback)
    basic_alt_plans = build_alternative_plans(
        {
            "target_amount": analysis.target_amount,
            "monthly_amount": analysis.monthly_amount,
        }
    )

    # 예금+적금 조합 최적화
    combination_strategy = None
    current_savings = int(user_input.get("current_savings") or 0)

    # 추천 상품 정보 구성
    recommended_deposit = None
    recommended_saving = None

    if best_deposit_opt:
        p = best_deposit_opt.product
        recommended_deposit = {
            "option_id": best_deposit_opt.id,
            "product_id": p.id,
            "fin_prdt_cd": p.fin_prdt_cd,
            "bank": p.kor_co_nm,
            "name": p.fin_prdt_nm,
            "rate": best_deposit_rate,
            "save_trm": best_deposit_opt.save_trm,
        }

    if best_saving_opt:
        p = best_saving_opt.product
        recommended_saving = {
            "option_id": best_saving_opt.id,
            "product_id": p.id,
            "fin_prdt_cd": p.fin_prdt_cd,
            "bank": p.kor_co_nm,
            "name": p.fin_prdt_nm,
            "rate": best_saving_rate,
            "save_trm": best_saving_opt.save_trm,
        }

    # 조합 전략 계산 (보유금 또는 월납입액이 있으면)
    if current_savings > 0 or int(analysis.monthly_amount) > 0:
        # 실제 추천 상품의 가입 기간 가져오기
        deposit_save_trm = best_deposit_opt.save_trm if best_deposit_opt else None
        saving_save_trm = best_saving_opt.save_trm if best_saving_opt else None

        combination_strategy = optimize_deposit_saving_combination(
            current_savings=current_savings,
            monthly_amount=int(analysis.monthly_amount),
            target_amount=int(analysis.target_amount),
            period_months=int(analysis.period_months),
            deposit_rate=best_deposit_rate if best_deposit_rate > 0 else 3.5,
            saving_rate=best_saving_rate if best_saving_rate > 0 else 4.0,
            deposit_save_trm=deposit_save_trm,  # 실제 예금 상품 기간
            saving_save_trm=saving_save_trm,  # 실제 적금 상품 기간
        )

        # 각 전략별로 최적 상품 정보 추가
        for strategy in combination_strategy.get("strategies", []):
            strategy_type = strategy.get("strategy_type", "")

            # 예금을 사용하는 전략
            if strategy.get("uses_deposit"):
                strategy["best_deposit_product"] = recommended_deposit

            # 적금을 사용하는 전략
            if strategy.get("uses_saving"):
                strategy["best_saving_product"] = recommended_saving

        # best_strategy에도 추가
        if combination_strategy.get("best_strategy"):
            best = combination_strategy["best_strategy"]
            if best.get("uses_deposit"):
                best["best_deposit_product"] = recommended_deposit
            if best.get("uses_saving"):
                best["best_saving_product"] = recommended_saving

        # 전체 추천 상품 정보도 추가 (기존 호환)
        combination_strategy["recommended_deposit"] = recommended_deposit
        combination_strategy["recommended_saving"] = recommended_saving

    # 목적별 추가 분석 데이터
    purpose_data = build_purpose_specific_data(user_input, analysis.purpose)

    # 환율 정보 (여행 목적일 때)
    exchange_rate_info = None
    if analysis.purpose == "travel" and user_input.get("travel_country_code"):
        try:
            import requests
            import os
            from datetime import datetime, timedelta

            country_code = user_input.get("travel_country_code")
            print(f"🔍 환율 조회 시도: {country_code}")

            # 한국수출입은행 API 직접 호출
            api_key = os.getenv("EXCHANGE_API_KEY")
            if api_key:
                base_url = (
                    "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
                )
                search_date = datetime.now().strftime("%Y%m%d")

                params = {"authkey": api_key, "searchdate": search_date, "data": "AP01"}

                # 개발 환경에서 verify=False 사용
                res = requests.get(base_url, params=params, timeout=10, verify=False)
                data = res.json() if res.status_code == 200 else []

                # 주말/공휴일인 경우 이전 영업일 조회
                if len(data) == 0:
                    for days_back in range(1, 8):
                        past_date = datetime.now() - timedelta(days=days_back)
                        params["searchdate"] = past_date.strftime("%Y%m%d")
                        res = requests.get(base_url, params=params, timeout=10)
                        data = res.json() if res.status_code == 200 else []
                        if len(data) > 0:
                            search_date = params["searchdate"]
                            break

                # 해당 통화 찾기
                for item in data:
                    cur_unit = item.get("cur_unit", "")
                    if country_code in cur_unit:
                        print(
                            f"환율 찾음: {cur_unit} | {item.get('cur_nm')} | {item.get('deal_bas_r')}"
                        )
                        target_krw = int(analysis.target_amount)
                        deal_bas_r_str = str(item.get("deal_bas_r", "0")).replace(
                            ",", ""
                        )
                        deal_bas_r = float(deal_bas_r_str)

                        # JPY(100) 처리
                        if "JPY" in cur_unit or "(100)" in cur_unit:
                            deal_bas_r = deal_bas_r / 100

                        foreign_amount = round(target_krw / deal_bas_r, 2)

                        # best_strategy에서 계산된 결과 사용
                        best_strategy = combination_strategy.get("best_strategy", {})

                        # best_strategy에서 이미 계산된 값 가져오기
                        total_with_interest = int(best_strategy.get("total_amount", 0))
                        total_interest = int(best_strategy.get("total_interest", 0))
                        strategy_name = best_strategy.get("strategy_name", "")
                        strategy_type = best_strategy.get("strategy_type", "")

                        # 예금/적금 세부 정보
                        deposit_info = best_strategy.get("deposit") or {}
                        saving_info = best_strategy.get("saving") or {}

                        # 예금 정보 (best_strategy에서)
                        deposit_principal = int(deposit_info.get("principal", 0))
                        deposit_interest = int(deposit_info.get("interest", 0))
                        deposit_rate = deposit_info.get("rate", 0)
                        deposit_term = deposit_info.get("term", 0)

                        # 적금 정보 (best_strategy에서)
                        saving_principal = int(saving_info.get("principal", 0))
                        saving_interest = int(saving_info.get("interest", 0))
                        saving_rate = saving_info.get("rate", 0)
                        saving_term = saving_info.get("term", 0)

                        # 총 원금
                        total_principal = deposit_principal + saving_principal

                        # 이자 포함 금액을 현지 통화로 환산
                        foreign_with_interest = (
                            round(total_with_interest / deal_bas_r, 2)
                            if total_with_interest > 0
                            else 0
                        )

                        exchange_rate_info = {
                            "currency_code": cur_unit,
                            "currency_name": item.get("cur_nm", ""),
                            "exchange_rate": deal_bas_r,
                            "target_krw": target_krw,
                            "target_foreign": foreign_amount,
                            "updated_at": search_date,
                            # best_strategy 기반 정보
                            "strategy_name": strategy_name,
                            "strategy_type": strategy_type,
                            # 예금 정보
                            "deposit_principal": deposit_principal,
                            "deposit_interest": deposit_interest,
                            "deposit_rate": deposit_rate,
                            "deposit_term": deposit_term,
                            # 적금 정보
                            "saving_principal": saving_principal,
                            "saving_interest": saving_interest,
                            "saving_rate": saving_rate,
                            "saving_term": saving_term,
                            # 총액
                            "total_principal": total_principal,
                            "total_interest": total_interest,
                            "total_with_interest_krw": total_with_interest,
                            "total_with_interest_foreign": foreign_with_interest,
                        }
                        break

                if not exchange_rate_info:
                    print(f"⚠️ 환율 정보 없음: {country_code}")
            else:
                print("⚠️ EXCHANGE_API_KEY가 설정되지 않았습니다")
        except Exception as e:
            print(f"❌ 환율 정보 조회 실패: {e}")
            import traceback

            traceback.print_exc()

    # 관련 뉴스 (목적별 키워드 기반)
    related_news = []
    search_keywords = purpose_data.get("search_keywords", [])
    try:
        print(f"뉴스 검색 키워드: {search_keywords}")

        if search_keywords:
            # 실시간 네이버 뉴스 API 호출
            import requests
            from django.conf import settings
            from django.utils.html import strip_tags
            from html import unescape

            def clean_html(s):
                s = unescape(s or "")
                return strip_tags(s)

            naver_client_id = getattr(settings, "NAVER_CLIENT_ID", None)
            naver_client_secret = getattr(settings, "NAVER_CLIENT_SECRET", None)

            if naver_client_id and naver_client_secret:
                # 첫 번째 키워드로 검색
                search_query = search_keywords[0]
                print(f"네이버 뉴스 API 호출: {search_query}")

                try:
                    url = "https://openapi.naver.com/v1/search/news.json"
                    headers = {
                        "X-Naver-Client-Id": naver_client_id,
                        "X-Naver-Client-Secret": naver_client_secret,
                    }
                    params = {"query": search_query, "display": 5, "sort": "date"}

                    res = requests.get(url, headers=headers, params=params, timeout=5)
                    if res.status_code == 200:
                        items = res.json().get("items", [])
                        print(f"네이버 뉴스 {len(items)}개 검색됨")

                        related_news = [
                            {
                                "title": clean_html(item.get("title", "")),
                                "link": item.get("link", ""),
                                "description": clean_html(item.get("description", "")),
                                "pubdate": item.get("pubDate", ""),
                            }
                            for item in items
                        ]
                    else:
                        print(f"네이버 뉴스 API 실패: {res.status_code}")
                except Exception as e:
                    print(f"❌ 네이버 뉴스 API 오류: {e}")
            else:
                print("네이버 API 키가 설정되지 않았습니다")
        else:
            print("검색 키워드가 없습니다")
    except Exception as e:
        print(f"❌ 뉴스 정보 조회 실패: {e}")
        import traceback

        traceback.print_exc()

    # 유튜브 검색 (여행 목적일 때)
    # 유튜브 검색 (여행 목적일 때 추천 여행지 탐색)
    related_youtube = []
    recommended_destinations = []  # 유튜브 제목에서 추출한 추천 여행지

    # 여행 목적일 때 전용 유튜브 검색 키워드 사용
    youtube_query = (
        purpose_data.get("youtube_search_keyword")
        if analysis.purpose == "travel"
        else (search_keywords[0] if search_keywords else None)
    )

    if youtube_query:
        try:
            import requests
            import re
            from django.conf import settings

            youtube_api_key = getattr(settings, "YOUTUBE_API_KEY", None)
            if youtube_api_key:
                print(f"유튜브 API 호출: {youtube_query}")

                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    "part": "snippet",
                    "q": youtube_query,
                    "type": "video",
                    "maxResults": 10,  # 추천 여행지 추출을 위해 더 많이 검색
                    "key": youtube_api_key,
                    "relevanceLanguage": "ko",
                }
                res = requests.get(url, params=params, timeout=5)
                if res.status_code == 200:
                    items = res.json().get("items", [])
                    print(f"유튜브 {len(items)}개 검색됨")

                    related_youtube = [
                        {
                            "title": item["snippet"]["title"],
                            "videoId": item["id"]["videoId"],
                            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                            "channelTitle": item["snippet"]["channelTitle"],
                        }
                        for item in items[:5]  # 표시용은 5개만
                    ]

                    # 여행 목적일 때: 유튜브 제목에서 추천 여행지 추출
                    if analysis.purpose == "travel":
                        country_name = purpose_data.get("country_name", "")
                        popular_cities = purpose_data.get("popular_cities", [])

                        # 제외할 단어 목록 (유튜버 이름, 일반 단어 등)
                        exclude_words = {
                            # 일반적인 제외 단어
                            "해외",
                            "국내",
                            "유럽",
                            "아시아",
                            "여행지",
                            "추천",
                            "필수",
                            "해외여행",
                            "국내여행",
                            "해외여행지",
                            "국내여행지",
                            "브이로그",
                            "여행기",
                            "여행자",
                            "유튜브",
                            "채널",
                            "베스트",
                            "인기",
                            "핫플",
                            "명소",
                            "코스",
                            "일정",
                            # 유튜버/인플루언서 관련
                            "곽튜브",
                            "곽튜브가",
                            "서동주",
                            "서동주가",
                            "빠니보틀",
                            "원지",
                            "원지가",
                            "승우아빠",
                            "승우",
                            "침착맨",
                            "풍자",
                            "풍자가",
                            "침튜브",
                            "피식대학",
                            "숏박스",
                            # 동사/형용사 관련
                            "갔다",
                            "다녀",
                            "가봤",
                            "가면",
                            "가는",
                            "갈때",
                            "먹방",
                            "먹을",
                            "맛집",
                            "호텔",
                            "숙소",
                        }

                        # 제목에서 장소명 추출 (간단한 패턴 매칭)
                        extracted_places = set()
                        for item in items:
                            title = item["snippet"]["title"]

                            # 인기 도시가 제목에 포함되어 있으면 추가
                            for city in popular_cities:
                                if city in title:
                                    extracted_places.add(city)

                            # 일반적인 여행지 패턴 매칭 (예: "XX 여행", "XX 추천")
                            place_patterns = re.findall(
                                r"([가-힣]{2,6})\s*(여행|추천|필수|핫플|명소)", title
                            )
                            for place, _ in place_patterns:
                                # 제외 단어가 아니고, 실제 장소처럼 보이는 것만 추가
                                if place not in exclude_words and not any(
                                    ex in place for ex in exclude_words
                                ):
                                    extracted_places.add(place)

                            # 특정 패턴으로 도시명 추출 (예: "도쿄 3박4일", "파리 여행")
                            city_patterns = re.findall(
                                r"([가-힣A-Za-z]{2,10})\s*(\d+박\d+일|\d+일|\d+Days?)",
                                title,
                            )
                            for city, _ in city_patterns:
                                if city not in exclude_words and len(city) <= 6:
                                    extracted_places.add(city)

                        # 인기 도시 우선, 나머지는 뒤에
                        priority_places = [
                            p for p in popular_cities if p in extracted_places
                        ]
                        other_places = [
                            p for p in extracted_places if p not in priority_places
                        ]
                        recommended_destinations = (priority_places + other_places)[:5]
                        print(f"추출된 추천 여행지: {recommended_destinations}")
                else:
                    print(f"유튜브 API 실패: {res.status_code}")
            else:
                print("유튜브 API 키가 설정되지 않았습니다 (YOUTUBE_API_KEY)")
        except Exception as e:
            print(f"❌ 유튜브 검색 실패: {e}")

    # AI 최종 판단 (GPT 요약에서 추출 가능)
    ai_verdict = result.summary  # 기본적으로 요약을 사용

    return Response(
        {
            "summary": result.summary,
            "goal_math": goal_math,
            "alternative_plans": alt_plans if alt_plans else basic_alt_plans,
            "combination_strategy": combination_strategy,
            "purpose_data": purpose_data,
            "exchange_rate_info": exchange_rate_info,
            "related_news": related_news,
            "related_youtube": related_youtube,
            "recommended_destinations": recommended_destinations,  # 추천 여행지 추가
            "ai_verdict": ai_verdict,
            "items": enriched_items,
            "created_at": result.created_at,
        }
    )
