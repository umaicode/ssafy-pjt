"""
Financial AI RAG System - 사용 예제
"""

import requests
import json

# API 기본 URL
BASE_URL = "http://localhost:8000"


def example_1_collect_data():
    """예제 1: 데이터 수집하기"""
    print("=" * 50)
    print("예제 1: 데이터 수집")
    print("=" * 50)
    
    # 1. 뉴스 수집
    print("\n1. 뉴스 데이터 수집...")
    response = requests.post(
        f"{BASE_URL}/api/collect/news",
        params={"query": "금융 OR 예금 OR 적금", "days": 7}
    )
    print(f"응답: {response.json()}")
    
    # 2. YouTube 수집
    print("\n2. YouTube 데이터 수집...")
    response = requests.post(
        f"{BASE_URL}/api/collect/youtube",
        params={"query": "재테크 금융", "max_results": 30}
    )
    print(f"응답: {response.json()}")
    
    # 3. 금융 상품 수집
    print("\n3. 금융 상품 수집...")
    response = requests.post(f"{BASE_URL}/api/collect/financial")
    print(f"응답: {response.json()}")


def example_2_query_rag():
    """예제 2: RAG 시스템에 질문하기"""
    print("\n" + "=" * 50)
    print("예제 2: RAG 질의")
    print("=" * 50)
    
    queries = [
        "높은 금리의 예금 상품을 추천해주세요",
        "청년을 위한 적금 상품이 있나요?",
        "최근 금리 동향은 어떤가요?",
        "재테크 초보자에게 추천하는 방법은?"
    ]
    
    for query in queries:
        print(f"\n질문: {query}")
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={
                "query": query,
                "top_k": 5,
                "include_metadata": True
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"답변: {data['answer'][:200]}...")
            print(f"참고 자료 수: {len(data['sources'])}")
        else:
            print(f"오류: {response.status_code}")


def example_3_analyze_trends():
    """예제 3: 트렌드 분석"""
    print("\n" + "=" * 50)
    print("예제 3: 트렌드 분석")
    print("=" * 50)
    
    response = requests.post(
        f"{BASE_URL}/api/analyze",
        json={
            "query": "금리 인상",
            "analysis_type": "trend",
            "time_range_days": 30
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n분석 요약: {data['summary']}")
        print("\n주요 인사이트:")
        for idx, insight in enumerate(data['insights'], 1):
            print(f"  {idx}. {insight}")


def example_4_sentiment_analysis():
    """예제 4: 감성 분석"""
    print("\n" + "=" * 50)
    print("예제 4: 감성 분석")
    print("=" * 50)
    
    topics = ["주식 시장", "부동산 투자", "예금 금리"]
    
    for topic in topics:
        print(f"\n주제: {topic}")
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={
                "query": topic,
                "analysis_type": "sentiment",
                "time_range_days": 30
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"분석 결과: {data['summary']}")
            if data['insights']:
                print(f"주요 발견: {data['insights'][0]}")


def example_5_product_recommendation():
    """예제 5: 상품 추천"""
    print("\n" + "=" * 50)
    print("예제 5: 금융 상품 추천")
    print("=" * 50)
    
    scenarios = [
        "단기 고금리 예금",
        "청년 우대 적금",
        "장기 저축 상품"
    ]
    
    for scenario in scenarios:
        print(f"\n시나리오: {scenario}")
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={
                "query": scenario,
                "analysis_type": "recommendation"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"분석: {data['summary']}")
            if data.get('recommendations'):
                print("\n추천 상품:")
                for rec in data['recommendations'][:3]:
                    print(f"  - {rec}")


def example_6_get_statistics():
    """예제 6: 시스템 통계 확인"""
    print("\n" + "=" * 50)
    print("예제 6: 시스템 통계")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/api/stats")
    
    if response.status_code == 200:
        data = response.json()
        print("\n시스템 상태:")
        print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """메인 함수 - 모든 예제 실행"""
    print("\n🚀 Financial AI RAG System - 사용 예제")
    print("=" * 50)
    
    try:
        # 서버 연결 확인
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code != 200:
            print("❌ 서버에 연결할 수 없습니다.")
            print("서버를 먼저 시작해주세요: python backend/main.py")
            return
        
        print("✅ 서버 연결 성공\n")
        
        # 예제 실행
        # example_1_collect_data()  # 데이터 수집 (시간이 걸릴 수 있음)
        example_2_query_rag()
        example_3_analyze_trends()
        example_4_sentiment_analysis()
        example_5_product_recommendation()
        example_6_get_statistics()
        
        print("\n" + "=" * 50)
        print("✨ 모든 예제가 완료되었습니다!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다.")
        print("서버를 먼저 시작해주세요: python backend/main.py")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()
