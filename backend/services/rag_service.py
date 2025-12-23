from typing import List, Dict, Any, Optional
from openai import OpenAI
from backend.config import get_settings
from backend.services.vector_store import VectorStore
from backend.models.schemas import QueryResponse


class RAGService:
    """RAG (Retrieval-Augmented Generation) service."""
    
    def __init__(self):
        self.settings = get_settings()
        self.vector_store = VectorStore()
        self.client = None
        
        # Initialize OpenAI client if API key is available
        if self.settings.openai_api_key:
            self.client = OpenAI(api_key=self.settings.openai_api_key)
    
    def query(
        self,
        query: str,
        source_filters: Optional[List[str]] = None,
        top_k: int = 5,
        include_metadata: bool = True
    ) -> QueryResponse:
        """
        Process a query using RAG.
        
        Args:
            query: User query
            source_filters: Filter by data source types
            top_k: Number of documents to retrieve
            include_metadata: Whether to include source metadata
        
        Returns:
            QueryResponse with answer and sources
        """
        # Retrieve relevant documents
        search_results = self.vector_store.search(
            query=query,
            collection_names=source_filters,
            top_k=top_k
        )
        
        if not search_results:
            return QueryResponse(
                query=query,
                answer="죄송합니다. 관련된 정보를 찾을 수 없습니다. 다른 질문을 해주세요.",
                sources=[]
            )
        
        # Generate answer using LLM
        answer = self._generate_answer(query, search_results)
        
        # Format sources
        sources = []
        if include_metadata:
            for result in search_results:
                source = {
                    "content": result["document"][:200] + "...",
                    "metadata": result["metadata"]
                }
                sources.append(source)
        
        return QueryResponse(
            query=query,
            answer=answer,
            sources=sources
        )
    
    def _generate_answer(
        self,
        query: str,
        search_results: List[Dict[str, Any]]
    ) -> str:
        """
        Generate answer using LLM.
        
        Args:
            query: User query
            search_results: Retrieved documents
        
        Returns:
            Generated answer
        """
        # Build context from search results
        context = "\n\n".join([
            f"[출처 {idx+1}]\n{result['document']}"
            for idx, result in enumerate(search_results[:3])
        ])
        
        if not self.client:
            # Fallback: Return context without LLM generation
            return self._generate_fallback_answer(query, search_results)
        
        try:
            # Create prompt
            system_prompt = """당신은 금융 전문 AI 어시스턴트입니다. 
사용자의 질문에 대해 제공된 맥락 정보를 바탕으로 정확하고 도움이 되는 답변을 제공하세요.
답변은 한국어로 작성하며, 친절하고 전문적인 톤을 유지하세요.
정보가 불충분한 경우, 그 사실을 명확히 밝히고 가능한 범위 내에서 답변하세요."""
            
            user_prompt = f"""질문: {query}

참고 자료:
{context}

위 자료를 바탕으로 질문에 답변해주세요. 답변 시 구체적인 수치나 정보가 있다면 반드시 포함해주세요."""
            
            response = self.client.chat.completions.create(
                model=self.settings.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.settings.temperature,
                max_tokens=self.settings.max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error generating answer with LLM: {e}")
            return self._generate_fallback_answer(query, search_results)
    
    def _generate_fallback_answer(
        self,
        query: str,
        search_results: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a simple answer without LLM.
        
        Args:
            query: User query
            search_results: Retrieved documents
        
        Returns:
            Simple answer based on search results
        """
        if not search_results:
            return "관련 정보를 찾을 수 없습니다."
        
        answer_parts = [f"'{query}'에 대한 검색 결과입니다:\n"]
        
        for idx, result in enumerate(search_results[:3], 1):
            metadata = result["metadata"]
            doc_type = metadata.get("type", "unknown")
            
            if doc_type == "news":
                answer_parts.append(
                    f"\n{idx}. [{metadata.get('source')}] {metadata.get('title')}\n"
                    f"   {result['document'][:150]}..."
                )
            elif doc_type == "youtube":
                answer_parts.append(
                    f"\n{idx}. [YouTube - {metadata.get('channel')}] {metadata.get('title')}\n"
                    f"   조회수: {metadata.get('view_count'):,}회\n"
                    f"   {result['document'][:150]}..."
                )
            elif doc_type in ["deposit", "savings"]:
                answer_parts.append(
                    f"\n{idx}. [{metadata.get('bank_name')}] {metadata.get('product_name')}\n"
                    f"   금리: {metadata.get('interest_rate')}% (최고 {metadata.get('max_interest_rate')}%)\n"
                    f"   기간: {metadata.get('period_months')}개월"
                )
        
        return "".join(answer_parts)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get RAG system statistics."""
        return {
            "vector_store_stats": self.vector_store.get_stats(),
            "llm_available": self.client is not None,
            "embedding_model": self.settings.embedding_model,
            "llm_model": self.settings.llm_model
        }
