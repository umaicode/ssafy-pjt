from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DataSource(str, Enum):
    """Data source types."""
    NEWS = "news"
    YOUTUBE = "youtube"
    DEPOSIT = "deposit"
    SAVINGS = "savings"


class NewsArticle(BaseModel):
    """News article model."""
    id: Optional[str] = None
    title: str
    content: str
    source: str
    url: str
    published_at: datetime
    author: Optional[str] = None
    category: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class YouTubeVideo(BaseModel):
    """YouTube video model."""
    id: Optional[str] = None
    video_id: str
    title: str
    description: str
    channel: str
    published_at: datetime
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FinancialProduct(BaseModel):
    """Financial product (deposit/savings) model."""
    id: Optional[str] = None
    product_type: str  # deposit or savings
    bank_name: str
    product_name: str
    interest_rate: float
    max_interest_rate: Optional[float] = None
    period_months: int
    description: str
    conditions: Optional[str] = None
    url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryRequest(BaseModel):
    """Query request model for RAG system."""
    query: str
    source_filters: Optional[List[DataSource]] = None
    top_k: int = Field(default=5, ge=1, le=20)
    include_metadata: bool = True


class QueryResponse(BaseModel):
    """Query response model."""
    query: str
    answer: str
    sources: List[Dict[str, Any]]
    confidence_score: Optional[float] = None


class AnalysisRequest(BaseModel):
    """Analysis request model."""
    query: str
    analysis_type: str  # trend, sentiment, recommendation, insight
    time_range_days: int = Field(default=30, ge=1, le=365)
    data_sources: Optional[List[DataSource]] = None


class AnalysisResponse(BaseModel):
    """Analysis response model."""
    analysis_type: str
    summary: str
    insights: List[str]
    data_points: List[Dict[str, Any]]
    recommendations: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.now)
