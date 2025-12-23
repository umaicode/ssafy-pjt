import pytest
from backend.services.vector_store import VectorStore
from backend.models.schemas import NewsArticle, YouTubeVideo, FinancialProduct
from datetime import datetime


@pytest.fixture
def vector_store():
    """Create a VectorStore instance for testing."""
    return VectorStore()


@pytest.fixture
def sample_news():
    """Create sample news articles."""
    return [
        NewsArticle(
            title="금리 인상 소식",
            content="중앙은행이 기준금리를 인상했습니다.",
            source="경제신문",
            url="https://example.com/news1",
            published_at=datetime.now(),
            author="김기자"
        )
    ]


@pytest.fixture
def sample_youtube():
    """Create sample YouTube videos."""
    return [
        YouTubeVideo(
            video_id="test123",
            title="재테크 기초",
            description="초보자를 위한 재테크 가이드",
            channel="금융TV",
            published_at=datetime.now(),
            view_count=1000,
            like_count=50,
            comment_count=10
        )
    ]


@pytest.fixture
def sample_products():
    """Create sample financial products."""
    return [
        FinancialProduct(
            product_type="deposit",
            bank_name="테스트은행",
            product_name="테스트 예금",
            interest_rate=3.5,
            max_interest_rate=3.8,
            period_months=12,
            description="테스트용 예금 상품"
        )
    ]


def test_add_news_articles(vector_store, sample_news):
    """Test adding news articles to vector store."""
    count = vector_store.add_news_articles(sample_news)
    assert count == len(sample_news)


def test_add_youtube_videos(vector_store, sample_youtube):
    """Test adding YouTube videos to vector store."""
    count = vector_store.add_youtube_videos(sample_youtube)
    assert count == len(sample_youtube)


def test_add_financial_products(vector_store, sample_products):
    """Test adding financial products to vector store."""
    count = vector_store.add_financial_products(sample_products)
    assert count == len(sample_products)


def test_search(vector_store, sample_news, sample_youtube, sample_products):
    """Test searching across collections."""
    # Add data
    vector_store.add_news_articles(sample_news)
    vector_store.add_youtube_videos(sample_youtube)
    vector_store.add_financial_products(sample_products)
    
    # Search
    results = vector_store.search("금리", top_k=5)
    assert len(results) > 0
    assert "document" in results[0]
    assert "metadata" in results[0]


def test_get_stats(vector_store):
    """Test getting statistics."""
    stats = vector_store.get_stats()
    assert "news_count" in stats
    assert "youtube_count" in stats
    assert "products_count" in stats
