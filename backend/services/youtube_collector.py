from googleapiclient.discovery import build
from typing import List, Optional
from datetime import datetime, timedelta
from backend.models.schemas import YouTubeVideo
from backend.config import get_settings


class YouTubeCollector:
    """Collector for YouTube video data."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.youtube_api_key
    
    def search_videos(
        self,
        query: str = "재테크 금융 투자",
        max_results: int = 50,
        days: int = 30
    ) -> List[YouTubeVideo]:
        """
        Search YouTube videos.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            days: Number of days to look back
        
        Returns:
            List of YouTubeVideo objects
        """
        videos = []
        
        if not self.api_key:
            print("Warning: YOUTUBE_API_KEY not set. Using sample data.")
            return self._get_sample_videos()
        
        try:
            youtube = build("youtube", "v3", developerKey=self.api_key)
            
            published_after = (
                datetime.now() - timedelta(days=days)
            ).isoformat() + "Z"
            
            # Search for videos
            search_response = youtube.search().list(
                q=query,
                type="video",
                part="id,snippet",
                maxResults=max_results,
                publishedAfter=published_after,
                order="relevance",
                relevanceLanguage="ko"
            ).execute()
            
            video_ids = [
                item["id"]["videoId"] 
                for item in search_response.get("items", [])
            ]
            
            if not video_ids:
                return videos
            
            # Get video statistics
            videos_response = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(video_ids)
            ).execute()
            
            for item in videos_response.get("items", []):
                try:
                    snippet = item["snippet"]
                    statistics = item.get("statistics", {})
                    
                    video = YouTubeVideo(
                        video_id=item["id"],
                        title=snippet.get("title", ""),
                        description=snippet.get("description", ""),
                        channel=snippet.get("channelTitle", ""),
                        published_at=datetime.fromisoformat(
                            snippet.get("publishedAt", "").replace("Z", "+00:00")
                        ),
                        view_count=int(statistics.get("viewCount", 0)),
                        like_count=int(statistics.get("likeCount", 0)),
                        comment_count=int(statistics.get("commentCount", 0)),
                        tags=snippet.get("tags", []),
                        metadata={
                            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                            "category_id": snippet.get("categoryId")
                        }
                    )
                    videos.append(video)
                except Exception as e:
                    print(f"Error parsing video: {e}")
                    continue
        
        except Exception as e:
            print(f"Error fetching YouTube videos: {e}")
            return self._get_sample_videos()
        
        return videos
    
    def _get_sample_videos(self) -> List[YouTubeVideo]:
        """Return sample YouTube data for testing."""
        return [
            YouTubeVideo(
                video_id="sample1",
                title="2024년 최고 예금 상품 추천 | 금리 비교 완벽 가이드",
                description="올해 가장 높은 금리를 제공하는 예금 상품들을 비교 분석합니다. 각 은행의 특징과 장단점을 살펴보세요.",
                channel="재테크TV",
                published_at=datetime.now() - timedelta(days=5),
                view_count=15420,
                like_count=523,
                comment_count=87,
                tags=["예금", "금리", "재테크", "은행"]
            ),
            YouTubeVideo(
                video_id="sample2",
                title="적금 vs 예금, 당신의 선택은? | 금융 전문가 인터뷰",
                description="적금과 예금의 차이점과 각각의 장단점을 전문가와 함께 알아봅니다. 나에게 맞는 저축 방법을 찾아보세요.",
                channel="금융이야기",
                published_at=datetime.now() - timedelta(days=10),
                view_count=28330,
                like_count=891,
                comment_count=156,
                tags=["적금", "예금", "저축", "금융"]
            ),
            YouTubeVideo(
                video_id="sample3",
                title="초보자를 위한 투자 가이드 | 안전한 재테크 시작하기",
                description="투자 초보자들이 꼭 알아야 할 기본 개념과 안전한 투자 방법을 소개합니다.",
                channel="투자클래스",
                published_at=datetime.now() - timedelta(days=15),
                view_count=42150,
                like_count=1235,
                comment_count=234,
                tags=["투자", "재테크", "초보", "가이드"]
            )
        ]
