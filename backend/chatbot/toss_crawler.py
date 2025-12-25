"""
파일명: chatbot/toss_crawler.py
설명: 토스증권 커뮤니티 크롤링 모듈

기능:
    - Selenium을 사용한 토스증권 커뮤니티 댓글 크롤링
    - 종목 검색 및 댓글 수집
    - 크롤링 결과 캐싱 (DB)

주의사항:
    - webdriver-manager가 자동으로 ChromeDriver를 관리합니다
    - Chrome 브라우저만 설치되어 있으면 됩니다
"""

import time
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver():
    """Chrome WebDriver 설정 및 반환 (webdriver-manager 사용으로 자동 설치)"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 서버에서 GUI 없이 실행
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # 이미지 로딩 비활성화 (속도 향상)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # webdriver-manager가 자동으로 ChromeDriver 다운로드 및 관리
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def fetch_toss_comments(company_name: str, limit: int = 20, max_scroll: int = 10) -> dict:
    """
    토스증권 커뮤니티에서 특정 종목의 댓글을 크롤링합니다.
    
    Args:
        company_name: 검색할 회사명 (예: "삼성전자", "애플")
        limit: 수집할 최대 댓글 수
        max_scroll: 최대 스크롤 횟수
    
    Returns:
        {
            "success": bool,
            "stock_code": str,
            "company_name": str,
            "comments": list[str],
            "error": str (실패 시)
        }
    """
    driver = None
    
    try:
        driver = get_chrome_driver()
        
        # 1) 토스증권 메인 페이지 접속
        print(f"[크롤링] 토스증권 접속 시작: {company_name}")
        driver.get("https://www.tossinvest.com/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(1)
        
        # 2) 검색창 활성화 ('/' 키로 검색창 열기)
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys("/")
        
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
            )
        )
        
        # 3) 종목 검색
        search_input.click()
        search_input.clear()
        search_input.send_keys(company_name)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        print(f"[크롤링] 검색어 입력 완료: {company_name}")
        
        # 4) /order 페이지 로딩 대기 (종목 상세 페이지)
        try:
            WebDriverWait(driver, 15).until(EC.url_contains("/order"))
        except TimeoutException:
            # 검색 결과가 없거나 다른 페이지로 이동한 경우
            return {
                "success": False,
                "error": f"'{company_name}' 종목을 찾을 수 없습니다.",
                "comments": []
            }
        
        current_url = driver.current_url
        print(f"[크롤링] 종목 페이지 진입: {current_url}")
        
        # 5) URL에서 종목 코드 추출
        stock_code = None
        parts = current_url.split("/")
        if "stocks" in parts:
            idx = parts.index("stocks")
            if idx + 1 < len(parts):
                stock_code = parts[idx + 1]
        
        # 6) 커뮤니티 페이지로 이동
        if stock_code:
            community_url = f"https://www.tossinvest.com/stocks/{stock_code}/community"
        else:
            community_url = current_url.replace("/order", "/community")
        
        driver.get(community_url)
        print(f"[크롤링] 커뮤니티 페이지 이동: {community_url}")
        
        # 7) 댓글 영역 로딩 대기
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "main article"))
            )
        except TimeoutException:
            return {
                "success": True,
                "stock_code": stock_code,
                "company_name": company_name,
                "comments": [],
                "message": "커뮤니티에 댓글이 없습니다."
            }
        
        time.sleep(1)
        
        # 8) 댓글 수집 (스크롤하면서 누적)
        comments = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for scroll_count in range(max_scroll):
            # 현재 화면의 댓글 추출
            # 토스증권 댓글 CSS 선택자 (변경될 수 있음)
            try:
                comment_elements = driver.find_elements(
                    By.CSS_SELECTOR, "article.comment span.tw-1r5dc8g0._60z0ev1"
                )
                
                # 대체 선택자들 시도
                if not comment_elements:
                    comment_elements = driver.find_elements(
                        By.CSS_SELECTOR, "[class*='comment'] span"
                    )
                
                for elem in comment_elements:
                    try:
                        text = elem.text.strip()
                        if text and text not in comments and len(text) > 5:
                            comments.append(text)
                    except:
                        continue
                        
            except Exception as e:
                print(f"[크롤링] 댓글 추출 오류: {e}")
            
            # 목표 개수 도달 시 종료
            if len(comments) >= limit:
                break
            
            # 스크롤 다운
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # 더 이상 스크롤할 내용이 없으면 종료
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        print(f"[크롤링] 댓글 {len(comments)}개 수집 완료")
        
        return {
            "success": True,
            "stock_code": stock_code,
            "company_name": company_name,
            "comments": comments[:limit]
        }
        
    except Exception as e:
        import traceback
        print(f"[크롤링 오류] {traceback.format_exc()}")
        return {
            "success": False,
            "error": f"크롤링 중 오류 발생: {str(e)}",
            "comments": []
        }
        
    finally:
        if driver:
            driver.quit()


def analyze_stock_sentiment(comments: list, company_name: str, client) -> dict:
    """
    OpenAI를 사용하여 댓글들의 감성을 분석하고 매수/매도 의견을 제시합니다.
    
    Args:
        comments: 크롤링된 댓글 목록
        company_name: 종목명
        client: OpenAI 클라이언트
    
    Returns:
        {
            "sentiment": "positive" | "negative" | "neutral",
            "recommendation": "buy" | "sell" | "hold",
            "confidence": float (0.0 ~ 1.0),
            "summary": str,
            "key_opinions": list[str]
        }
    """
    if not comments:
        return {
            "sentiment": "neutral",
            "recommendation": "hold",
            "confidence": 0.3,
            "summary": "분석할 댓글이 충분하지 않습니다.",
            "key_opinions": []
        }
    
    # 댓글들을 하나의 텍스트로 결합
    combined_comments = "\n".join([f"- {c}" for c in comments[:30]])
    
    analysis_prompt = f"""다음은 '{company_name}'에 대한 토스증권 커뮤니티의 투자자 댓글들입니다.

=== 댓글 목록 ===
{combined_comments}

=== 분석 요청 ===
위 댓글들을 분석하여 다음 JSON 형식으로 응답해주세요:

{{
    "sentiment": "positive" | "negative" | "neutral",
    "recommendation": "buy" | "sell" | "hold",
    "confidence": 0.0 ~ 1.0 (분석 신뢰도),
    "summary": "전반적인 여론 요약 (2-3문장)",
    "key_opinions": ["주요 의견 1", "주요 의견 2", "주요 의견 3"],
    "positive_points": ["긍정적 포인트들"],
    "negative_points": ["부정적 포인트들"]
}}

주의사항:
1. 댓글의 전반적인 분위기를 파악하세요
2. 매수(buy), 매도(sell), 보유(hold) 중 하나를 추천하세요
3. 추천의 근거를 명확히 제시하세요
4. 투자는 개인의 판단이라는 점을 인지하세요
"""

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "당신은 주식 시장 감성 분석 전문가입니다. 투자자들의 댓글을 분석하여 객관적인 시장 심리를 파악합니다."
                },
                {"role": "user", "content": analysis_prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # JSON 파싱
        import json
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        return json.loads(result_text)
        
    except Exception as e:
        print(f"[감성 분석 오류] {e}")
        return {
            "sentiment": "neutral",
            "recommendation": "hold",
            "confidence": 0.3,
            "summary": "댓글 분석 중 오류가 발생했습니다.",
            "key_opinions": []
        }
