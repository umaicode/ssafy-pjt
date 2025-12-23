import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_query_endpoint():
    """Test query endpoint."""
    response = client.post(
        "/api/query",
        json={
            "query": "높은 금리 예금",
            "top_k": 5
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "answer" in data
    assert "sources" in data


def test_analyze_endpoint():
    """Test analyze endpoint."""
    response = client.post(
        "/api/analyze",
        json={
            "query": "금리",
            "analysis_type": "trend",
            "time_range_days": 30
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "analysis_type" in data
    assert "summary" in data
    assert "insights" in data


def test_collect_news_endpoint():
    """Test news collection endpoint."""
    response = client.post(
        "/api/collect/news?query=금융&days=7"
    )
    assert response.status_code == 200
    assert response.json()["status"] == "started"


def test_stats_endpoint():
    """Test stats endpoint."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "statistics" in response.json()
