"""
파일명: recommendations/llm.py
설명: GPT API 통합 및 프롬프트 관리 모듈

기능:
    - OpenAI GPT API 호출 (call_gpt_json)
    - 금융 상품 추천 전문가 시스템 프롬프트
    - 사용자 입력 기반 프롬프트 생성 (build_user_prompt)
    - 목적별 컨텍스트 구성 (build_purpose_context)

핵심 구성요소:
    - SYSTEM_PROMPT: GPT가 금융 전문가 역할을 하도록 하는 시스템 프롬프트
    - build_user_prompt: 사용자 입력과 후보 상품을 기반으로 프롬프트 생성
    - call_gpt_json: GPT API 호출 및 JSON 응답 파싱

응답 스키마:
    - summary: 종합 분석 요약
    - strategy: 예금/적금 활용 전략
    - recommendations: 추천 상품 목록
    - alternative_suggestions: 대안 제안
"""

import json
from django.conf import settings
from openai import OpenAI

# services의 compute_goal_math를 import
from .services import compute_goal_math

SYSTEM_PROMPT = """당신은 한국의 은행 예/적금 상품 추천 전문가입니다.
반드시 제공된 후보(candidates) 안에서만 선택하세요.
반드시 '한국어'로만 답하세요. 영어 사용 금지.
반드시 'JSON만' 반환하세요. 마크다운/추가 텍스트 금지.

당신은 사용자의 금융 목표 달성을 위한 최적의 전략을 제시해야 합니다.
- 예금과 적금을 동시에 활용하는 것이 유리한 경우, 그 조합을 추천하세요.
- 목표 달성이 어려운 경우, 대안을 제시하세요.
- 사용자의 목적(주택, 여행, 목돈)에 맞는 맞춤형 조언을 제공하세요.
"""


def build_user_prompt(user_input: dict, candidates: list[dict], top_k: int = 5) -> str:
    # 후보 상품에서 최고 금리 추출
    best_deposit_rate = 3.5
    best_saving_rate = 4.0

    for c in candidates:
        rate = float(c.get("intr_rate2") or c.get("intr_rate") or 0)
        if c.get("kind") == "deposit" and rate > best_deposit_rate:
            best_deposit_rate = rate
        elif c.get("kind") == "saving" and rate > best_saving_rate:
            best_saving_rate = rate

    calc = compute_goal_math(
        user_input, deposit_rate=best_deposit_rate, saving_rate=best_saving_rate
    )
    purpose = user_input.get("purpose", "savings")

    # 목적별 추가 컨텍스트
    purpose_context = build_purpose_context(user_input, purpose)

    schema = f"""
{{
  "summary": "string (종합 분석 요약)",
  "goal_math": {{
    "planned_total_amount": number,
    "months_to_goal": number|null,
    "required_monthly_amount": number|null,
    "extra_needed_per_month": number|null,
    "shortfall_amount": number
  }},
  "strategy": "string (예금/적금 활용 전략)",
  "combination_advice": "string (예금+적금 동시 가입 시 조언, 보유금 활용 전략)",
  "recommendations": [
    {{"kind":"deposit|saving","option_id":number,"product_id":number,"fit_score":number,"reason":"string","usage":"deposit_only|saving_only|combination"}}
  ],
  "alternative_suggestions": [
    {{"type":"string","description":"string","detail":"string"}}
  ],
  "purpose_specific_advice": "string (목적별 맞춤 조언)",
  "ai_verdict": "string (★ summary와 다른 내용! 추천 상품의 핵심 장단점, 가입 시 주의사항, 우대금리 달성 난이도 등 실행 관점의 조언)"
}}
""".strip()

    current_savings = int(user_input.get("current_savings", 0))

    # 세전/세후 정보 추출
    total_before_tax = calc["total_with_interest"]
    total_after_tax = calc.get("total_with_interest_after_tax", total_before_tax)
    tax_amount = calc.get("tax_amount", 0)

    # 달성 가능/불가에 따른 강제 summary prefix
    if calc["achievable_in_period"]:
        surplus = total_before_tax - calc["target_amount"]
        mandatory_summary_start = f"사용자는 {calc['period_months']}개월 내 {calc['target_amount']:,}원의 목표를 달성할 수 있습니다. 보유금 {current_savings:,}원과 월 {calc['monthly_amount']:,}원 납입으로 총 예상금액은 약 {total_before_tax:,}원(세전)으로 목표 대비 약 {surplus:,}원 초과 달성이 가능합니다."
    else:
        mandatory_summary_start = f"현재 조건으로는 목표 달성이 어렵습니다. 약 {calc['shortfall_amount']:,}원이 부족하므로 월납입액 증가 또는 기간 연장이 필요합니다."

    return f"""
[사용자 입력]
- 목적: {user_input.get("purpose", "목돈")}
- 목표기간(개월): {calc["period_months"]}
- 목표금액: {calc["target_amount"]:,}원
- 월납입액: {calc["monthly_amount"]:,}원
- 현재 보유금액(즉시 사용가능): {current_savings:,}원

{purpose_context}

[서버 계산 결과] 절대 변경 금지 - 이 숫자가 정답입니다

┌─────────────────────────────────────────────────────────────┐
│  [자금 계산]                                                  │
│  보유금(예금 예치):      {current_savings:>15,}원               │
│  + 예금 이자(세전):     +{calc.get("deposit_interest", 0):>14,}원               │
│  + 적금 원금:           {calc["planned_total_amount"]:>15,}원               │
│  + 적금 이자(세전):     +{calc.get("saving_interest", 0):>14,}원               │
│  ─────────────────────────────────────                        │
│  = 세전 총 예상금액:    {total_before_tax:>15,}원               │
│  - 이자소득세(15.4%):   -{tax_amount:>14,}원               │
│  = 세후 총 예상금액:    {total_after_tax:>15,}원               │
├─────────────────────────────────────────────────────────────┤
│  [목표 비교]                                                  │
│  목표금액:               {calc["target_amount"]:>15,}원               │
│                                                               │
│  ▶ 판정: {"✅ 달성 가능" if calc["achievable_in_period"] else "❌ 달성 불가"} ({total_before_tax:,}원 {">" if calc["achievable_in_period"] else "<"} {calc["target_amount"]:,}원)     │
└─────────────────────────────────────────────────────────────┘

[필수] summary 필드에 아래 문장을 반드시 포함하세요
{mandatory_summary_start}

[보유금 활용 전략]
- 보유금 {current_savings:,}원은 예금에 예치하여 이자 수익 확보
- 월납입액 {calc['monthly_amount']:,}원은 적금으로 꾸준히 적립
- 예금+적금 동시 활용이 유리

[후보 목록]
{json.dumps(candidates, ensure_ascii=False)}

[작업]
1. 후보 중에서 사용자에게 가장 적합한 TOP {top_k}개를 추천
2. ★ summary 첫 문장은 반드시 위 [필수] 문장으로 시작
3. goal_math는 서버 계산 결과 그대로 복사

[목표 달성 불가 시에만]
- 기간 연장, 월납입 증가, 목표 하향 등 대안을 alternative_suggestions에 제시

[출력 스키마(JSON만)]
{schema}

[규칙]
- recommendations 길이는 반드시 {top_k}
- fit_score는 0.0~1.0
- option_id/product_id/kind는 후보에 존재해야 함
- usage 필드: 해당 상품을 예금용/적금용/조합용 중 어디에 활용하면 좋을지 표시
- purpose_specific_advice: 사용자의 목적({user_input.get("purpose")})에 맞는 구체적 조언
- summary: 목표 달성 가능 여부와 예상 금액 중심의 '분석 요약' (숫자 중심)
- ai_verdict: summary와 절대 중복되지 않는 '실행 조언' (추천 상품들의 우대금리 달성 난이도, 가입 시 주의사항, 조합 활용 팁 등 실질적 조언)
""".strip()


def build_purpose_context(user_input: dict, purpose: str) -> str:
    """목적별 추가 컨텍스트 생성"""

    if purpose == "housing":
        housing_type = user_input.get("housing_type", "")
        target_region = user_input.get("target_region", "")
        target_apartment = user_input.get("target_apartment", "")
        apartment_price = user_input.get("apartment_price", "")

        housing_type_names = {
            "purchase": "매매",
            "jeonse": "전세",
            "wolse_deposit": "월세 보증금",
            "wolse": "월세",
        }

        return f"""
[주택 목적 상세]
- 주거 유형: {housing_type_names.get(housing_type, housing_type)}
- 목표 지역: {target_region or '미정'}
- 목표 아파트: {target_apartment or '미정'}
- 예상 가격: {apartment_price:,}원 (설정된 경우)

[주택 구매/임대 시 고려사항]
- 매매: 취득세, 중개수수료 등 부대비용 3~5% 추가
- 전세: 전세보증보험, 등기부등본 확인
- 월세: 보증금 + 월세 환산 비용 고려
"""

    elif purpose == "travel":
        destination = user_input.get("travel_destination", "")
        country_code = user_input.get("travel_country_code", "")

        return f"""
[여행 목적 상세]
- 여행지: {destination or '미정'}
- 통화: {country_code or '미정'}

[여행 자금 고려사항]
- 기간 내 목표 달성이 중요 (여행 날짜가 정해진 경우)
- 환율 변동 고려하여 약간의 여유 금액 권장
- 단기간일수록 적금보다 예금이 유리할 수 있음
"""

    elif purpose == "savings":
        detail = user_input.get("savings_purpose_detail", "")
        return f"""
[목돈 마련 상세]
- 세부 목적: {detail or '일반 저축'}

[목돈 마련 고려사항]
- 목표 금액의 10~20%는 예비비로 추가 확보 권장
- 장기일수록 금리 높은 상품 선택 유리
"""

    return ""


def build_final_analysis_prompt(
    user_input: dict,
    product_recommendations: list,
    purpose_data: dict,
    news_data: list = None,
    video_data: list = None,
    exchange_rate: dict = None,
) -> str:
    """
    최종 분석을 위한 프롬프트 (뉴스/유튜브/환율 데이터 포함)
    """
    purpose = user_input.get("purpose", "savings")

    context_parts = []

    # 뉴스 데이터
    if news_data:
        news_summary = "\n".join([f"- {n.get('title', '')}" for n in news_data[:5]])
        context_parts.append(
            f"""
[관련 뉴스]
{news_summary}
"""
        )

    # 유튜브 데이터
    if video_data:
        video_summary = "\n".join([f"- {v.get('title', '')}" for v in video_data[:5]])
        context_parts.append(
            f"""
[관련 유튜브 영상]
{video_summary}
"""
        )

    # 환율 정보 (여행 목적)
    if exchange_rate and purpose == "travel":
        context_parts.append(
            f"""
[현재 환율 정보]
- 통화: {exchange_rate.get('currency', '')}
- 환율: {exchange_rate.get('rate', '')}
- 목표 금액 환산: {exchange_rate.get('converted_amount', '')}
"""
        )

    # 부동산 정보 (주택 목적)
    if purpose == "housing" and purpose_data:
        context_parts.append(
            f"""
[부동산 정보]
- 목표 지역: {purpose_data.get('target_region', '')}
- 목표 아파트: {purpose_data.get('target_apartment', '')}
- 예상 가격: {purpose_data.get('apartment_price', '')}
"""
        )

    return f"""
[사용자 목적]: {purpose}
[추천된 금융 상품]: {len(product_recommendations)}개

{chr(10).join(context_parts)}

[분석 요청]
위 정보를 종합하여 다음을 분석해주세요:

1. (주택 목적) 현재 부동산 시장 상황과 구매/임대 타이밍에 대한 의견
2. (여행 목적) 환율 상황과 추천 여행지, 예상 비용
3. (공통) 추천 상품으로 목표 달성 가능성
4. (공통) 주의사항 및 추가 조언

JSON 형식으로 응답:
{{
  "market_analysis": "string (시장/환율 분석)",
  "timing_advice": "string (타이밍 조언)",
  "additional_recommendations": ["string"],
  "warnings": ["string"],
  "final_verdict": "string (최종 종합 판단)"
}}
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
        max_tokens=2000,
        response_format={"type": "json_object"},
    )

    return json.loads(res.choices[0].message.content)
