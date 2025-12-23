# analysis/llm.py
import json
from django.conf import settings
from openai import OpenAI

from .services import validate_plan_advice_payload

PLAN_ADVICE_SYSTEM_PROMPT = """당신은 한국의 금융 전문 상담사입니다.
사용자의 목적/성향과 '이미 계산된 플랜(세후 금액, 부족액, 기간/월납입 대안)'을 바탕으로
가장 적합한 플랜을 선택하고 실행 조언을 제공합니다.

중요 규칙:
1) 반드시 한국어로만 답변
2) 제공된 수치(expected_after_tax, shortfall 등)는 정확값이므로 변경/재계산 금지
3) 반드시 JSON만 출력
4) 플랜(plan_id)은 제공된 목록 중에서만 선택
"""

def call_gpt_json(system_prompt: str, user_prompt: str) -> dict:
    if not getattr(settings, "OPENAI_API_KEY", None):
        raise RuntimeError("OPENAI_API_KEY is not set")
    if not getattr(settings, "OPENAI_BASE_URL", None):
        raise RuntimeError("OPENAI_BASE_URL is not set")

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )

    res = client.chat.completions.create(
        model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=1200,
        response_format={"type": "json_object"},
    )
    return json.loads(res.choices[0].message.content)

def build_plan_advice_prompt(user_input: dict, plan_result: dict) -> str:
    # LLM에게 전달할 “결정 카드”만 간단히 정리(너무 길게 주면 오히려 성능↓)
    plans = []
    for p in plan_result.get("plans", []):
        item = {
            "plan_id": p.get("plan_id"),
            "plan_name": p.get("plan_name"),
            "period_months": p.get("period_months"),
            "monthly_amount": p.get("monthly_amount"),
            "expected_after_tax": p.get("expected_after_tax"),
            "shortfall": p.get("shortfall"),
            "feasibility": p.get("feasibility"),
        }
        if p.get("deposit"):
            d = p["deposit"]
            item["deposit"] = {
                "bank": d["bank"], "name": d["name"], "save_trm": d["save_trm"],
                "max_rate": d["max_rate"],
                "difficulty": d["condition_difficulty"],
                "keywords": d["spcl_cnd_keywords"][:8],
                "join_way": d["join_way"],
                "limit_is_over": d["limit"]["is_over"],
            }
        if p.get("saving"):
            s = p["saving"]
            item["saving"] = {
                "bank": s["bank"], "name": s["name"], "save_trm": s["save_trm"],
                "max_rate": s["max_rate"],
                "difficulty": s["condition_difficulty"],
                "keywords": s["spcl_cnd_keywords"][:8],
                "join_way": s["join_way"],
                "limit_is_over": s["limit"]["is_over"],
            }
        plans.append(item)

    schema = """
{
  "overall_advice": "전체 조언(2~3문장)",
  "best_plan": "A",
  "best_plan_reason": "왜 이 플랜이 사용자에게 가장 맞는지(1~2문장)",
  "plan_recommendations": [
    { "plan_id": "A", "recommendation": "이 플랜 추천 이유", "tips": ["실행 팁1", "팁2"] }
  ],
  "risk_notes": ["주의사항1", "주의사항2"],
  "additional_tips": ["추가 조언1", "추가 조언2"],
  "encouragement": "격려 한 문장"
}
""".strip()

    preferences = user_input.get("preferences") or {}
    # 추천 성향 기본값(프론트에서 안 보내도 동작)
    pref_defaults = {
        "priority": preferences.get("priority", "균형"),  # 금리우선/실행가능성우선/균형
        "card_spending_ok": preferences.get("card_spending_ok", False),
        "prefer_online": preferences.get("prefer_online", True),
        "early_termination_risk": preferences.get("early_termination_risk", "낮음"),  # 높음/낮음
    }

    return f"""
[사용자 입력]
- 목적: {user_input.get("purpose")}
- 현재 보유금: {int(user_input.get("current_amount") or 0):,}원
- 월 납입 가능: {int(user_input.get("monthly_amount") or 0):,}원
- 목표 금액: {int(user_input.get("target_amount") or 0):,}원
- 목표 기간: {int(user_input.get("period_months") or 0)}개월

[사용자 성향(개인화 기준)]
- 우선순위: {pref_defaults["priority"]}
- 카드실적/사용조건 가능: {str(pref_defaults["card_spending_ok"]).lower()}
- 비대면 선호: {str(pref_defaults["prefer_online"]).lower()}
- 중도해지 가능성(리스크): {pref_defaults["early_termination_risk"]}

[Feasibility]
- 상태: {plan_result.get("feasibility", {}).get("status")}
- 메시지: {plan_result.get("feasibility", {}).get("message")}
- 부족액(gap): {plan_result.get("feasibility", {}).get("gap")}

[플랜 후보(이미 계산된 세후 결과, 수정 금지)]
{json.dumps(plans, ensure_ascii=False, indent=2)}

[작업 지시]
- 위 플랜 중 사용자 성향에 가장 맞는 best_plan을 1개 선택하세요.
- priority가 '실행가능성우선'이면 difficulty(우대조건 난이도)가 낮고, limit_is_over가 false인 플랜을 선호하세요.
- priority가 '금리우선'이면 max_rate가 높은 쪽을 선호하되, 중도해지 리스크가 '높음'이면 기간이 긴 상품(혹은 plan D)을 과도하게 밀지 마세요.
- prefer_online=true면 join_way에 모바일/인터넷이 포함된 상품을 선호하세요.
- card_spending_ok=false면 keywords에 카드/실적 관련이 보이면 보수적으로 평가하세요.
- plan_recommendations에는 2~4개 플랜만 포함해도 됩니다. (A/B/D/E 중 선택)

[출력 형식]
반드시 아래 스키마(JSON만)로 출력:
{schema}
""".strip()

def generate_plan_advice(user_input: dict, plan_result: dict) -> dict:
    prompt = build_plan_advice_prompt(user_input, plan_result)
    raw = call_gpt_json(PLAN_ADVICE_SYSTEM_PROMPT, prompt)
    cleaned = validate_plan_advice_payload(raw, plan_result)
    return cleaned
