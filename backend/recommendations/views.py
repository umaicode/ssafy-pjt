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

    # ✅ 여행 목적일 때 환율 정보 계산
    exchange_rate_info = None
    if analysis.purpose == "travel" and analysis.travel_country_code:
        from exchange.models import ExchangeRate
        
        country_code = analysis.travel_country_code
        
        # 통화 코드 매핑 (API의 cur_unit 형식으로 변환)
        currency_mapping = {
            "JPY": "JPY(100)",
            "USD": "USD",
            "EUR": "EUR",
            "CNH": "CNH",
            "CNY": "CNH",  # CNY도 CNH로 매핑
            "THB": "THB",
            "SGD": "SGD",
            "GBP": "GBP",
            "HKD": "HKD",
        }
        
        cur_unit = currency_mapping.get(country_code, country_code)
        
        try:
            exchange_rate = ExchangeRate.objects.get(cur_unit=cur_unit)
            
            # deal_bas_r (매매기준율)에서 쉼표 제거 후 float 변환
            rate_str = exchange_rate.deal_bas_r.replace(",", "") if exchange_rate.deal_bas_r else "0"
            exchange_rate_value = float(rate_str) if rate_str else 0
            
            # JPY(100)의 경우 100엔 기준이므로 1엔 기준으로 변환
            if cur_unit == "JPY(100)":
                exchange_rate_value = exchange_rate_value / 100
            
            # 예상 이자 계산 (추천된 상품 중 가장 높은 금리 적용)
            best_rate = 0
            for item in enriched_items:
                if item.get("detail") and item["detail"].get("intr_rate2"):
                    try:
                        item_rate = float(item["detail"]["intr_rate2"])
                        if item_rate > best_rate:
                            best_rate = item_rate
                    except (ValueError, TypeError):
                        pass
            
            if best_rate == 0:
                best_rate = 3.5  # 기본 금리
            
            # 만기 시 예상 금액 계산 (단리)
            principal = int(analysis.monthly_amount) * int(analysis.period_months)
            interest = int(principal * (best_rate / 100) * (int(analysis.period_months) / 12))
            total_with_interest = principal + interest
            
            # 외화 환산 (환율로 나누기)
            if exchange_rate_value > 0:
                foreign_amount = round(total_with_interest / exchange_rate_value, 2)
            else:
                foreign_amount = 0
            
            exchange_rate_info = {
                "currency_code": country_code,
                "currency_name": exchange_rate.cur_nm,
                "exchange_rate": exchange_rate_value,
                "updated_at": exchange_rate.search_date,
                "applied_rate": best_rate,
                "estimated_interest": interest,
                "total_with_interest_krw": total_with_interest,
                "total_with_interest_foreign": foreign_amount,
            }
            
        except ExchangeRate.DoesNotExist:
            # 환율 데이터가 없는 경우
            principal = int(analysis.monthly_amount) * int(analysis.period_months)
            exchange_rate_info = {
                "currency_code": country_code,
                "currency_name": f"{country_code} (환율 데이터 없음)",
                "exchange_rate": None,
                "updated_at": None,
                "error_message": "환율 데이터가 존재하지 않습니다.",
                "total_with_interest_krw": principal,
                "total_with_interest_foreign": None,
            }

    return Response({
        "summary": result.summary,
        "goal_math": goal_math,
        "alternative_plans": alt_plans,
        "items": enriched_items,
        "exchange_rate_info": exchange_rate_info,
        "created_at": result.created_at,
    })


# ============================================================
# 새로운 플랜 기반 분석 API (plan_engine + GPT 하이브리드)
# ============================================================
from .plan_engine import (
    generate_financial_plans,
    check_feasibility,
    calculate_deposit_maturity,
    calculate_saving_maturity,
    FeasibilityStatus,
)
from .llm import generate_plan_advice


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def analyze_with_plan(request):
    """
    [POST] /api/v1/analysis/plan/
    
    하이브리드 분석 API (plan_engine 계산 + GPT 조언)
    
    1단계: plan_engine으로 정확한 계산 수행
    2단계: GPT로 개인화된 조언 생성
    
    Request Body:
    {
        "purpose": "주택" | "목돈" | "여행",
        "property_type": "매매" | "전세" | "월세",  // 주택일 경우만
        "current_amount": 10000000,  // 현재 보유 금액 (원)
        "monthly_amount": 500000,    // 월 저축 가능 금액 (원)
        "target_amount": 50000000,   // 목표 금액 (원)
        "period_months": 24          // 목표 기간 (개월)
    }
    """
    from .serializers import AnalysisCreateSerializer
    
    serializer = AnalysisCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    
    # 분석 요청 저장
    analysis = AnalysisRequest.objects.create(
        user=request.user,
        purpose=data['purpose'],
        property_type=data.get('property_type'),
        period_months=data['period_months'],
        target_amount=data['target_amount'],
        monthly_amount=data['monthly_amount'],
        current_amount=data.get('current_amount', 0),
    )
    
    # ========================================
    # 1단계: plan_engine으로 정확한 계산
    # ========================================
    plan_result = generate_financial_plans(
        purpose=data['purpose'],
        current_amount=data.get('current_amount', 0),
        monthly_amount=data['monthly_amount'],
        target_amount=data['target_amount'],
        period_months=data['period_months'],
        property_type=data.get('property_type'),
    )
    
    # ========================================
    # 2단계: GPT로 개인화된 조언 생성
    # ========================================
    user_input = {
        'purpose': data['purpose'],
        'property_type': data.get('property_type'),
        'current_amount': data.get('current_amount', 0),
        'monthly_amount': data['monthly_amount'],
        'target_amount': data['target_amount'],
        'period_months': data['period_months'],
    }
    
    ai_advice = generate_plan_advice(user_input, plan_result)
    
    # 결과에 AI 조언 추가
    plan_result['ai_advice'] = ai_advice.get('advice', {})
    plan_result['ai_success'] = ai_advice.get('success', False)
    
    # 결과 저장
    RecommendationResult.objects.create(
        analysis=analysis,
        summary=plan_result['summary'],
        items=plan_result['plans'],
        gpt_raw=str(ai_advice)  # AI 응답 원본 저장
    )
    
    return Response({
        "analysis_id": analysis.id,
        **plan_result
    }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_plan_result(request, analysis_id: int):
    """
    [GET] /api/v1/analysis/<analysis_id>/plan/
    
    저장된 플랜 결과 조회
    """
    analysis = AnalysisRequest.objects.filter(id=analysis_id, user=request.user).first()
    if not analysis:
        return Response({"detail": "분석 요청을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    if not hasattr(analysis, 'result'):
        return Response({"detail": "분석 결과가 아직 생성되지 않았습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    result = analysis.result
    
    return Response({
        "analysis_id": analysis.id,
        "purpose": analysis.purpose,
        "property_type": analysis.property_type,
        "current_amount": analysis.current_amount,
        "monthly_amount": analysis.monthly_amount,
        "target_amount": analysis.target_amount,
        "period_months": analysis.period_months,
        "summary": result.summary,
        "plans": result.items,
        "created_at": result.created_at,
    })


@api_view(["POST"])
def calculate_preview(request):
    """
    [POST] /api/v1/analysis/calculate/
    
    로그인 없이도 사용 가능한 간단 계산 미리보기 API
    만기 금액만 계산해서 반환 (상품 추천 X)
    
    Request Body:
    {
        "current_amount": 10000000,
        "monthly_amount": 500000,
        "period_months": 24,
        "deposit_rate": 3.5,  // 예금 금리 (없으면 DB 최고 금리)
        "saving_rate": 4.5    // 적금 금리 (없으면 DB 최고 금리)
    }
    """
    current_amount = int(request.data.get('current_amount', 0))
    monthly_amount = int(request.data.get('monthly_amount', 0))
    period_months = int(request.data.get('period_months', 12))
    
    # 금리 (미입력 시 기본값)
    deposit_rate = float(request.data.get('deposit_rate', 3.5))
    saving_rate = float(request.data.get('saving_rate', 4.5))
    
    # 계산
    deposit_result = calculate_deposit_maturity(current_amount, deposit_rate, period_months)
    saving_result = calculate_saving_maturity(monthly_amount, saving_rate, period_months)
    
    total_principal = deposit_result.principal + saving_result.principal
    total_interest = deposit_result.interest + saving_result.interest
    total_maturity = deposit_result.maturity_amount + saving_result.maturity_amount
    total_after_tax = deposit_result.after_tax_amount + saving_result.after_tax_amount
    
    return Response({
        "deposit": {
            "principal": deposit_result.principal,
            "interest": deposit_result.interest,
            "maturity_amount": deposit_result.maturity_amount,
            "after_tax_amount": deposit_result.after_tax_amount,
            "annual_rate": deposit_result.annual_rate,
        },
        "saving": {
            "principal": saving_result.principal,
            "interest": saving_result.interest,
            "maturity_amount": saving_result.maturity_amount,
            "after_tax_amount": saving_result.after_tax_amount,
            "annual_rate": saving_result.annual_rate,
        },
        "total": {
            "principal": total_principal,
            "interest": total_interest,
            "maturity_amount": total_maturity,
            "after_tax_amount": total_after_tax,
        },
        "period_months": period_months,
    })


@api_view(["POST"])
def check_feasibility_api(request):
    """
    [POST] /api/v1/analysis/feasibility/
    
    목표 달성 가능성 판정만 수행 (로그인 불필요)
    
    Request Body:
    {
        "current_amount": 10000000,
        "monthly_amount": 500000,
        "target_amount": 50000000,
        "period_months": 24
    }
    """
    current_amount = int(request.data.get('current_amount', 0))
    monthly_amount = int(request.data.get('monthly_amount', 0))
    target_amount = int(request.data.get('target_amount', 0))
    period_months = int(request.data.get('period_months', 12))
    
    if target_amount <= 0:
        return Response({"error": "목표 금액을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    result = check_feasibility(
        current_amount=current_amount,
        monthly_amount=monthly_amount,
        target_amount=target_amount,
        period_months=period_months,
    )
    
    # Enum을 문자열로 변환
    result['status'] = result['status'].value
    
    return Response(result)
