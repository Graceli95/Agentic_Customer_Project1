"""
Test Suite for Main FastAPI Application

Tests the core API endpoints and application configuration.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


# ============================================================================
# Test Client Setup
# ============================================================================

client = TestClient(app)


# ============================================================================
# Health Check Endpoint Tests
# ============================================================================

@pytest.mark.unit
def test_health_check_returns_200():
    """Test that health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200


@pytest.mark.unit
def test_health_check_response_structure():
    """Test that health check returns expected JSON structure."""
    response = client.get("/health")
    data = response.json()
    
    # Verify all expected fields are present
    assert "status" in data
    assert "service" in data
    assert "version" in data
    assert "environment" in data


@pytest.mark.unit
def test_health_check_status_healthy():
    """Test that health check status is 'healthy'."""
    response = client.get("/health")
    data = response.json()
    
    assert data["status"] == "healthy"


@pytest.mark.unit
def test_health_check_service_name():
    """Test that health check returns correct service name."""
    response = client.get("/health")
    data = response.json()
    
    assert data["service"] == "customer-service-ai"


@pytest.mark.unit
def test_health_check_version():
    """Test that health check returns version information."""
    response = client.get("/health")
    data = response.json()
    
    assert data["version"] == "1.0.0"


# ============================================================================
# Root Endpoint Tests
# ============================================================================

@pytest.mark.unit
def test_root_endpoint_returns_200():
    """Test that root endpoint returns 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.unit
def test_root_endpoint_response_structure():
    """Test that root endpoint returns expected JSON structure."""
    response = client.get("/")
    data = response.json()
    
    # Verify all expected fields are present
    assert "message" in data
    assert "docs" in data
    assert "health" in data
    assert "version" in data


@pytest.mark.unit
def test_root_endpoint_message():
    """Test that root endpoint returns welcome message."""
    response = client.get("/")
    data = response.json()
    
    assert "Customer Service AI" in data["message"]


@pytest.mark.unit
def test_root_endpoint_docs_path():
    """Test that root endpoint provides documentation path."""
    response = client.get("/")
    data = response.json()
    
    assert data["docs"] == "/docs"


@pytest.mark.unit
def test_root_endpoint_health_path():
    """Test that root endpoint provides health check path."""
    response = client.get("/")
    data = response.json()
    
    assert data["health"] == "/health"


# ============================================================================
# API Documentation Tests
# ============================================================================

@pytest.mark.unit
def test_openapi_docs_accessible():
    """Test that OpenAPI documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.unit
def test_redoc_docs_accessible():
    """Test that ReDoc documentation is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200


@pytest.mark.unit
def test_openapi_json_accessible():
    """Test that OpenAPI JSON schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200


# ============================================================================
# CORS Configuration Tests
# ============================================================================

@pytest.mark.unit
def test_cors_headers_present():
    """Test that CORS headers are present in response."""
    response = client.get("/health", headers={"Origin": "http://localhost:3000"})
    
    # CORS headers should be present
    assert "access-control-allow-origin" in response.headers


# ============================================================================
# Error Handling Tests
# ============================================================================

@pytest.mark.unit
def test_nonexistent_endpoint_returns_404():
    """Test that accessing a non-existent endpoint returns 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


@pytest.mark.unit
def test_method_not_allowed_returns_405():
    """Test that using wrong HTTP method returns 405."""
    response = client.post("/health")
    assert response.status_code == 405

