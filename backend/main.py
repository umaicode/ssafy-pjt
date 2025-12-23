from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

from backend.config import get_settings
from backend.models.schemas import (
    QueryRequest, QueryResponse,
    AnalysisRequest, AnalysisResponse
)
from backend.services.news_collector import NewsCollector
from backend.services.youtube_collector import YouTubeCollector
from backend.services.financial_collector import FinancialProductCollector
from backend.services.vector_store import VectorStore
from backend.services.rag_service import RAGService
from backend.services.analysis_service import AnalysisService

# Initialize app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI/RAG 기반 금융 분석 시스템"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
vector_store = VectorStore()
rag_service = RAGService()
analysis_service = AnalysisService()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Financial AI RAG System API",
        "version": settings.app_version,
        "endpoints": {
            "docs": "/docs",
            "query": "/api/query",
            "analyze": "/api/analyze",
            "collect": "/api/collect",
            "stats": "/api/stats"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "vector_store": "operational",
            "rag_service": "operational",
            "analysis_service": "operational"
        }
    }


@app.post("/api/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system.
    
    Args:
        request: Query request with search parameters
    
    Returns:
        QueryResponse with answer and sources
    """
    try:
        response = rag_service.query(
            query=request.query,
            source_filters=request.source_filters,
            top_k=request.top_k,
            include_metadata=request.include_metadata
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_data(request: AnalysisRequest):
    """
    Analyze financial data.
    
    Args:
        request: Analysis request with parameters
    
    Returns:
        AnalysisResponse with analysis results
    """
    try:
        if request.analysis_type == "trend":
            response = analysis_service.analyze_trends(
                query=request.query,
                time_range_days=request.time_range_days,
                data_sources=request.data_sources
            )
        elif request.analysis_type == "sentiment":
            response = analysis_service.analyze_sentiment(
                query=request.query,
                time_range_days=request.time_range_days
            )
        elif request.analysis_type == "recommendation":
            response = analysis_service.recommend_products(
                query=request.query
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown analysis type: {request.analysis_type}"
            )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/collect/news")
async def collect_news(
    background_tasks: BackgroundTasks,
    query: str = "금융 OR 투자 OR 예금 OR 적금",
    days: int = 7
):
    """
    Collect news articles and add to vector store.
    
    Args:
        query: Search query for news
        days: Number of days to look back
    
    Returns:
        Collection status
    """
    def collect_and_store():
        collector = NewsCollector()
        articles = collector.collect_from_newsapi(query=query, days=days)
        count = vector_store.add_news_articles(articles)
        print(f"Collected and stored {count} news articles")
    
    background_tasks.add_task(collect_and_store)
    
    return {
        "status": "started",
        "message": f"News collection started for query: {query}"
    }


@app.post("/api/collect/youtube")
async def collect_youtube(
    background_tasks: BackgroundTasks,
    query: str = "재테크 금융 투자 예금 적금",
    max_results: int = 50,
    days: int = 30
):
    """
    Collect YouTube videos and add to vector store.
    
    Args:
        query: Search query
        max_results: Maximum number of results
        days: Number of days to look back
    
    Returns:
        Collection status
    """
    def collect_and_store():
        collector = YouTubeCollector()
        videos = collector.search_videos(
            query=query,
            max_results=max_results,
            days=days
        )
        count = vector_store.add_youtube_videos(videos)
        print(f"Collected and stored {count} YouTube videos")
    
    background_tasks.add_task(collect_and_store)
    
    return {
        "status": "started",
        "message": f"YouTube collection started for query: {query}"
    }


@app.post("/api/collect/financial")
async def collect_financial(background_tasks: BackgroundTasks):
    """
    Collect financial products and add to vector store.
    
    Returns:
        Collection status
    """
    def collect_and_store():
        collector = FinancialProductCollector()
        deposits = collector.collect_deposits()
        savings = collector.collect_savings()
        
        deposit_count = vector_store.add_financial_products(deposits)
        savings_count = vector_store.add_financial_products(savings)
        
        total = deposit_count + savings_count
        print(f"Collected and stored {total} financial products")
    
    background_tasks.add_task(collect_and_store)
    
    return {
        "status": "started",
        "message": "Financial product collection started"
    }


@app.post("/api/collect/all")
async def collect_all(background_tasks: BackgroundTasks):
    """
    Collect all data types.
    
    Returns:
        Collection status
    """
    def collect_all_data():
        # Collect news
        news_collector = NewsCollector()
        articles = news_collector.collect_from_newsapi()
        vector_store.add_news_articles(articles)
        
        # Collect YouTube
        youtube_collector = YouTubeCollector()
        videos = youtube_collector.search_videos()
        vector_store.add_youtube_videos(videos)
        
        # Collect financial products
        financial_collector = FinancialProductCollector()
        deposits = financial_collector.collect_deposits()
        savings = financial_collector.collect_savings()
        vector_store.add_financial_products(deposits)
        vector_store.add_financial_products(savings)
        
        print("All data collection completed")
    
    background_tasks.add_task(collect_all_data)
    
    return {
        "status": "started",
        "message": "Collecting all data types"
    }


@app.get("/api/stats")
async def get_stats():
    """
    Get system statistics.
    
    Returns:
        System statistics
    """
    try:
        rag_stats = rag_service.get_statistics()
        return {
            "status": "ok",
            "statistics": rag_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
