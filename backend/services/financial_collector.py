import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from backend.models.schemas import FinancialProduct


class FinancialProductCollector:
    """Collector for deposit and savings product data."""
    
    def __init__(self):
        self.base_url = "https://finlife.fss.or.kr"  # Financial Supervisory Service
    
    def collect_deposits(self) -> List[FinancialProduct]:
        """
        Collect deposit product information.
        
        Note: This uses sample data. For real implementation,
        you would need to use the FSS Open API or web scraping.
        
        Returns:
            List of FinancialProduct objects
        """
        return self._get_sample_deposits()
    
    def collect_savings(self) -> List[FinancialProduct]:
        """
        Collect savings product information.
        
        Returns:
            List of FinancialProduct objects
        """
        return self._get_sample_savings()
    
    def _get_sample_deposits(self) -> List[FinancialProduct]:
        """Return sample deposit data."""
        return [
            FinancialProduct(
                product_type="deposit",
                bank_name="KB국민은행",
                product_name="KB Star 정기예금",
                interest_rate=3.50,
                max_interest_rate=3.80,
                period_months=12,
                description="기본금리 3.50%, 우대금리 최고 0.30%p 제공",
                conditions="비대면 가입 시 우대금리 0.10%p, 급여이체 시 0.20%p 추가",
                url="https://example.com/kb-deposit"
            ),
            FinancialProduct(
                product_type="deposit",
                bank_name="신한은행",
                product_name="신한 쏠편한 정기예금",
                interest_rate=3.45,
                max_interest_rate=3.75,
                period_months=12,
                description="쏠(SOL) 앱 전용 상품, 우대금리 최고 0.30%p",
                conditions="신규 가입 고객 0.10%p, 자동이체 등록 0.20%p",
                url="https://example.com/shinhan-deposit"
            ),
            FinancialProduct(
                product_type="deposit",
                bank_name="하나은행",
                product_name="하나머니 정기예금",
                interest_rate=3.40,
                max_interest_rate=3.70,
                period_months=12,
                description="모바일 전용 고금리 정기예금",
                conditions="첫 거래 고객 0.15%p, 거래실적 우대 0.15%p",
                url="https://example.com/hana-deposit"
            ),
            FinancialProduct(
                product_type="deposit",
                bank_name="카카오뱅크",
                product_name="정기예금",
                interest_rate=3.55,
                max_interest_rate=3.85,
                period_months=12,
                description="100% 모바일 정기예금",
                conditions="신규 고객 0.20%p, 26주 적금 가입 시 0.10%p",
                url="https://example.com/kakao-deposit"
            ),
            FinancialProduct(
                product_type="deposit",
                bank_name="토스뱅크",
                product_name="먹이는 정기예금",
                interest_rate=3.60,
                max_interest_rate=3.90,
                period_months=12,
                description="매일 이자를 확인하는 재미있는 예금",
                conditions="첫 가입 0.15%p, 자동이체 3건 이상 0.15%p",
                url="https://example.com/toss-deposit"
            )
        ]
    
    def _get_sample_savings(self) -> List[FinancialProduct]:
        """Return sample savings data."""
        return [
            FinancialProduct(
                product_type="savings",
                bank_name="KB국민은행",
                product_name="KB청년희망적금",
                interest_rate=4.00,
                max_interest_rate=5.00,
                period_months=12,
                description="청년 전용 우대금리 적금 상품",
                conditions="만 19~34세, 기본금리 4.00%, 우대조건 충족 시 최고 5.00%",
                url="https://example.com/kb-youth-savings"
            ),
            FinancialProduct(
                product_type="savings",
                bank_name="신한은행",
                product_name="쏠편한 적금",
                interest_rate=3.80,
                max_interest_rate=4.30,
                period_months=12,
                description="자유적립식 적금",
                conditions="비대면 가입 0.20%p, 급여이체 0.30%p",
                url="https://example.com/shinhan-savings"
            ),
            FinancialProduct(
                product_type="savings",
                bank_name="하나은행",
                product_name="청년도약계좌",
                interest_rate=4.50,
                max_interest_rate=6.00,
                period_months=60,
                description="5년 만기 청년 지원 적금",
                conditions="소득요건 충족 시, 정부 기여금 지원",
                url="https://example.com/hana-youth-account"
            ),
            FinancialProduct(
                product_type="savings",
                bank_name="카카오뱅크",
                product_name="세이프박스 자유적금",
                interest_rate=3.70,
                max_interest_rate=4.20,
                period_months=12,
                description="언제든 자유롭게 입금하는 적금",
                conditions="목표금액 달성 시 0.30%p, 연속 입금 0.20%p",
                url="https://example.com/kakao-savings"
            ),
            FinancialProduct(
                product_type="savings",
                bank_name="토스뱅크",
                product_name="티끌 모아 적금",
                interest_rate=3.90,
                max_interest_rate=4.40,
                period_months=12,
                description="소액으로 시작하는 적금",
                conditions="자동이체 등록 0.25%p, 친구 추천 0.25%p",
                url="https://example.com/toss-savings"
            ),
            FinancialProduct(
                product_type="savings",
                bank_name="우리은행",
                product_name="우리 첫 적금",
                interest_rate=4.10,
                max_interest_rate=4.80,
                period_months=12,
                description="첫 거래 고객 우대 적금",
                conditions="신규 고객 전용, 모바일 가입 시 추가 우대",
                url="https://example.com/woori-first-savings"
            )
        ]
