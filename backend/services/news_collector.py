import requests
import feedparser
from typing import List, Optional
from datetime import datetime, timedelta
from backend.models.schemas import NewsArticle
from backend.config import get_settings


class NewsCollector:
    """Collector for news articles from various sources."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.news_api_key
    
    def collect_from_newsapi(
        self,
        query: str = "금융 OR 투자 OR 경제",
        days: int = 7,
        language: str = "ko"
    ) -> List[NewsArticle]:
        """
        Collect news from NewsAPI.org
        
        Args:
            query: Search query for news
            days: Number of days to look back
            language: Language code (ko for Korean)
        
        Returns:
            List of NewsArticle objects
        """
        articles = []
        
        if not self.api_key:
            print("Warning: NEWS_API_KEY not set. Using sample data.")
            return self._get_sample_news()
        
        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "from": from_date,
                "language": language,
                "sortBy": "publishedAt",
                "apiKey": self.api_key,
                "pageSize": 100
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for article in data.get("articles", []):
                try:
                    news_article = NewsArticle(
                        title=article.get("title", ""),
                        content=article.get("content") or article.get("description", ""),
                        source=article.get("source", {}).get("name", "Unknown"),
                        url=article.get("url", ""),
                        published_at=datetime.fromisoformat(
                            article.get("publishedAt", "").replace("Z", "+00:00")
                        ),
                        author=article.get("author"),
                        metadata={"image": article.get("urlToImage")}
                    )
                    articles.append(news_article)
                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue
        
        except Exception as e:
            print(f"Error fetching news: {e}")
            return self._get_sample_news()
        
        return articles
    
    def collect_from_rss(self, feed_url: str) -> List[NewsArticle]:
        """
        Collect news from RSS feed.
        
        Args:
            feed_url: RSS feed URL
        
        Returns:
            List of NewsArticle objects
        """
        articles = []
        
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:50]:  # Limit to 50 articles
                try:
                    published = entry.get("published_parsed")
                    if published:
                        published_dt = datetime(*published[:6])
                    else:
                        published_dt = datetime.now()
                    
                    news_article = NewsArticle(
                        title=entry.get("title", ""),
                        content=entry.get("summary", ""),
                        source=feed.feed.get("title", "RSS Feed"),
                        url=entry.get("link", ""),
                        published_at=published_dt,
                        author=entry.get("author")
                    )
                    articles.append(news_article)
                except Exception as e:
                    print(f"Error parsing RSS entry: {e}")
                    continue
        
        except Exception as e:
            print(f"Error fetching RSS feed: {e}")
        
        return articles
    
    def _get_sample_news(self) -> List[NewsArticle]:
        """Return sample news data for testing."""
        return [
            NewsArticle(
                title="금리 인하 전망, 예금자들의 선택은?",
                content="중앙은행의 금리 인하 가능성이 높아지면서 예금자들이 고민에 빠졌습니다. 전문가들은 현재 높은 금리의 예금 상품에 가입하는 것이 유리하다고 조언합니다.",
                source="경제일보",
                url="https://example.com/news1",
                published_at=datetime.now() - timedelta(days=1),
                author="김기자",
                category="금융"
            ),
            NewsArticle(
                title="2024년 주목할 적금 상품 TOP 5",
                content="새해를 맞아 각 은행들이 다양한 적금 상품을 출시했습니다. 특히 청년층을 대상으로 한 우대금리 상품이 인기를 끌고 있습니다.",
                source="금융신문",
                url="https://example.com/news2",
                published_at=datetime.now() - timedelta(days=2),
                author="이기자",
                category="재테크"
            ),
            NewsArticle(
                title="디지털 자산 투자 열풍, 주의사항은?",
                content="최근 디지털 자산에 대한 투자가 급증하고 있습니다. 하지만 변동성이 큰 만큼 신중한 접근이 필요합니다.",
                source="투자뉴스",
                url="https://example.com/news3",
                published_at=datetime.now() - timedelta(days=3),
                author="박기자",
                category="투자"
            )
        ]
