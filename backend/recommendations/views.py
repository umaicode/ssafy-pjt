from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import AnalysisRequest, RecommendationResult, RecommendationCache
from .serializers import AnalysisCreateSerializer, RecommendationResultSerializer

from .services import compute_goal_math, build_alternative_plans

import traceback
import math  # ✅ 추가

from .services import (
    pick_candidates_scored,
    option_to_compact_dict,
    make_cache_key,
    validate_reco_payload,
)

from .llm import SYSTEM_PROMPT, build_user_prompt, call_gpt_json


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_analysis(request):
    serializer = AnalysisCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    analysis = AnalysisRequest.objects.create(
        user=request.user,
        **serializer.validated_data
    )

    user_input = {
        "purpose": analysis.purpose,
        "period_months": int(analysis.period_months),
        "target_amount": int(analysis.target_amount),
        "monthly_amount": int(analysis.monthly_amount),
    }

    scored = pick_candidates_scored(user_input, dep_limit=200, sav_limit=200, top_n=60)

    if not scored:
        return Response(
            {"detail": "추천 가능한 후보 상품(옵션)을 찾지 못했습니다. (기간/데이터 범위 확인 필요)"},
            status=status.HTTP_400_BAD_REQUEST
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
            gpt_raw=""
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
            }
        )

        RecommendationResult.objects.create(
            analysis=analysis,
            summary=cleaned.get("summary", ""),
            items=cleaned.get("items", []),
            gpt_raw=str(raw)[:5000]
        )

        return Response({"analysis_id": analysis.id}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("========== GPT FAILED ==========")
        print("ERROR:", repr(e))
        traceback.print_exc()
        print("================================")

        fallback_items = []
        for score, opt, kind, dbg in scored[:5]:
            fallback_items.append({
                "kind": kind,
                "option_id": int(opt.id),
                "product_id": int(opt.product.id),
                "fit_score": 0.50,
                "reason": "LLM 응답 오류로 인해 내부 점수 기반 추천으로 대체되었습니다."
            })

        RecommendationResult.objects.create(
            analysis=analysis,
            summary="내부 점수 기반으로 목표/기간/조건을 반영해 추천했습니다.",
            items=fallback_items,
            gpt_raw=f"ERROR: {str(e)[:2000]}"
        )

        return Response(
            {
                "analysis_id": analysis.id,
                "warning": "GPT 추천 생성에 실패하여 내부 점수 기반 추천으로 대체되었습니다."
            },
            status=status.HTTP_201_CREATED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_analysis_result(request, analysis_id: int):
    """
    [GET] /api/v1/analysis/<analysis_id>/result/
    ✅ items에 product/option 상세 + plan(목표 달성 계산) 포함해서 내려줌
    ✅ goal_math(전체 계획) + alternative_plans(기간별 필요 월납입) 포함
    """
    analysis = AnalysisRequest.objects.filter(id=analysis_id, user=request.user).first()
    if not analysis or not hasattr(analysis, "result"):
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    result = analysis.result
    stored_items = result.items or []

    deposit_option_ids = [it["option_id"] for it in stored_items if it.get("kind") == "deposit"]
    saving_option_ids  = [it["option_id"] for it in stored_items if it.get("kind") == "saving"]

    from products.models import DepositOption, SavingOption

    deposit_opts = (
        DepositOption.objects
        .select_related("product")
        .filter(id__in=deposit_option_ids)
    )
    saving_opts = (
        SavingOption.objects
        .select_related("product")
        .filter(id__in=saving_option_ids)
    )

    deposit_map = {opt.id: opt for opt in deposit_opts}
    saving_map  = {opt.id: opt for opt in saving_opts}

    # ✅ 사용자 입력 값 (정수)
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
            enriched_items.append({
                **it,
                "detail": None,
                "plan": None,
                "missing": True,
            })
            continue

        p = opt.product
        term = int(opt.save_trm)  # ✅ 이 추천 옵션의 기간

        # -------------------------
        # ✅ plan(추천 카드 하단용 계산)
        # -------------------------
        if kind == "saving":
            # 적금: 월납 기준 계산
            required_monthly = math.ceil(target / term) if (target > 0 and term > 0) else None
            extra_needed = max(0, required_monthly - monthly) if (required_monthly is not None) else None

            plan = {
                "type": "monthly",
                "term_months": term,
                "required_monthly_amount": required_monthly,
                "extra_needed_per_month": extra_needed,
                "planned_total_amount": monthly * term,
                "shortfall_amount": max(0, target - monthly * term),
                "message": "" if (required_monthly is None) else
                    (f"{term}개월 목표 달성에는 월 {required_monthly}원 필요"
                     + (f"(현재보다 +{extra_needed}원/월)" if extra_needed and extra_needed > 0 else "")),
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
        # ✅ detail(기존 유지)
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

        enriched_items.append({
            "kind": kind,
            "option_id": int(option_id),
            "product_id": int(it.get("product_id") or p.id),
            "fit_score": it.get("fit_score"),
            "reason": it.get("reason"),
            "detail": detail,
            "plan": plan,  # ✅ 핵심 추가
        })

    # ✅ 전체 계획(사용자 입력 기간 기준)
    goal_math = compute_goal_math({
        "purpose": analysis.purpose,
        "period_months": analysis.period_months,
        "target_amount": analysis.target_amount,
        "monthly_amount": analysis.monthly_amount,
    })

    # ✅ 기간 대안표(목표/월납 기준)
    alt_plans = build_alternative_plans({
        "target_amount": analysis.target_amount,
        "monthly_amount": analysis.monthly_amount,
    })

    return Response({
        "summary": result.summary,
        "goal_math": goal_math,
        "alternative_plans": alt_plans,
        "items": enriched_items,
        "created_at": result.created_at,
    })
