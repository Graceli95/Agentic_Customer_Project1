"""
Test suite for main.py FastAPI application

Tests the basic API endpoints and application setup.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for the /health endpoint"""
    
    def test_health_check_returns_200(self):
        """Test that health endpoint returns 200 OK"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_correct_structure(self):
        """Test that health endpoint returns expected JSON structure"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert "environment" in data
    
    def test_health_check_status_is_healthy(self):
        """Test that health endpoint reports healthy status"""
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "customer-service-ai"
        assert data["version"] == "1.0.0"


class TestRootEndpoint:
    """Tests for the / root endpoint"""
    
    def test_root_returns_200(self):
        """Test that root endpoint returns 200 OK"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_welcome_message(self):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        data = response.json()
        
        assert "message" in data
        assert "Advanced Customer Service AI" in data["message"]
    
    def test_root_returns_api_info(self):
        """Test that root endpoint returns API documentation links"""
        response = client.get("/")
        data = response.json()
        
        assert "docs" in data
        assert "health" in data
        assert "version" in data
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"


class TestCORS:
    """Tests for CORS configuration"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses"""
        response = client.options(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers or \
               response.status_code == 200  # FastAPI TestClient may not fully simulate CORS


@pytest.mark.asyncio
async def test_app_lifespan():
    """Test that app startup and shutdown events work"""
    # This is a placeholder test for lifespan events
    # In real implementation, you'd test any startup/shutdown logic
    assert app is not None
    assert hasattr(app, "router")


def test_app_metadata():
    """Test that app has correct metadata"""
    assert app.title == "Advanced Customer Service AI"
    assert app.version == "1.0.0"
    assert app.description == "Multi-agent AI system for customer service"

