import re, math
from typing import Any, Dict, List, Tuple, Optional

# 한국 이자소득세율 (15.4% = 소득세 14% + 지방소득세 1.4%)
INTEREST_TAX_RATE = 0.154


def compute_goal_math(
    user_input: dict, deposit_rate: float = 3.5, saving_rate: float = 4.0
) -> dict:
    """
    목표 달성 가능 여부 계산
    - 현재 보유금 + 예금 이자
    - 월 납입액 + 적금 이자
    - 예금+적금 조합 시 총 예상 금액으로 판단
    ★★★ 세전 이자로 계산 (세후는 별도 필드로 제공) ★★★
    """
    period = int(user_input.get("period_months") or 0)
    target = int(user_input.get("target_amount") or 0)
    monthly = int(user_input.get("monthly_amount") or 0)
    current_savings = int(user_input.get("current_savings") or 0)

    # 단순 계획 (이자 미포함)
    planned_total_simple = monthly * period if (monthly > 0 and period > 0) else 0

    # === 세전 이자 계산 ===
    # 1) 예금 이자 (보유금을 예금에 넣었을 때) - 세전
    deposit_interest = 0
    if current_savings > 0 and period > 0:
        deposit_interest = int(current_savings * (deposit_rate / 100) * (period / 12))

    # 2) 적금 이자 (월 납입액을 적금에 넣었을 때) - 세전
    saving_interest = 0
    if monthly > 0 and period > 0:
        # 단리 적금 이자 공식: 월납입액 × 기간 × (기간+1) / 2 × 월이율
        saving_interest = int(
            monthly * period * (period + 1) / 2 * ((saving_rate / 100) / 12)
        )

    # 총 세전 이자
    total_interest_before_tax = deposit_interest + saving_interest

    # 세후 이자 (15.4% 공제)
    deposit_interest_after_tax = int(deposit_interest * (1 - INTEREST_TAX_RATE))
    saving_interest_after_tax = int(saving_interest * (1 - INTEREST_TAX_RATE))
    total_interest_after_tax = deposit_interest_after_tax + saving_interest_after_tax

    # 세금액
    tax_amount = total_interest_before_tax - total_interest_after_tax

    # 3) 예금+적금 조합 총액 (세전 이자 포함)
    total_with_interest = (
        current_savings + deposit_interest + planned_total_simple + saving_interest
    )

    # 세후 총액
    total_with_interest_after_tax = (
        current_savings
        + deposit_interest_after_tax
        + planned_total_simple
        + saving_interest_after_tax
    )

    # 4) 적금만 (이자 포함) - 비교용
    saving_only_total = planned_total_simple + saving_interest

    months_to_goal = (
        math.ceil((target - current_savings) / monthly)
        if (target > 0 and monthly > 0 and target > current_savings)
        else None
    )

    # 목표 달성에 필요한 월 납입액 계산 (보유금 + 이자 고려)
    remaining_target = max(0, target - current_savings - deposit_interest)
    if period > 0 and remaining_target > 0:
        # 적금 이자 고려한 필요 월납입액 (역산)
        multiplier = period + period * (period + 1) / 2 * ((saving_rate / 100) / 12)
        required_monthly = (
            math.ceil(remaining_target / multiplier) if multiplier > 0 else None
        )
    else:
        required_monthly = 0 if remaining_target <= 0 else None

    # 달성 가능 여부 판단 (예금+적금 조합 기준, 세전 기준)
    achievable = total_with_interest >= target if (target > 0 and period > 0) else False

    # 세후 기준 달성 가능 여부
    achievable_after_tax = (
        total_with_interest_after_tax >= target
        if (target > 0 and period > 0)
        else False
    )

    # 부족액 계산 (세전 기준)
    shortfall = max(0, target - total_with_interest)
    shortfall_after_tax = max(0, target - total_with_interest_after_tax)

    extra_needed_per_month = None
    if required_monthly is not None and monthly > 0:
        extra_needed_per_month = max(0, required_monthly - monthly)

    return {
        "period_months": period,
        "target_amount": target,
        "monthly_amount": monthly,
        "current_savings": current_savings,
        # 단순 계획 (적금 원금만)
        "planned_total_amount": planned_total_simple,
        # 세전 이자 정보
        "deposit_interest": deposit_interest,
        "saving_interest": saving_interest,
        "total_interest": total_interest_before_tax,
        # 세후 이자 정보
        "deposit_interest_after_tax": deposit_interest_after_tax,
        "saving_interest_after_tax": saving_interest_after_tax,
        "total_interest_after_tax": total_interest_after_tax,
        "tax_amount": tax_amount,
        "tax_rate": INTEREST_TAX_RATE,
        # 총 예상 금액 (세전)
        "total_with_interest": total_with_interest,
        # 총 예상 금액 (세후)
        "total_with_interest_after_tax": total_with_interest_after_tax,
        "saving_only_total": saving_only_total,
        # 목표 달성 관련
        "months_to_goal": months_to_goal,
        "required_monthly_amount": required_monthly,
        "extra_needed_per_month": extra_needed_per_month,
        "achievable_in_period": achievable,  # 세전 기준
        "achievable_after_tax": achievable_after_tax,  # 세후 기준
        "shortfall_amount": shortfall,  # 세전 기준
        "shortfall_after_tax": shortfall_after_tax,  # 세후 기준
        # 사용된 금리
        "deposit_rate": deposit_rate,
        "saving_rate": saving_rate,
    }


# -----------------------------
# 1) 우대조건 키워드 추출/난이도
# -----------------------------

EASY_KWS = [
    "자동이체",
    "비대면",
    "모바일",
    "앱",
    "인터넷",
    "스마트폰",
    "첫거래",
    "신규",
]
HARD_KWS = [
    "카드",
    "신용카드",
    "체크카드",
    "카드실적",
    "사용실적",
    "결제",
    "이용실적",
    "실적",
]


def compress_spcl_cnd(text: str, max_len: int = 140) -> Dict[str, Any]:
    if not text:
        return {"short": "", "keywords": [], "hard": [], "easy": []}

    cleaned = re.sub(r"\s+", " ", str(text)).strip()
    short = cleaned[:max_len]

    easy = [k for k in EASY_KWS if k in cleaned]
    hard = [k for k in HARD_KWS if k in cleaned]

    # 키워드는 UI 표시용/디버깅용으로 합쳐서 저장
    keywords = list(dict.fromkeys(easy + hard))[:10]
    return {"short": short, "keywords": keywords, "hard": hard[:10], "easy": easy[:10]}


def channel_bonus(join_way: str) -> float:
    """
    join_way: "인터넷,스마트폰,영업점" 이런 식일 가능성
    """
    s = join_way or ""
    bonus = 0.0
    if "스마트폰" in s or "모바일" in s or "앱" in s:
        bonus += 0.10
    if "인터넷" in s:
        bonus += 0.07
    # 영업점만 있으면 가산 없음
    return bonus


def condition_penalty(spcl_cnd: str) -> float:
    """
    카드실적류가 많을수록 감점
    """
    info = compress_spcl_cnd(spcl_cnd or "")
    hard_cnt = len(info["hard"])
    easy_cnt = len(info["easy"])

    # 쉬운 조건은 약간 가산, 어려운 조건은 감점
    # (너가 원하는 방향에 맞게 계수는 쉽게 조정 가능)
    penalty = 0.0
    penalty += hard_cnt * 0.08  # 어려운 키워드 하나당 -0.08
    penalty -= easy_cnt * 0.03  # 쉬운 키워드 하나당 +0.03 (감점 감소)
    return penalty


# -----------------------------
# 2) 달성가능성(feasibility)
# -----------------------------


def feasibility_score(
    period_months: int, target_amount: int, monthly_amount: int
) -> float:
    """
    monthly_amount * period_months 가 target_amount에 얼마나 근접/충족하는지 점수화 (0~1 권장)
    - 부족하면 0~1 사이
    - 초과해도 1 이상으로 올리지 않고 1로 캡
    """
    period_months = max(1, int(period_months))
    target_amount = max(1, int(target_amount))
    monthly_amount = max(0, int(monthly_amount))

    planned = monthly_amount * period_months  # 단순 누적(이자 고려 X)
    ratio = planned / target_amount

    # 너무 부족하면 낮게, 1 이상이면 1로
    if ratio >= 1.0:
        return 1.0
    # 0.0 ~ 1.0
    return max(0.0, min(1.0, ratio))


# -----------------------------
# 3) 한도 적합성(limit fitness)
# -----------------------------


def limit_fitness(
    max_limit: int | None, target_amount: int, monthly_amount: int, period_months: int
) -> float:
    """
    Option.max_limit 기준 적합성
    - max_limit이 없으면 중립(0.0)
    - 계획 금액이 max_limit를 넘을수록 감점
    """
    if max_limit is None:
        return 0.0

    try:
        ml = int(max_limit)
    except:
        return 0.0

    planned = int(monthly_amount) * int(period_months)
    if ml <= 0:
        return 0.0

    # planned가 한도 이하이면 가산(0~0.1), 초과하면 감점(0~0.25)
    if planned <= ml:
        # 여유가 많을수록 아주 살짝 가산
        return 0.10
    else:
        # 초과 비율이 클수록 감점 커짐
        over_ratio = (planned - ml) / ml
        return -min(0.25, over_ratio * 0.25)


# -----------------------------
# 4) 금리 점수(rate score)
# -----------------------------


def rate_score(base_rate: float, max_rate: float) -> float:
    """
    금리를 0~1 근사로 매핑 (상대 비교용)
    - 여기서는 단순히 max_rate 중심
    - 후보군 내에서 정규화하면 더 정확하지만, 빠른 구현용으로 고정 스케일 사용
    """
    br = float(base_rate or 0.0)
    mr = float(max_rate or 0.0)

    # 한국 예/적금 금리 범위를 대충 0~6%로 가정 (프로젝트용)
    # 범위를 벗어나면 클램프
    x = max(0.0, min(6.0, mr))
    return x / 6.0


# -----------------------------
# 5) 최종 후보 점수 계산
# -----------------------------


def candidate_score(
    opt: Any,
    kind: str,
    user_input: Dict[str, Any],
) -> Tuple[float, Dict[str, Any]]:
    """
    opt: DepositOption or SavingOption (select_related(product))
    user_input: purpose, period_months, target_amount, monthly_amount
    반환: (final_score, debug_parts)
    """
    p = opt.product

    period_months = int(user_input["period_months"])
    target_amount = int(user_input["target_amount"])
    monthly_amount = int(user_input["monthly_amount"])
    user_period = int(user_input["period_months"])
    opt_period = int(getattr(opt, "save_trm", 0) or 0)
    tadj = term_adjustment(user_period, opt_period)

    # 1) 달성가능성(중요도 높게)
    feas = feasibility_score(period_months, target_amount, monthly_amount)  # 0~1

    # 2) 금리
    rscore = rate_score(
        getattr(opt, "intr_rate", 0), getattr(opt, "intr_rate2", 0)
    )  # 0~1

    # 3) 채널 가산
    cbonus = channel_bonus(getattr(p, "join_way", ""))  # 0~0.17

    # 4) 우대조건 난이도 감점
    cpen = condition_penalty(getattr(p, "spcl_cnd", ""))  # 0~(대략 0.4)

    # 5) 한도 적합성 (옵션에 존재)
    lfit = limit_fitness(
        getattr(opt, "max_limit", None), target_amount, monthly_amount, period_months
    )  # -0.25~+0.1

    # ✅ 가중치 조합 (너가 원하는대로 조정 가능)
    # 달성가능성을 가장 중요하게(0.55), 금리(0.35), 나머지 보정
    final = (
        0.55 * feas
        + 0.35 * rscore
        + 1.00 * cbonus
        + 1.00 * lfit
        - 1.00 * cpen
        + 1.00 * tadj
    )

    debug = {
        "feasibility": feas,
        "rate_score": rscore,
        "channel_bonus": cbonus,
        "limit_fit": lfit,
        "condition_penalty": cpen,
        "final": final,
        "kind": kind,
        "option_id": int(opt.id),
        "product_id": int(p.id),
        "bank": getattr(p, "kor_co_nm", ""),
        "name": getattr(p, "fin_prdt_nm", ""),
        "join_way": getattr(p, "join_way", ""),
    }
    return final, debug


# -----------------------------
# 6) 후보 뽑기 + 점수 정렬
# -----------------------------
def _pick_terms_near(kind_model, user_period: int) -> List[int]:
    """
    DB에 존재하는 save_trm들 중 사용자 기간 주변(하위/상위)을 골라준다.
    예: user_period=27, DB terms=[6,12,24,36] -> [24,36]
    """
    qs = kind_model.objects.values_list("save_trm", flat=True).distinct()
    terms = sorted({int(t) for t in qs if t is not None})

    if not terms:
        return []

    lower = [t for t in terms if t <= user_period]
    upper = [t for t in terms if t >= user_period]

    chosen = set()
    if lower:
        chosen.add(max(lower))
    if upper:
        chosen.add(min(upper))

    # 혹시 user_period가 정확히 있으면 그거 하나로 충분
    # chosen에 user_period가 들어가면 lower/upper가 동일할 수 있음(자동 처리)
    return sorted(chosen)


def pick_candidates_scored(
    user_input: Dict[str, Any],
    dep_limit: int = 80,
    sav_limit: int = 80,
    top_n: int = 60,
):
    from products.models import DepositOption, SavingOption

    user_period = int(user_input["period_months"])
    monthly_amount = int(user_input.get("monthly_amount", 0))
    current_savings = int(user_input.get("current_savings", 0))

    # ✅ 중요: 월 납입액이 있으면 적금 중심, 목돈이 있으면 예금도 고려
    # 월 납입만 있고 목돈이 없으면 -> 적금만 추천
    # 목돈이 있으면 -> 예금+적금 조합 추천

    scored: List[Tuple[float, Any, str, Dict[str, Any]]] = []

    # 적금은 항상 추천 (월 납입이 있을 때)
    if monthly_amount > 0:
        sav_terms = _pick_terms_near(SavingOption, user_period)
        sav_qs = (
            SavingOption.objects.select_related("product").filter(
                save_trm__in=sav_terms
            )
        )[:sav_limit]

        for opt in sav_qs:
            s, dbg = candidate_score(opt, "saving", user_input)
            scored.append((s, opt, "saving", dbg))

    # 예금은 보유금이 있거나, 월 납입이 없을 때만 추천
    if current_savings > 0 or monthly_amount == 0:
        dep_terms = _pick_terms_near(DepositOption, user_period)
        dep_qs = (
            DepositOption.objects.select_related("product").filter(
                save_trm__in=dep_terms
            )
        )[:dep_limit]

        for opt in dep_qs:
            s, dbg = candidate_score(opt, "deposit", user_input)
            scored.append((s, opt, "deposit", dbg))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_n]


def term_adjustment(user_period: int, opt_period: int) -> float:
    """
    - opt_period <= user_period : 만기 후 재운용(보수적) 가능 -> 약간 가산
    - opt_period >  user_period : 중도해지 가능성 -> 감점
    """
    d = opt_period - user_period
    if d == 0:
        return 0.08  # 정확히 맞으면 가산
    if d < 0:
        # 27개월 목표인데 24개월이면 재운용 필요: 가산은 작게
        return 0.03
    # 36개월 추천은 중도해지 리스크 -> 감점
    return -min(0.15, (d / 12) * 0.10)  # 12개월 초과당 -0.10, 최대 -0.15


# -----------------------------
# 7) GPT로 넘길 compact dict 생성 (한도/우대/채널 포함)
# -----------------------------


def option_to_compact_dict(opt: Any, kind: str) -> Dict[str, Any]:
    p = opt.product
    sp = compress_spcl_cnd(getattr(p, "spcl_cnd", "") or "")

    return {
        "kind": kind,
        "option_id": int(opt.id),
        "product_id": int(p.id),
        "bank": str(getattr(p, "kor_co_nm", "") or ""),
        "name": str(getattr(p, "fin_prdt_nm", "") or ""),
        "period_months": int(getattr(opt, "save_trm", 0) or 0),
        "base_rate": float(getattr(opt, "intr_rate", 0) or 0),
        "max_rate": float(getattr(opt, "intr_rate2", 0) or 0),
        # ✅ 옵션 한도 (네 모델 기준)
        "max_limit": getattr(opt, "max_limit", None),
        # ✅ 채널
        "join_way": str(getattr(p, "join_way", "") or ""),
        "join_member": str(getattr(p, "join_member", "") or ""),
        # ✅ 우대조건
        "spcl_cnd_short": sp["short"],
        "spcl_cnd_keywords": sp["keywords"],
    }


import json
import hashlib


def make_cache_key(user_input: dict, candidates: list[dict]) -> str:
    """
    같은 입력 + 같은 후보면 GPT 재호출 방지하기 위한 캐시 키
    """
    base = {
        "purpose": user_input.get("purpose"),
        "period_months": int(user_input.get("period_months")),
        "target_amount": int(user_input.get("target_amount")),
        "monthly_amount": int(user_input.get("monthly_amount")),
        "current_savings": int(
            user_input.get("current_savings") or 0
        ),  # ★ 보유금도 캐시 키에 포함
        # 후보 전체를 넣으면 길어지니까 option_id만 사용
        "candidate_option_ids": [c.get("option_id") for c in candidates],
        "v": 4,  # ★ 버전 올림 - 기존 캐시 무효화
    }
    s = json.dumps(base, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def validate_reco_payload(
    payload: dict, candidates: list[dict], top_k: int = 5
) -> dict:
    """
    - option_id가 후보에 있으면 kind/product_id는 후보값으로 강제 교정(LLM 실수 방지)
    - 후보 밖 option_id는 버림
    - 부족하면 pre_score 상위로 채워서 항상 top_k 맞춤(안 터지게)
    """
    # option_id -> candidate dict
    cand_map = {int(c["option_id"]): c for c in candidates}

    recos = payload.get("recommendations", [])
    if not isinstance(recos, list):
        recos = []

    used_option_ids = set()
    cleaned_items = []

    # 1) GPT 추천 정리/교정
    for r in recos:
        try:
            oid = int(r.get("option_id"))
        except:
            continue

        if oid not in cand_map:
            continue
        if oid in used_option_ids:
            continue

        cand = cand_map[oid]
        # ✅ kind/product_id는 후보 기준으로 강제 교정
        kind = cand["kind"]
        pid = int(cand["product_id"])

        try:
            score = float(r.get("fit_score", 0))
        except:
            score = 0.0
        score = max(0.0, min(1.0, score))

        reason = (r.get("reason") or "").strip()[:220]
        if not reason:
            reason = "후보 조건/금리/우대조건 난이도를 종합해 추천했습니다."

        cleaned_items.append(
            {
                "kind": kind,
                "option_id": oid,
                "product_id": pid,
                "fit_score": score,
                "reason": reason,
            }
        )
        used_option_ids.add(oid)

        if len(cleaned_items) == top_k:
            break

    # 2) 부족하면 후보 pre_score 상위로 채우기 (절대 터지지 않게)
    if len(cleaned_items) < top_k:
        # candidates에 pre_score가 있으면 그걸 우선 사용
        def _cand_sort_key(c):
            return float(c.get("pre_score", 0.0))

        fallback_sorted = sorted(candidates, key=_cand_sort_key, reverse=True)
        for c in fallback_sorted:
            oid = int(c["option_id"])
            if oid in used_option_ids:
                continue
            cleaned_items.append(
                {
                    "kind": c["kind"],
                    "option_id": oid,
                    "product_id": int(c["product_id"]),
                    "fit_score": 0.50,
                    "reason": "LLM 출력이 일부 불완전하여 내부 점수(pre_score) 기준으로 보완 추천했습니다.",
                }
            )
            used_option_ids.add(oid)
            if len(cleaned_items) == top_k:
                break

    # 여기까지 왔는데도 부족하면 candidates 자체가 부족한 것
    if len(cleaned_items) != top_k:
        raise ValueError("Not enough valid candidates to fill recommendations")

    summary = (payload.get("summary") or "").strip()[:600]
    strategy = (payload.get("strategy") or "").strip()[:600]
    goal_math = payload.get("goal_math") or {}

    return {
        "summary": summary,
        "strategy": strategy,
        "goal_math": goal_math,
        "items": cleaned_items,
    }


def build_alternative_plans(
    user_input: dict, months_list=(3, 6, 12, 24, 36)
) -> list[dict]:
    target = int(user_input.get("target_amount") or 0)
    monthly = int(user_input.get("monthly_amount") or 0)

    plans = []
    for m in months_list:
        required = math.ceil(target / m) if (target > 0 and m > 0) else None
        extra = (
            max(0, required - monthly)
            if (required is not None and monthly > 0)
            else None
        )
        plans.append(
            {
                "period_months": m,
                "required_monthly_amount": required,
                "extra_needed_per_month": extra,
            }
        )
    return plans


# -----------------------------
# 8) 예금/적금 조합 최적화 계산
# -----------------------------

# 한국 이자소득세율 (15.4% = 소득세 14% + 지방소득세 1.4%)
INTEREST_TAX_RATE = 0.154


def calculate_deposit_interest(
    principal: int, rate: float, months: int, after_tax: bool = False
) -> dict:
    """
    예금 이자 계산 (단리)
    principal: 원금
    rate: 연이율 (%)
    months: 기간 (개월)
    after_tax: 세후 이자 계산 여부 (기본값: False = 세전)
    """
    rate_decimal = rate / 100
    interest_before_tax = principal * rate_decimal * (months / 12)

    if after_tax:
        interest = interest_before_tax * (1 - INTEREST_TAX_RATE)
    else:
        interest = interest_before_tax

    total = principal + interest
    return {
        "principal": principal,
        "interest_before_tax": round(interest_before_tax),
        "interest": round(interest),
        "interest_after_tax": round(interest_before_tax * (1 - INTEREST_TAX_RATE)),
        "tax_amount": round(interest_before_tax * INTEREST_TAX_RATE),
        "total": round(total),
        "total_after_tax": round(
            principal + interest_before_tax * (1 - INTEREST_TAX_RATE)
        ),
        "rate": rate,
        "months": months,
        "is_after_tax": after_tax,
    }


def calculate_saving_interest(
    monthly: int, rate: float, months: int, after_tax: bool = False
) -> dict:
    """
    적금 이자 계산 (단리, 월복리 근사)
    monthly: 월 납입액
    rate: 연이율 (%)
    months: 기간 (개월)
    after_tax: 세후 이자 계산 여부 (기본값: False = 세전)
    """
    rate_decimal = rate / 100
    total_principal = monthly * months
    # 단리 적금 이자 공식: 월납입액 × 기간 × (기간+1) / 2 × 월이율
    interest_before_tax = monthly * months * (months + 1) / 2 * (rate_decimal / 12)

    if after_tax:
        interest = interest_before_tax * (1 - INTEREST_TAX_RATE)
    else:
        interest = interest_before_tax

    total = total_principal + interest
    return {
        "principal": total_principal,
        "interest_before_tax": round(interest_before_tax),
        "interest": round(interest),
        "interest_after_tax": round(interest_before_tax * (1 - INTEREST_TAX_RATE)),
        "tax_amount": round(interest_before_tax * INTEREST_TAX_RATE),
        "total": round(total),
        "total_after_tax": round(
            total_principal + interest_before_tax * (1 - INTEREST_TAX_RATE)
        ),
        "rate": rate,
        "months": months,
        "monthly_payment": monthly,
        "is_after_tax": after_tax,
    }


def optimize_deposit_saving_combination(
    current_savings: int,
    monthly_amount: int,
    target_amount: int,
    period_months: int,
    deposit_rate: float = 3.5,
    saving_rate: float = 4.0,
    deposit_save_trm: int = None,  # 실제 예금 상품의 가입 기간
    saving_save_trm: int = None,  # 실제 적금 상품의 가입 기간
) -> dict:
    """
    예금과 적금을 어떻게 조합하면 최적인지 계산
    ★★★ 실제 상품의 가입 기간(save_trm)을 기준으로 계산 ★★★

    전략 1: 예금 + 적금 병행 (보유금은 예금, 월납입은 적금)
    전략 2: 전액 적금 (보유금을 분할해서 월 납입액에 추가)
    전략 3: 적금만 (보유금 없이 월납입만)
    전략 4: 예금만 (보유금만 예금에 넣고 적금 안함)
    """
    strategies = []

    # 실제 상품 기간이 없으면 사용자 목표 기간 사용 (fallback)
    actual_deposit_term = deposit_save_trm if deposit_save_trm else period_months
    actual_saving_term = saving_save_trm if saving_save_trm else period_months

    # 전략 1: 예금 + 적금 병행 (보유금 → 예금, 월납입 → 적금)
    if current_savings > 0 and monthly_amount > 0:
        dep_result = calculate_deposit_interest(
            current_savings, deposit_rate, actual_deposit_term
        )
        sav_result = calculate_saving_interest(
            monthly_amount, saving_rate, actual_saving_term
        )
        total_1 = dep_result["total"] + sav_result["total"]
        total_interest_1 = dep_result["interest"] + sav_result["interest"]
        strategies.append(
            {
                "strategy_name": "예금 + 적금 병행",
                "strategy_type": "deposit_and_saving",
                "description": f"보유금 {current_savings:,}원은 예금({actual_deposit_term}개월 만기), 매달 {monthly_amount:,}원은 적금({actual_saving_term}개월 만기)",
                "deposit": dep_result,
                "saving": sav_result,
                "total_amount": round(total_1),
                "total_interest": round(total_interest_1),
                "achievable": total_1 >= target_amount,
                "shortfall": max(0, target_amount - round(total_1)),
                "uses_deposit": True,
                "uses_saving": True,
                "deposit_term": actual_deposit_term,
                "saving_term": actual_saving_term,
            }
        )

    # 전략 2: 보유금 분할 → 월 납입액 증가 (전부 적금) - 실제 적금 상품 기간 기준
    if current_savings > 0 and actual_saving_term > 0:
        extra_monthly = current_savings // actual_saving_term
        total_monthly = monthly_amount + extra_monthly
        sav_result_2 = calculate_saving_interest(
            total_monthly, saving_rate, actual_saving_term
        )
        strategies.append(
            {
                "strategy_name": "전액 적금 (보유금 분할)",
                "strategy_type": "saving_only_split",
                "description": f"보유금을 {actual_saving_term}개월로 분할하여 매달 {total_monthly:,}원 적금 ({actual_saving_term}개월 만기 상품)",
                "deposit": None,
                "saving": sav_result_2,
                "total_amount": sav_result_2["total"],
                "total_interest": sav_result_2["interest"],
                "achievable": sav_result_2["total"] >= target_amount,
                "shortfall": max(0, target_amount - sav_result_2["total"]),
                "extra_monthly_from_savings": extra_monthly,
                "uses_deposit": False,
                "uses_saving": True,
                "saving_term": actual_saving_term,
            }
        )

    # 전략 3: 적금만 (보유금 없이 월납입만) - 실제 적금 상품 기간 기준
    if monthly_amount > 0:
        sav_result_3 = calculate_saving_interest(
            monthly_amount, saving_rate, actual_saving_term
        )
        strategies.append(
            {
                "strategy_name": "적금만",
                "strategy_type": "saving_only",
                "description": f"매달 {monthly_amount:,}원 적금 ({actual_saving_term}개월 만기 상품)",
                "deposit": None,
                "saving": sav_result_3,
                "total_amount": sav_result_3["total"],
                "total_interest": sav_result_3["interest"],
                "achievable": sav_result_3["total"] >= target_amount,
                "shortfall": max(0, target_amount - sav_result_3["total"]),
                "uses_deposit": False,
                "uses_saving": True,
                "saving_term": actual_saving_term,
            }
        )

    # 전략 4: 예금만 (보유금만 예금에, 적금 안함) - 실제 예금 상품 기간 기준
    if current_savings > 0:
        dep_result_4 = calculate_deposit_interest(
            current_savings, deposit_rate, actual_deposit_term
        )
        strategies.append(
            {
                "strategy_name": "예금만",
                "strategy_type": "deposit_only",
                "description": f"보유금 {current_savings:,}원을 예금 ({actual_deposit_term}개월 만기 상품)",
                "deposit": dep_result_4,
                "saving": None,
                "total_amount": dep_result_4["total"],
                "total_interest": dep_result_4["interest"],
                "achievable": dep_result_4["total"] >= target_amount,
                "shortfall": max(0, target_amount - dep_result_4["total"]),
                "uses_deposit": True,
                "uses_saving": False,
                "deposit_term": actual_deposit_term,
            }
        )

    # 최적 전략 선택 (총 수익이 가장 높은 것)
    best = max(strategies, key=lambda x: x["total_amount"]) if strategies else None

    return {
        "strategies": strategies,
        "best_strategy": best,
        "analysis": {
            "current_savings": current_savings,
            "monthly_amount": monthly_amount,
            "target_amount": target_amount,
            "period_months": period_months,
            "deposit_rate": deposit_rate,
            "saving_rate": saving_rate,
        },
    }


def build_smart_alternative_plans(
    user_input: dict,
    goal_math: dict,
) -> list[dict]:
    """
    목표 달성이 불가능할 때 다양한 대안 제시
    - 기간 조정
    - 월 납입액 조정
    - 목표 금액 조정
    """
    target = int(user_input.get("target_amount") or 0)
    monthly = int(user_input.get("monthly_amount") or 0)
    period = int(user_input.get("period_months") or 0)
    current = int(user_input.get("current_savings") or 0)

    plans = []

    # 1. 기간 연장 옵션들
    for extra_months in [6, 12, 18, 24]:
        new_period = period + extra_months
        new_total = current + (monthly * new_period)
        if new_total >= target:
            plans.append(
                {
                    "type": "extend_period",
                    "description": f"기간을 {extra_months}개월 연장",
                    "new_period_months": new_period,
                    "monthly_amount": monthly,
                    "expected_total": new_total,
                    "achievable": True,
                }
            )
            break

    # 2. 월 납입액 증가 옵션들
    required_monthly = goal_math.get("required_monthly_amount") or 0
    if required_monthly > monthly:
        extra_needed = required_monthly - monthly
        plans.append(
            {
                "type": "increase_monthly",
                "description": f"월 납입액을 {extra_needed:,}원 추가",
                "new_monthly_amount": required_monthly,
                "period_months": period,
                "expected_total": current + (required_monthly * period),
                "achievable": True,
            }
        )

    # 3. 목표 금액 하향 옵션
    achievable_target = current + (monthly * period)
    if achievable_target < target:
        plans.append(
            {
                "type": "reduce_target",
                "description": f"현재 조건으로 달성 가능한 목표",
                "achievable_target": achievable_target,
                "original_target": target,
                "reduction_rate": round((1 - achievable_target / target) * 100, 1),
            }
        )

    # 4. 복합 전략 (기간 + 금액 조정)
    for new_period in [period + 6, period + 12]:
        for increase_rate in [1.2, 1.5]:  # 20%, 50% 증가
            new_monthly = int(monthly * increase_rate)
            new_total = current + (new_monthly * new_period)
            if new_total >= target:
                plans.append(
                    {
                        "type": "combined",
                        "description": f"기간 {new_period}개월 + 월 {new_monthly:,}원",
                        "new_period_months": new_period,
                        "new_monthly_amount": new_monthly,
                        "expected_total": new_total,
                        "achievable": True,
                    }
                )
                break

    return plans


def find_products_for_alternative_plan(plan: dict, current_savings: int = 0) -> dict:
    """
    대안 플랜에 맞는 실제 가입 가능한 상품 찾기
    """
    from products.models import DepositOption, SavingOption

    plan_type = plan.get("type")
    result = {"deposit": None, "saving": None}

    # 대안 플랜의 기간 결정
    if plan_type == "extend_period":
        target_period = plan.get("new_period_months", 12)
    elif plan_type == "increase_monthly":
        target_period = plan.get("period_months", 12)
    elif plan_type == "reduce_target":
        target_period = plan.get("period_months", 12)
    elif plan_type == "combined":
        target_period = plan.get("new_period_months", 12)
    else:
        target_period = 12

    # 해당 기간에 가장 가까운 상품 찾기
    terms = _pick_terms_near(SavingOption, target_period)

    if terms:
        # 적금: 해당 기간의 최고 금리 상품
        best_saving = (
            SavingOption.objects.select_related("product")
            .filter(save_trm__in=terms)
            .order_by("-intr_rate2", "-intr_rate")
            .first()
        )
        if best_saving:
            p = best_saving.product
            result["saving"] = {
                "option_id": best_saving.id,
                "product_id": p.id,
                "fin_prdt_cd": p.fin_prdt_cd,
                "bank": p.kor_co_nm,
                "name": p.fin_prdt_nm,
                "rate": float(best_saving.intr_rate2 or best_saving.intr_rate or 0),
                "save_trm": best_saving.save_trm,
            }

    # 예금: 보유금이 있는 경우에만
    if current_savings > 0:
        dep_terms = _pick_terms_near(DepositOption, target_period)
        if dep_terms:
            best_deposit = (
                DepositOption.objects.select_related("product")
                .filter(save_trm__in=dep_terms)
                .order_by("-intr_rate2", "-intr_rate")
                .first()
            )
            if best_deposit:
                p = best_deposit.product
                result["deposit"] = {
                    "option_id": best_deposit.id,
                    "product_id": p.id,
                    "fin_prdt_cd": p.fin_prdt_cd,
                    "bank": p.kor_co_nm,
                    "name": p.fin_prdt_nm,
                    "rate": float(
                        best_deposit.intr_rate2 or best_deposit.intr_rate or 0
                    ),
                    "save_trm": best_deposit.save_trm,
                }

    return result


def build_smart_alternative_plans_with_products(
    user_input: dict,
    goal_math: dict,
) -> list[dict]:
    """
    목표 달성이 불가능할 때 다양한 대안 제시 + 해당 대안에 맞는 상품 추천
    """
    from products.models import DepositOption, SavingOption

    target = int(user_input.get("target_amount") or 0)
    monthly = int(user_input.get("monthly_amount") or 0)
    period = int(user_input.get("period_months") or 0)
    current = int(user_input.get("current_savings") or 0)

    plans = []

    # DB에 존재하는 적금/예금 기간 목록 가져오기
    saving_terms = sorted(
        {
            int(t)
            for t in SavingOption.objects.values_list("save_trm", flat=True).distinct()
            if t
        }
    )
    deposit_terms = sorted(
        {
            int(t)
            for t in DepositOption.objects.values_list("save_trm", flat=True).distinct()
            if t
        }
    )

    # ★ 합리적인 기간 제한: 목표 기간의 2배 또는 +12개월 중 작은 값
    max_allowed_period = min(period * 2, period + 12)

    # 제한된 기간 내의 상품만 필터링
    valid_saving_terms = [t for t in saving_terms if t <= max_allowed_period]

    # 1. 기간 연장 옵션 - 실제 존재하는 상품 기간 기준 (제한된 범위 내)
    for new_period in valid_saving_terms:
        if new_period > period:
            # 해당 기간의 최고 금리 적금 찾기
            best_saving = (
                SavingOption.objects.select_related("product")
                .filter(save_trm=new_period)
                .order_by("-intr_rate2", "-intr_rate")
                .first()
            )
            if best_saving:
                saving_rate = float(
                    best_saving.intr_rate2 or best_saving.intr_rate or 0
                )
                # 이자 포함 총액 계산
                sav_result = calculate_saving_interest(monthly, saving_rate, new_period)
                dep_result = (
                    calculate_deposit_interest(current, 3.5, new_period)
                    if current > 0
                    else {"total": 0, "interest": 0}
                )
                expected_total = sav_result["total"] + dep_result["total"]

                if expected_total >= target:
                    p = best_saving.product
                    plans.append(
                        {
                            "type": "extend_period",
                            "description": f"기간을 {new_period - period}개월 연장 ({new_period}개월)",
                            "new_period_months": new_period,
                            "monthly_amount": monthly,
                            "expected_total": round(expected_total),
                            "expected_interest": round(
                                sav_result["interest"] + dep_result["interest"]
                            ),
                            "achievable": True,
                            "recommended_product": {
                                "kind": "saving",
                                "option_id": best_saving.id,
                                "product_id": p.id,
                                "fin_prdt_cd": p.fin_prdt_cd,
                                "bank": p.kor_co_nm,
                                "name": p.fin_prdt_nm,
                                "rate": saving_rate,
                                "save_trm": new_period,
                            },
                        }
                    )
                    break  # 달성 가능한 첫 번째 기간만

    # 2. 월 납입액 증가 옵션 - 현재 기간에 맞는 상품 기준
    nearest_period = (
        min(saving_terms, key=lambda x: abs(x - period)) if saving_terms else period
    )
    best_saving_current = (
        SavingOption.objects.select_related("product")
        .filter(save_trm=nearest_period)
        .order_by("-intr_rate2", "-intr_rate")
        .first()
    )

    if best_saving_current:
        saving_rate = float(
            best_saving_current.intr_rate2 or best_saving_current.intr_rate or 0
        )
        # 목표 달성에 필요한 월 납입액 역산
        dep_contribution = (
            current + (current * (3.5 / 100) * (nearest_period / 12))
            if current > 0
            else 0
        )
        remaining = target - dep_contribution

        # 적금 이자 고려한 필요 월납입액 계산
        if remaining > 0 and nearest_period > 0:
            # 단순 원금 + 이자 역산
            multiplier = nearest_period + nearest_period * (nearest_period + 1) / 2 * (
                (saving_rate / 100) / 12
            )
            required_monthly = (
                math.ceil(remaining / multiplier) if multiplier > 0 else monthly
            )

            if required_monthly > monthly:
                extra_needed = required_monthly - monthly
                sav_result = calculate_saving_interest(
                    required_monthly, saving_rate, nearest_period
                )
                expected_total = sav_result["total"] + dep_contribution

                p = best_saving_current.product
                plans.append(
                    {
                        "type": "increase_monthly",
                        "description": f"월 납입액을 {extra_needed:,}원 추가",
                        "new_monthly_amount": required_monthly,
                        "period_months": nearest_period,
                        "expected_total": round(expected_total),
                        "expected_interest": round(sav_result["interest"]),
                        "achievable": True,
                        "recommended_product": {
                            "kind": "saving",
                            "option_id": best_saving_current.id,
                            "product_id": p.id,
                            "fin_prdt_cd": p.fin_prdt_cd,
                            "bank": p.kor_co_nm,
                            "name": p.fin_prdt_nm,
                            "rate": saving_rate,
                            "save_trm": nearest_period,
                        },
                    }
                )

    # 3. 목표 금액 하향 옵션
    if best_saving_current and nearest_period > 0:
        saving_rate = float(
            best_saving_current.intr_rate2 or best_saving_current.intr_rate or 0
        )
        sav_result = calculate_saving_interest(monthly, saving_rate, nearest_period)
        dep_result = (
            calculate_deposit_interest(current, 3.5, nearest_period)
            if current > 0
            else {"total": 0, "interest": 0}
        )
        achievable_target = round(sav_result["total"] + dep_result["total"])

        if achievable_target < target:
            p = best_saving_current.product
            plans.append(
                {
                    "type": "reduce_target",
                    "description": f"현재 조건으로 달성 가능한 목표",
                    "achievable_target": achievable_target,
                    "original_target": target,
                    "reduction_rate": round((1 - achievable_target / target) * 100, 1),
                    "period_months": nearest_period,
                    "achievable": True,
                    "recommended_product": {
                        "kind": "saving",
                        "option_id": best_saving_current.id,
                        "product_id": p.id,
                        "fin_prdt_cd": p.fin_prdt_cd,
                        "bank": p.kor_co_nm,
                        "name": p.fin_prdt_nm,
                        "rate": saving_rate,
                        "save_trm": nearest_period,
                    },
                }
            )

    # 4. 복합 전략 (기간 연장 + 금액 증가) - 제한된 범위 내
    increase_rates = [1.2, 1.5]  # 20%, 50% 증가
    combined_added = 0

    for new_period in valid_saving_terms:
        if new_period > period and combined_added < 2:  # 최대 2개만
            best_saving_combo = (
                SavingOption.objects.select_related("product")
                .filter(save_trm=new_period)
                .order_by("-intr_rate2", "-intr_rate")
                .first()
            )
            if best_saving_combo:
                saving_rate = float(
                    best_saving_combo.intr_rate2 or best_saving_combo.intr_rate or 0
                )

                for increase_rate in increase_rates:
                    new_monthly = int(monthly * increase_rate)
                    sav_result = calculate_saving_interest(
                        new_monthly, saving_rate, new_period
                    )
                    dep_result = (
                        calculate_deposit_interest(current, 3.5, new_period)
                        if current > 0
                        else {"total": 0, "interest": 0}
                    )
                    expected_total = sav_result["total"] + dep_result["total"]

                    if expected_total >= target:
                        p = best_saving_combo.product
                        plans.append(
                            {
                                "type": "combined",
                                "description": f"기간 {new_period}개월 + 월 {new_monthly:,}원",
                                "new_period_months": new_period,
                                "new_monthly_amount": new_monthly,
                                "expected_total": round(expected_total),
                                "expected_interest": round(
                                    sav_result["interest"] + dep_result["interest"]
                                ),
                                "achievable": True,
                                "recommended_product": {
                                    "kind": "saving",
                                    "option_id": best_saving_combo.id,
                                    "product_id": p.id,
                                    "fin_prdt_cd": p.fin_prdt_cd,
                                    "bank": p.kor_co_nm,
                                    "name": p.fin_prdt_nm,
                                    "rate": saving_rate,
                                    "save_trm": new_period,
                                },
                            }
                        )
                        combined_added += 1
                        break  # 이 기간에서는 달성 가능한 첫 번째만

                if combined_added >= 2:
                    break

    # 대안 플랜에 기간 제한 정보 추가 (UI 표시용)
    for plan in plans:
        plan["max_allowed_period"] = max_allowed_period
        plan["original_period"] = period

    return plans


# -----------------------------
# 9) 목적별 추가 분석 데이터 생성
# -----------------------------


def build_purpose_specific_data(user_input: dict, purpose: str) -> dict:
    """
    목적별 추가 분석 데이터 생성
    """
    result = {}

    if purpose == "housing":
        result = build_housing_analysis_data(user_input)
    elif purpose == "travel":
        result = build_travel_analysis_data(user_input)
    elif purpose == "savings":
        result = build_savings_analysis_data(user_input)

    return result


def build_housing_analysis_data(user_input: dict) -> dict:
    """
    주택 목적 분석 데이터
    """
    housing_type = user_input.get("housing_type", "")
    target_region = user_input.get("target_region", "")
    target_apartment = user_input.get("target_apartment", "")
    apartment_price = user_input.get("apartment_price") or user_input.get(
        "target_amount", 0
    )

    # 주거 유형별 분석 포인트
    analysis_points = {
        "purchase": {
            "type_name": "매매",
            "tips": [
                "취득세, 중개수수료 등 부대비용 약 3~5% 추가 필요",
                "대출 활용 시 DTI/DSR 규제 확인",
                "등기비용, 이사비용 별도 준비",
            ],
            "additional_cost_rate": 0.05,
        },
        "jeonse": {
            "type_name": "전세",
            "tips": [
                "전세보증보험 가입 권장",
                "계약 전 등기부등본 확인 필수",
                "전세자금대출 활용 시 최대 80% 가능",
            ],
            "additional_cost_rate": 0.02,
        },
        "wolse_deposit": {
            "type_name": "월세 보증금",
            "tips": [
                "보증금 반환 보증보험 가입 검토",
                "월세 환산 시 전세보다 유리한지 계산",
                "임대차 3법 적용 여부 확인",
            ],
            "additional_cost_rate": 0.01,
        },
        "wolse": {
            "type_name": "월세",
            "tips": [
                "월세 세액공제 활용 가능 (총급여 7천만원 이하)",
                "관리비, 공과금 별도 예상",
            ],
            "additional_cost_rate": 0.0,
        },
    }

    type_info = analysis_points.get(housing_type, {})
    additional_cost = int(apartment_price * type_info.get("additional_cost_rate", 0.03))

    return {
        "housing_type": housing_type,
        "housing_type_name": type_info.get("type_name", ""),
        "target_region": target_region,
        "target_apartment": target_apartment,
        "apartment_price": apartment_price,
        "additional_cost": additional_cost,
        "total_needed": apartment_price + additional_cost,
        "tips": type_info.get("tips", []),
        "search_keywords": [
            target_apartment if target_apartment else target_region,
            f"{target_region} 부동산",
            f"{target_region} 아파트 시세",
        ],
    }


def build_travel_analysis_data(user_input: dict) -> dict:
    """
    여행 목적 분석 데이터
    - 나라를 기반으로 여행 뉴스/유튜브 검색 키워드 생성
    """
    destination = user_input.get("travel_destination", "")
    country_code = user_input.get("travel_country_code", "")
    target_amount = int(user_input.get("target_amount") or 0)

    # 주요 여행지별 통화/정보
    destination_info = {
        "JPY": {
            "country": "일본",
            "currency": "JPY",
            "currency_name": "엔",
            "avg_daily_cost": 150000,
            "popular_cities": ["도쿄", "오사카", "교토", "후쿠오카", "삿포로"],
        },
        "USD": {
            "country": "미국",
            "currency": "USD",
            "currency_name": "달러",
            "avg_daily_cost": 250000,
            "popular_cities": ["뉴욕", "LA", "샌프란시스코", "하와이", "라스베가스"],
        },
        "EUR": {
            "country": "유럽",
            "currency": "EUR",
            "currency_name": "유로",
            "avg_daily_cost": 200000,
            "popular_cities": ["파리", "로마", "바르셀로나", "런던", "암스테르담"],
        },
        "CNY": {
            "country": "중국",
            "currency": "CNY",
            "currency_name": "위안",
            "avg_daily_cost": 100000,
            "popular_cities": ["상하이", "베이징", "광저우", "청두", "시안"],
        },
        "THB": {
            "country": "태국",
            "currency": "THB",
            "currency_name": "바트",
            "avg_daily_cost": 80000,
            "popular_cities": ["방콕", "치앙마이", "푸켓", "파타야", "끄라비"],
        },
        "VND": {
            "country": "베트남",
            "currency": "VND",
            "currency_name": "동",
            "avg_daily_cost": 70000,
            "popular_cities": ["다낭", "호치민", "하노이", "나트랑", "푸꾸옥"],
        },
        "TWD": {
            "country": "대만",
            "currency": "TWD",
            "currency_name": "대만 달러",
            "avg_daily_cost": 100000,
            "popular_cities": ["타이페이", "가오슝", "타이중", "화롄", "지우펀"],
        },
        "HKD": {
            "country": "홍콩",
            "currency": "HKD",
            "currency_name": "홍콩 달러",
            "avg_daily_cost": 180000,
            "popular_cities": ["빅토리아 피크", "란타우", "침사추이", "몽콕"],
        },
        "SGD": {
            "country": "싱가포르",
            "currency": "SGD",
            "currency_name": "싱가포르 달러",
            "avg_daily_cost": 200000,
            "popular_cities": ["마리나베이", "센토사", "차이나타운", "오차드로드"],
        },
    }

    # 통화 코드로 정보 찾기
    dest_info = destination_info.get(country_code, {})
    country_name = dest_info.get("country", destination) or destination
    popular_cities = dest_info.get("popular_cities", [])

    # 검색 키워드 생성 - 나라 여행 정보 위주
    search_keywords = []
    if country_name:
        search_keywords = [
            f"{country_name} 여행",  # 네이버 뉴스 검색용
            f"{country_name} 여행 추천",  # 유튜브 검색용
            f"{country_name} 여행지 추천",
        ]

    # 유튜브 검색용 키워드 (추천 여행지 탐색)
    youtube_search_keyword = (
        f"{country_name} 여행 추천 여행지" if country_name else "해외여행 추천"
    )

    return {
        "destination": destination,
        "country_name": country_name,
        "country_code": country_code or "USD",
        "currency_name": dest_info.get("currency_name", ""),
        "target_amount_krw": target_amount,
        "avg_daily_cost": dest_info.get("avg_daily_cost", 150000),
        "estimated_days": (
            target_amount // dest_info.get("avg_daily_cost", 150000)
            if dest_info.get("avg_daily_cost")
            else 0
        ),
        "popular_cities": popular_cities,
        "search_keywords": search_keywords,  # 뉴스 검색용
        "youtube_search_keyword": youtube_search_keyword,  # 유튜브 검색용
        "tips": [
            "환전은 출발 1~2주 전에 환율 추이를 보고 결정",
            "신용카드 해외결제 수수료 확인",
            "여행자보험 가입 권장",
            (
                f"{country_name} 인기 여행지: {', '.join(popular_cities[:3])}"
                if popular_cities
                else ""
            ),
        ],
    }


def build_savings_analysis_data(user_input: dict) -> dict:
    """
    목돈 마련 목적 분석 데이터
    """
    detail = user_input.get("savings_purpose_detail", "")
    target_amount = int(user_input.get("target_amount") or 0)

    # 세부 목적별 팁
    purpose_tips = {
        "결혼": {
            "tips": [
                "결혼 비용 외 신혼집 비용 별도 계획",
                "청년희망적금 등 정책 상품 활용",
            ],
            "avg_cost": 50000000,
        },
        "자동차": {
            "tips": [
                "취등록세, 보험료 등 부대비용 약 10% 추가",
                "중고차 vs 신차 비교 검토",
            ],
            "avg_cost": 30000000,
        },
        "창업": {
            "tips": [
                "창업 자금 대출 상품 검토",
                "예비비 최소 20% 추가 확보 권장",
            ],
            "avg_cost": 50000000,
        },
        "교육": {
            "tips": [
                "교육비 세액공제 활용",
                "장기 교육 저축 상품 검토",
            ],
            "avg_cost": 20000000,
        },
    }

    matched_tips = {}
    for key, info in purpose_tips.items():
        if key in detail:
            matched_tips = info
            break

    return {
        "purpose_detail": detail,
        "target_amount": target_amount,
        "tips": matched_tips.get(
            "tips", ["목표 금액의 10~20%는 예비비로 추가 확보 권장"]
        ),
        "reference_cost": matched_tips.get("avg_cost"),
    }
