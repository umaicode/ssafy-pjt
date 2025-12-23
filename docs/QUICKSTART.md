# 빠른 시작 가이드

## 1분만에 시작하기

### 1단계: 설치

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```bash
setup.bat
```

### 2단계: API 키 설정

`.env` 파일을 열어 API 키를 입력하세요:

```env
OPENAI_API_KEY=your_key_here
YOUTUBE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

> 💡 **팁**: API 키가 없어도 샘플 데이터로 테스트할 수 있습니다!

### 3단계: 서버 시작

```bash
# 가상 환경 활성화 (Linux/Mac)
source venv/bin/activate

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# 서버 시작
python backend/main.py
```

### 4단계: 브라우저에서 확인

- API 문서: http://localhost:8000/docs
- 헬스 체크: http://localhost:8000/api/health

---

## 첫 번째 질의하기

### 방법 1: API 문서 사용

1. http://localhost:8000/docs 접속
2. `/api/collect/all` 엔드포인트 클릭
3. "Try it out" 버튼 클릭
4. "Execute" 버튼 클릭 (데이터 수집)
5. `/api/query` 엔드포인트로 질문하기

### 방법 2: Python 스크립트 사용

```bash
python docs/examples.py
```

### 방법 3: cURL 사용

```bash
# 1. 데이터 수집
curl -X POST "http://localhost:8000/api/collect/all"

# 2. 질문하기
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "높은 금리의 예금 상품을 추천해주세요",
    "top_k": 5
  }'
```

---

## 주요 기능 테스트

### 1. RAG 질의

```python
import requests

response = requests.post(
    "http://localhost:8000/api/query",
    json={
        "query": "청년을 위한 적금 상품이 있나요?",
        "top_k": 5
    }
)

print(response.json()["answer"])
```

### 2. 트렌드 분석

```python
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={
        "query": "금리 인상",
        "analysis_type": "trend",
        "time_range_days": 30
    }
)

print(response.json()["summary"])
```

### 3. 상품 추천

```python
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={
        "query": "단기 고금리 예금",
        "analysis_type": "recommendation"
    }
)

for rec in response.json()["recommendations"]:
    print(rec)
```

---

## 문제 해결

### Q: 서버가 시작되지 않아요
A: 
1. Python 3.8 이상이 설치되어 있는지 확인
2. 가상 환경이 활성화되어 있는지 확인
3. 의존성이 모두 설치되었는지 확인: `pip install -r requirements.txt`

### Q: API 키가 없어도 사용할 수 있나요?
A: 네! API 키 없이도 샘플 데이터로 모든 기능을 테스트할 수 있습니다.

### Q: 데이터가 저장되나요?
A: 네, ChromaDB에 영구 저장됩니다. `chroma_db/` 디렉토리를 삭제하면 초기화됩니다.

### Q: OpenAI API를 사용하지 않을 수 있나요?
A: 네, API 키 없이도 기본 답변 생성 기능을 사용할 수 있습니다.

---

## 다음 단계

1. **커스터마이징**: `backend/config.py`에서 설정 변경
2. **데이터 추가**: 자신만의 데이터 소스 추가
3. **프론트엔드 개발**: React/Vue.js로 UI 구축
4. **배포**: Docker로 컨테이너화 및 클라우드 배포

---

## 추가 자료

- 📖 [전체 문서](README.md)
- 🎯 [구현 가이드](docs/IMPLEMENTATION_GUIDE.md)
- 💻 [예제 코드](docs/examples.py)
- 🐛 [이슈 리포트](https://github.com/your-repo/issues)
