import json
from django.conf import settings
from openai import OpenAI

# services의 compute_goal_math를 import
from .services import compute_goal_math

SYSTEM_PROMPT = """당신은 한국의 은행 예/적금 상품 추천 전문가입니다.
반드시 제공된 후보(candidates) 안에서만 선택하세요.
반드시 '한국어'로만 답하세요. 영어 사용 금지.
반드시 'JSON만' 반환하세요. 마크다운/추가 텍스트 금지.
"""

def build_user_prompt(user_input: dict, candidates: list[dict], top_k: int = 5) -> str:
    calc = compute_goal_math(user_input)

    schema = f"""
{{
  "summary": "string",
  "goal_math": {{
    "planned_total_amount": number,
    "months_to_goal": number|null,
    "required_monthly_amount": number|null,
    "extra_needed_per_month": number|null,
    "shortfall_amount": number
  }},
  "strategy": "string",
  "recommendations": [
    {{"kind":"deposit|saving","option_id":number,"product_id":number,"fit_score":number,"reason":"string"}}
  ]
}}
""".strip()

    return f"""
[사용자 입력]
- 목적: {user_input["purpose"]}
- 목표기간(개월): {calc["period_months"]}
- 목표금액: {calc["target_amount"]}
- 월납입액: {calc["monthly_amount"]}

[서버 계산 결과(정확값, 수정/재계산 금지)]
- 계획 총 납입액: {calc["planned_total_amount"]}
- 목표 달성까지 예상 개월(올림): {calc["months_to_goal"]}
- 기간 내 달성 가능 여부: {str(calc["achievable_in_period"]).lower()}
- 기간 내 달성 불가 시 부족분: {calc["shortfall_amount"]}
- 기간 내 달성하려면 필요한 월납입액(올림): {calc["required_monthly_amount"]}
- (추가) 기간 내 달성하려면 월납입액 추가 필요분: {calc.get("extra_needed_per_month")}

[후보 목록]
{json.dumps(candidates, ensure_ascii=False)}

[작업]
- 후보 중에서 사용자에게 가장 적합한 TOP {top_k}개를 추천하세요.
- 위 [서버 계산 결과]는 이미 정확히 계산된 값입니다. 너는 계산을 다시 하지 말고,
  이 수치를 근거로 추천 이유/전략만 작성하세요.
- goal_math 필드는 반드시 위 서버 계산 결과를 그대로 복사해서 넣으세요(값 변경 금지).
- 최대금리(max_rate)도 고려하되, 우대조건 난이도를 함께 고려하세요.
- max_limit이 있고 계획금액이 한도를 초과할 가능성이 크면 fit_score를 낮추세요.
- 목표기간과 정확히 일치하는 옵션이 없어도 가장 가까운 기간 옵션을 추천할 수 있습니다.
- recommendations의 kind/product_id는 해당 option_id가 가진 후보 값과 반드시 일치해야 합니다.
  (option_id를 고른 뒤, 그 option_id의 kind/product_id를 candidates에서 그대로 복사하세요.)


[출력 스키마(JSON만)]
{schema}

[규칙]
- recommendations 길이는 반드시 {top_k}
- fit_score는 0.0~1.0
- option_id/product_id/kind는 후보에 존재해야 함
""".strip()


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
