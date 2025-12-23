from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import Counter
from backend.services.vector_store import VectorStore
from backend.services.rag_service import RAGService
from backend.models.schemas import AnalysisResponse


class AnalysisService:
    """Service for analyzing financial data."""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.rag_service = RAGService()
    
    def analyze_trends(
        self,
        query: str,
        time_range_days: int = 30,
        data_sources: List[str] = None
    ) -> AnalysisResponse:
        """
        Analyze trends in financial data.
        
        Args:
            query: Analysis query
            time_range_days: Time range in days
            data_sources: Data source filters
        
        Returns:
            AnalysisResponse with trend analysis
        """
        # Search for relevant documents
        results = self.vector_store.search(
            query=query,
            collection_names=data_sources,
            top_k=20
        )
        
        # Analyze trends
        insights = []
        data_points = []
        
        # Count mentions by source type
        source_types = Counter([r["metadata"].get("type") for r in results])
        
        insights.append(
            f"최근 {time_range_days}일간 '{query}' 관련 데이터: "
            f"뉴스 {source_types.get('news', 0)}건, "
            f"유튜브 {source_types.get('youtube', 0)}건, "
            f"금융상품 {source_types.get('deposit', 0) + source_types.get('savings', 0)}건"
        )
        
        # Analyze by time if available
        dates = []
        for r in results:
            if "published_at" in r["metadata"]:
                try:
                    date = datetime.fromisoformat(r["metadata"]["published_at"])
                    dates.append(date)
                except:
                    pass
        
        if dates:
            recent_count = sum(1 for d in dates if d > datetime.now() - timedelta(days=7))
            insights.append(
                f"최근 7일간 관련 콘텐츠가 {recent_count}건 게시되어 "
                f"관심이 {'높은' if recent_count > len(dates) * 0.3 else '꾸준한'} 상태입니다."
            )
        
        # Extract key products if financial products are included
        products = [r for r in results if r["metadata"].get("type") in ["deposit", "savings"]]
        if products:
            # Find highest interest rate
            max_rate = max(
                products,
                key=lambda x: x["metadata"].get("max_interest_rate", 0)
            )
            insights.append(
                f"최고 금리 상품: {max_rate['metadata']['bank_name']} "
                f"{max_rate['metadata']['product_name']} "
                f"({max_rate['metadata']['max_interest_rate']}%)"
            )
            
            # Average interest rate
            avg_rate = sum(
                p["metadata"].get("interest_rate", 0) for p in products
            ) / len(products)
            insights.append(f"평균 기본 금리: {avg_rate:.2f}%")
        
        # Generate summary
        summary = f"'{query}'에 대한 트렌드 분석 결과입니다. " + " ".join(insights[:2])
        
        # Prepare data points
        for r in results[:10]:
            data_points.append({
                "type": r["metadata"].get("type"),
                "title": r["metadata"].get("title") or r["metadata"].get("product_name"),
                "source": r["metadata"].get("source") or r["metadata"].get("bank_name"),
                "relevance_score": 1 - r["distance"]  # Convert distance to similarity
            })
        
        return AnalysisResponse(
            analysis_type="trend",
            summary=summary,
            insights=insights,
            data_points=data_points
        )
    
    def analyze_sentiment(
        self,
        query: str,
        time_range_days: int = 30
    ) -> AnalysisResponse:
        """
        Analyze sentiment in news and YouTube content.
        
        Args:
            query: Analysis query
            time_range_days: Time range in days
        
        Returns:
            AnalysisResponse with sentiment analysis
        """
        # Search news and YouTube
        results = self.vector_store.search(
            query=query,
            collection_names=["news", "youtube"],
            top_k=15
        )
        
        insights = []
        data_points = []
        
        # Simple sentiment analysis based on keywords
        positive_keywords = ["상승", "증가", "호조", "긍정", "성장", "기회", "추천"]
        negative_keywords = ["하락", "감소", "부진", "위험", "주의", "하락세"]
        
        positive_count = 0
        negative_count = 0
        
        for r in results:
            doc = r["document"].lower()
            pos_score = sum(1 for kw in positive_keywords if kw in doc)
            neg_score = sum(1 for kw in negative_keywords if kw in doc)
            
            if pos_score > neg_score:
                positive_count += 1
                sentiment = "positive"
            elif neg_score > pos_score:
                negative_count += 1
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            data_points.append({
                "title": r["metadata"].get("title"),
                "sentiment": sentiment,
                "type": r["metadata"].get("type")
            })
        
        neutral_count = len(results) - positive_count - negative_count
        
        # Determine overall sentiment
        if positive_count > negative_count:
            overall = "긍정적"
        elif negative_count > positive_count:
            overall = "부정적"
        else:
            overall = "중립적"
        
        insights.append(
            f"'{query}' 관련 콘텐츠의 전반적인 정서는 {overall}입니다."
        )
        insights.append(
            f"긍정: {positive_count}건, 중립: {neutral_count}건, 부정: {negative_count}건"
        )
        
        summary = (
            f"최근 {time_range_days}일간 '{query}' 관련 뉴스 및 유튜브 콘텐츠 {len(results)}건을 분석한 결과, "
            f"{overall} 정서가 우세한 것으로 나타났습니다."
        )
        
        return AnalysisResponse(
            analysis_type="sentiment",
            summary=summary,
            insights=insights,
            data_points=data_points
        )
    
    def recommend_products(
        self,
        query: str,
        product_type: str = None,
        min_interest_rate: float = 0.0
    ) -> AnalysisResponse:
        """
        Recommend financial products based on query.
        
        Args:
            query: User requirements
            product_type: Filter by product type (deposit/savings)
            min_interest_rate: Minimum interest rate filter
        
        Returns:
            AnalysisResponse with product recommendations
        """
        # Search financial products
        collection_names = []
        if product_type:
            collection_names = [product_type]
        else:
            collection_names = ["deposit", "savings"]
        
        results = self.vector_store.search(
            query=query,
            collection_names=collection_names,
            top_k=10
        )
        
        # Filter by interest rate
        filtered = [
            r for r in results
            if r["metadata"].get("interest_rate", 0) >= min_interest_rate
        ]
        
        insights = []
        recommendations = []
        data_points = []
        
        if not filtered:
            insights.append("조건에 맞는 상품을 찾을 수 없습니다.")
        else:
            # Top 5 recommendations
            top_products = sorted(
                filtered[:5],
                key=lambda x: x["metadata"].get("max_interest_rate", 0),
                reverse=True
            )
            
            for idx, p in enumerate(top_products, 1):
                meta = p["metadata"]
                recommendation = (
                    f"{idx}. {meta['bank_name']} - {meta['product_name']}: "
                    f"기본금리 {meta['interest_rate']}%, "
                    f"최고금리 {meta['max_interest_rate']}%, "
                    f"기간 {meta['period_months']}개월"
                )
                recommendations.append(recommendation)
                
                data_points.append({
                    "rank": idx,
                    "bank": meta["bank_name"],
                    "product": meta["product_name"],
                    "base_rate": meta["interest_rate"],
                    "max_rate": meta["max_interest_rate"],
                    "period": meta["period_months"],
                    "url": meta.get("url")
                })
            
            avg_rate = sum(
                p["metadata"]["interest_rate"] for p in top_products
            ) / len(top_products)
            
            insights.append(f"추천 상품의 평균 기본금리: {avg_rate:.2f}%")
            insights.append(
                f"최고 금리 상품: {top_products[0]['metadata']['bank_name']} "
                f"{top_products[0]['metadata']['product_name']}"
            )
        
        summary = f"'{query}' 조건에 맞는 금융 상품 {len(filtered)}개를 찾았습니다."
        
        return AnalysisResponse(
            analysis_type="recommendation",
            summary=summary,
            insights=insights,
            data_points=data_points,
            recommendations=recommendations
        )
