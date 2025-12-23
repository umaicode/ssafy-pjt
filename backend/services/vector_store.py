import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import json
from backend.config import get_settings
from backend.models.schemas import NewsArticle, YouTubeVideo, FinancialProduct


class VectorStore:
    """Vector store for RAG system using ChromaDB."""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = chromadb.PersistentClient(
            path=self.settings.chroma_persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        self.embedder = SentenceTransformer(self.settings.embedding_model)
        
        # Create collections
        self.news_collection = self.client.get_or_create_collection(
            name="news_articles",
            metadata={"description": "Financial news articles"}
        )
        
        self.youtube_collection = self.client.get_or_create_collection(
            name="youtube_videos",
            metadata={"description": "YouTube videos about finance"}
        )
        
        self.products_collection = self.client.get_or_create_collection(
            name="financial_products",
            metadata={"description": "Deposit and savings products"}
        )
    
    def add_news_articles(self, articles: List[NewsArticle]) -> int:
        """
        Add news articles to vector store.
        
        Args:
            articles: List of NewsArticle objects
        
        Returns:
            Number of articles added
        """
        if not articles:
            return 0
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, article in enumerate(articles):
            # Create document text
            doc_text = f"{article.title}\n\n{article.content}"
            documents.append(doc_text)
            
            # Create metadata
            metadata = {
                "title": article.title,
                "source": article.source,
                "url": article.url,
                "published_at": article.published_at.isoformat(),
                "author": article.author or "Unknown",
                "type": "news"
            }
            metadatas.append(metadata)
            
            # Create unique ID
            ids.append(f"news_{idx}_{hash(article.title)}")
        
        # Generate embeddings
        embeddings = self.embedder.encode(documents).tolist()
        
        # Add to collection
        self.news_collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(articles)
    
    def add_youtube_videos(self, videos: List[YouTubeVideo]) -> int:
        """
        Add YouTube videos to vector store.
        
        Args:
            videos: List of YouTubeVideo objects
        
        Returns:
            Number of videos added
        """
        if not videos:
            return 0
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, video in enumerate(videos):
            # Create document text
            doc_text = f"{video.title}\n\n{video.description}\n\nTags: {', '.join(video.tags)}"
            documents.append(doc_text)
            
            # Create metadata
            metadata = {
                "title": video.title,
                "video_id": video.video_id,
                "channel": video.channel,
                "published_at": video.published_at.isoformat(),
                "view_count": video.view_count,
                "like_count": video.like_count,
                "type": "youtube",
                "url": f"https://youtube.com/watch?v={video.video_id}"
            }
            metadatas.append(metadata)
            
            # Create unique ID
            ids.append(f"youtube_{video.video_id}")
        
        # Generate embeddings
        embeddings = self.embedder.encode(documents).tolist()
        
        # Add to collection
        self.youtube_collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(videos)
    
    def add_financial_products(self, products: List[FinancialProduct]) -> int:
        """
        Add financial products to vector store.
        
        Args:
            products: List of FinancialProduct objects
        
        Returns:
            Number of products added
        """
        if not products:
            return 0
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, product in enumerate(products):
            # Create document text
            doc_text = (
                f"{product.product_name} - {product.bank_name}\n\n"
                f"금리: {product.interest_rate}% (최고 {product.max_interest_rate}%)\n"
                f"기간: {product.period_months}개월\n"
                f"설명: {product.description}\n"
                f"조건: {product.conditions or 'N/A'}"
            )
            documents.append(doc_text)
            
            # Create metadata
            metadata = {
                "product_name": product.product_name,
                "bank_name": product.bank_name,
                "product_type": product.product_type,
                "interest_rate": product.interest_rate,
                "max_interest_rate": product.max_interest_rate or product.interest_rate,
                "period_months": product.period_months,
                "type": product.product_type,
                "url": product.url or ""
            }
            metadatas.append(metadata)
            
            # Create unique ID
            ids.append(f"{product.product_type}_{idx}_{hash(product.product_name)}")
        
        # Generate embeddings
        embeddings = self.embedder.encode(documents).tolist()
        
        # Add to collection
        self.products_collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(products)
    
    def search(
        self,
        query: str,
        collection_names: Optional[List[str]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search across collections.
        
        Args:
            query: Search query
            collection_names: List of collection names to search (None = all)
            top_k: Number of results to return per collection
        
        Returns:
            List of search results with documents and metadata
        """
        if collection_names is None:
            collections = [
                self.news_collection,
                self.youtube_collection,
                self.products_collection
            ]
        else:
            collection_map = {
                "news": self.news_collection,
                "youtube": self.youtube_collection,
                "deposit": self.products_collection,
                "savings": self.products_collection
            }
            collections = [
                collection_map[name] 
                for name in collection_names 
                if name in collection_map
            ]
        
        # Generate query embedding
        query_embedding = self.embedder.encode([query])[0].tolist()
        
        all_results = []
        
        for collection in collections:
            try:
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k
                )
                
                # Format results
                for idx in range(len(results["ids"][0])):
                    all_results.append({
                        "id": results["ids"][0][idx],
                        "document": results["documents"][0][idx],
                        "metadata": results["metadatas"][0][idx],
                        "distance": results["distances"][0][idx]
                    })
            except Exception as e:
                print(f"Error searching collection: {e}")
        
        # Sort by distance (lower is better)
        all_results.sort(key=lambda x: x["distance"])
        
        return all_results[:top_k]
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about stored documents."""
        return {
            "news_count": self.news_collection.count(),
            "youtube_count": self.youtube_collection.count(),
            "products_count": self.products_collection.count()
        }
