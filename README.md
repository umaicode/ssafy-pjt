# Financial AI/RAG System (금융 AI/RAG 시스템)

AI와 RAG(Retrieval-Augmented Generation) 기술을 활용한 금융 데이터 분석 시스템입니다. 
뉴스 데이터, YouTube 콘텐츠, 예금/적금 상품 정보를 통합하여 지능적인 금융 분석과 추천을 제공합니다.

## 🎯 주요 기능

### 1. 데이터 수집 (Data Collection)
- **뉴스 수집**: NewsAPI를 통한 실시간 금융 뉴스 수집
- **YouTube 수집**: YouTube Data API를 통한 재테크 관련 동영상 정보 수집
- **금융 상품 수집**: 예금/적금 상품 정보 수집

### 2. RAG 시스템 (Retrieval-Augmented Generation)
- **벡터 데이터베이스**: ChromaDB를 활용한 효율적인 문서 저장 및 검색
- **임베딩**: Sentence Transformers를 통한 고품질 문서 임베딩
- **의미론적 검색**: 사용자 질의에 대한 정확한 문서 검색
- **LLM 통합**: OpenAI GPT를 활용한 자연어 답변 생성

### 3. 분석 기능 (Analysis Features)
- **트렌드 분석**: 시간대별 금융 키워드 트렌드 분석
- **감성 분석**: 뉴스 및 YouTube 콘텐츠의 감성 분석
- **상품 추천**: 사용자 조건에 맞는 예금/적금 상품 추천
- **인사이트 생성**: AI 기반 금융 인사이트 제공

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     사용자 인터페이스                      │
│                    (API / Web UI)                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  FastAPI Backend                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐      │
│  │   RAG    │  │ Analysis │  │  Data Collection │      │
│  │ Service  │  │ Service  │  │     Services     │      │
│  └──────────┘  └──────────┘  └──────────────────┘      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Vector Store (ChromaDB)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐      │
│  │   News   │  │ YouTube  │  │    Financial     │      │
│  │   Data   │  │   Data   │  │    Products      │      │
│  └──────────┘  └──────────┘  └──────────────────┘      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│             External Data Sources                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐      │
│  │ NewsAPI  │  │ YouTube  │  │  FSS Open API    │      │
│  │          │  │   API    │  │  (금융감독원)     │      │
│  └──────────┘  └──────────┘  └──────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

## 🚀 시작하기

### 필수 요구사항
- Python 3.8 이상
- pip (Python 패키지 관리자)

### 설치 방법

1. **저장소 클론**
```bash
git clone <repository-url>
cd ssafy-pjt
```

2. **가상 환경 생성 및 활성화**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **환경 변수 설정**
```bash
cp .env.example .env
```

`.env` 파일을 열어 다음 값들을 설정하세요:
```env
OPENAI_API_KEY=your_openai_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

### 실행 방법

**서버 시작**
```bash
cd backend
python main.py
```

서버가 시작되면 다음 주소에서 접속할 수 있습니다:
- API 서버: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 📚 API 사용 가이드

### 1. 데이터 수집

**모든 데이터 수집**
```bash
curl -X POST "http://localhost:8000/api/collect/all"
```

**뉴스 수집**
```bash
curl -X POST "http://localhost:8000/api/collect/news?query=금융&days=7"
```

**YouTube 수집**
```bash
curl -X POST "http://localhost:8000/api/collect/youtube?query=재테크&max_results=50"
```

**금융 상품 수집**
```bash
curl -X POST "http://localhost:8000/api/collect/financial"
```

### 2. RAG 질의

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "높은 금리의 예금 상품을 추천해주세요",
    "top_k": 5
  }'
```

### 3. 데이터 분석

**트렌드 분석**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "금리 인상",
    "analysis_type": "trend",
    "time_range_days": 30
  }'
```

**감성 분석**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "주식 시장",
    "analysis_type": "sentiment"
  }'
```

**상품 추천**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "단기 고금리 예금",
    "analysis_type": "recommendation"
  }'
```

### 4. 시스템 통계

```bash
curl -X GET "http://localhost:8000/api/stats"
```

## 💡 주제 및 활용 방안

### 추천 주제

1. **개인화된 금융 상담 챗봇**
   - 사용자의 재무 상황에 맞는 예금/적금 상품 추천
   - 최신 금융 뉴스 기반 투자 조언
   - YouTube 콘텐츠를 활용한 금융 교육 자료 제공

2. **금융 트렌드 분석 대시보드**
   - 실시간 금융 키워드 트렌드 분석
   - 뉴스 감성 분석을 통한 시장 심리 파악
   - 금리 변동 예측 및 분석

3. **스마트 재테크 어시스턴트**
   - 목표 금액과 기간에 맞는 저축 플랜 추천
   - 시장 상황에 따른 투자 전략 제안
   - 금융 상품 비교 및 최적 상품 추천

4. **금융 교육 플랫폼**
   - RAG를 활용한 금융 용어 설명
   - YouTube 콘텐츠 큐레이션
   - 초보자를 위한 맞춤형 학습 경로 제공

### 확장 가능한 기능

- **실시간 알림**: 관심 키워드나 금리 변동 시 알림
- **포트폴리오 관리**: 사용자의 금융 상품 포트폴리오 추적
- **소셜 기능**: 사용자 간 투자 아이디어 공유
- **다국어 지원**: 영어, 중국어 등 다국어 콘텐츠 분석
- **음성 인터페이스**: 음성으로 질의하고 답변 받기

## 🛠️ 기술 스택

- **Backend**: FastAPI, Python 3.8+
- **AI/ML**: 
  - OpenAI GPT (LLM)
  - Sentence Transformers (임베딩)
  - LangChain (RAG 프레임워크)
- **Vector Database**: ChromaDB
- **Data Sources**: 
  - NewsAPI (뉴스)
  - YouTube Data API (동영상)
  - 금융감독원 오픈 API (금융 상품)

## 📁 프로젝트 구조

```
ssafy-pjt/
├── backend/
│   ├── api/              # API 엔드포인트
│   ├── services/         # 비즈니스 로직
│   │   ├── news_collector.py
│   │   ├── youtube_collector.py
│   │   ├── financial_collector.py
│   │   ├── vector_store.py
│   │   ├── rag_service.py
│   │   └── analysis_service.py
│   ├── models/           # 데이터 모델
│   │   └── schemas.py
│   ├── utils/            # 유틸리티 함수
│   ├── config.py         # 설정 관리
│   └── main.py           # 애플리케이션 진입점
├── tests/                # 테스트 코드
├── docs/                 # 문서
├── requirements.txt      # Python 의존성
├── .env.example          # 환경 변수 템플릿
└── README.md             # 프로젝트 문서
```

## 🧪 테스트

```bash
pytest tests/
```

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 🤝 기여

이슈나 풀 리퀘스트를 통해 기여해주세요!

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해주세요.
