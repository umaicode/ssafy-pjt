import re, math
from typing import Any, Dict, List, Tuple, Optional

def compute_goal_math(user_input: dict) -> dict:
    period = int(user_input.get("period_months") or 0)
    target = int(user_input.get("target_amount") or 0)
    monthly = int(user_input.get("monthly_amount") or 0)

    planned_total = monthly * period if (monthly > 0 and period > 0) else 0

    months_to_goal = math.ceil(target / monthly) if (target > 0 and monthly > 0) else None
    required_monthly = math.ceil(target / period) if (target > 0 and period > 0) else None

    achievable = (planned_total >= target) if (target > 0 and monthly > 0 and period > 0) else False
    shortfall = max(0, target - planned_total) if (target > 0 and monthly > 0 and period > 0) else target

    extra_needed_per_month = None
    if required_monthly is not None:
        extra_needed_per_month = max(0, required_monthly - monthly)

    return {
        "period_months": period,
        "target_amount": target,
        "monthly_amount": monthly,
        "planned_total_amount": planned_total,
        "months_to_goal": months_to_goal,
        "required_monthly_amount": required_monthly,
        "extra_needed_per_month": extra_needed_per_month,  # ✅ “얼마 더 내야?”
        "achievable_in_period": achievable,
        "shortfall_amount": shortfall,
    }

# -----------------------------
# 1) 우대조건 키워드 추출/난이도
# -----------------------------

EASY_KWS = ["자동이체", "비대면", "모바일", "앱", "인터넷", "스마트폰", "첫거래", "신규"]
HARD_KWS = ["카드", "신용카드", "체크카드", "카드실적", "사용실적", "결제", "이용실적", "실적"]

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
    s = (join_way or "")
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
    penalty += hard_cnt * 0.08     # 어려운 키워드 하나당 -0.08
    penalty -= easy_cnt * 0.03     # 쉬운 키워드 하나당 +0.03 (감점 감소)
    return penalty

# -----------------------------
# 2) 달성가능성(feasibility)
# -----------------------------

def feasibility_score(period_months: int, target_amount: int, monthly_amount: int) -> float:
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

def limit_fitness(max_limit: int | None, target_amount: int, monthly_amount: int, period_months: int) -> float:
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
    rscore = rate_score(getattr(opt, "intr_rate", 0), getattr(opt, "intr_rate2", 0))  # 0~1

    # 3) 채널 가산
    cbonus = channel_bonus(getattr(p, "join_way", ""))  # 0~0.17

    # 4) 우대조건 난이도 감점
    cpen = condition_penalty(getattr(p, "spcl_cnd", ""))  # 0~(대략 0.4)

    # 5) 한도 적합성 (옵션에 존재)
    lfit = limit_fitness(getattr(opt, "max_limit", None), target_amount, monthly_amount, period_months)  # -0.25~+0.1

    # ✅ 가중치 조합 (너가 원하는대로 조정 가능)
    # 달성가능성을 가장 중요하게(0.55), 금리(0.35), 나머지 보정
    final = (
        0.55 * feas +
        0.35 * rscore +
        1.00 * cbonus +
        1.00 * lfit -
        1.00 * cpen +
        1.00 * tadj
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


def pick_candidates_scored(user_input: Dict[str, Any], dep_limit: int = 80, sav_limit: int = 80, top_n: int = 60):
    from products.models import DepositOption, SavingOption

    user_period = int(user_input["period_months"])

    dep_terms = _pick_terms_near(DepositOption, user_period)
    sav_terms = _pick_terms_near(SavingOption, user_period)

    dep_qs = (
        DepositOption.objects
        .select_related("product")
        .filter(save_trm__in=dep_terms)
    )[:dep_limit]

    sav_qs = (
        SavingOption.objects
        .select_related("product")
        .filter(save_trm__in=sav_terms)
    )[:sav_limit]

    scored: List[Tuple[float, Any, str, Dict[str, Any]]] = []

    for opt in dep_qs:
        s, dbg = candidate_score(opt, "deposit", user_input)
        scored.append((s, opt, "deposit", dbg))

    for opt in sav_qs:
        s, dbg = candidate_score(opt, "saving", user_input)
        scored.append((s, opt, "saving", dbg))

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
        # 후보 전체를 넣으면 길어지니까 option_id만 사용
        "candidate_option_ids": [c.get("option_id") for c in candidates],
        "v": 3,  # 로직 바뀌면 버전 올려서 캐시 무효화
    }
    s = json.dumps(base, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def validate_reco_payload(payload: dict, candidates: list[dict], top_k: int = 5) -> dict:
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

        cleaned_items.append({
            "kind": kind,
            "option_id": oid,
            "product_id": pid,
            "fit_score": score,
            "reason": reason,
        })
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
            cleaned_items.append({
                "kind": c["kind"],
                "option_id": oid,
                "product_id": int(c["product_id"]),
                "fit_score": 0.50,
                "reason": "LLM 출력이 일부 불완전하여 내부 점수(pre_score) 기준으로 보완 추천했습니다.",
            })
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



def build_alternative_plans(user_input: dict, months_list=(3, 6, 12, 24, 36)) -> list[dict]:
    target = int(user_input.get("target_amount") or 0)
    monthly = int(user_input.get("monthly_amount") or 0)

    plans = []
    for m in months_list:
        required = math.ceil(target / m) if (target > 0 and m > 0) else None
        extra = max(0, required - monthly) if (required is not None and monthly > 0) else None
        plans.append({
            "period_months": m,
            "required_monthly_amount": required,
            "extra_needed_per_month": extra,
        })
    return plans
