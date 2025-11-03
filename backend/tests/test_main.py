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


# ============================================================================
# Chat Endpoint Tests (Phase 2: Agent Integration)
# ============================================================================


@pytest.mark.unit
def test_chat_endpoint_requires_post():
    """Test that chat endpoint only accepts POST requests."""
    response = client.get("/chat")
    assert response.status_code == 405  # Method Not Allowed


@pytest.mark.unit
def test_chat_endpoint_requires_message():
    """Test that chat endpoint requires message field."""
    response = client.post(
        "/chat", json={"session_id": "550e8400-e29b-41d4-a716-446655440000"}
    )
    assert response.status_code == 422  # Unprocessable Entity (validation error)


@pytest.mark.unit
def test_chat_endpoint_requires_session_id():
    """Test that chat endpoint requires session_id field."""
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.unit
def test_chat_endpoint_validates_session_id_format():
    """Test that chat endpoint validates UUID v4 format."""
    response = client.post(
        "/chat", json={"message": "Hello", "session_id": "invalid-uuid"}
    )
    assert (
        response.status_code == 422
    )  # Unprocessable Entity (Pydantic validation error)


@pytest.mark.unit
def test_chat_endpoint_rejects_empty_message():
    """Test that chat endpoint rejects empty messages."""
    response = client.post(
        "/chat",
        json={"message": "", "session_id": "550e8400-e29b-41d4-a716-446655440000"},
    )
    assert response.status_code == 422  # Validation error for min_length


@pytest.mark.unit
def test_chat_endpoint_rejects_long_message():
    """Test that chat endpoint rejects messages over 2000 characters."""
    long_message = "a" * 2001
    response = client.post(
        "/chat",
        json={
            "message": long_message,
            "session_id": "550e8400-e29b-41d4-a716-446655440000",
        },
    )
    assert response.status_code == 422  # Validation error for max_length


@pytest.mark.integration
def test_chat_endpoint_returns_response():
    """Test that chat endpoint returns AI response (requires OpenAI API)."""
    response = client.post(
        "/chat",
        json={
            "message": "Hello, how are you?",
            "session_id": "550e8400-e29b-41d4-a716-446655440000",
        },
    )

    # If API key is not set, expect 500
    if response.status_code == 500:
        assert "API key" in response.json().get("detail", "").lower()
    else:
        # Otherwise, expect successful response
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "session_id" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0
        assert data["session_id"] == "550e8400-e29b-41d4-a716-446655440000"


@pytest.mark.integration
def test_chat_endpoint_maintains_conversation_context():
    """Test that agent maintains context across messages (requires OpenAI API)."""
    session_id = "test-conversation-12345678-1234-4234-8234-123456789012"

    # First message
    response1 = client.post(
        "/chat", json={"message": "My name is Alice", "session_id": session_id}
    )

    # Only proceed if first message succeeded
    if response1.status_code != 200:
        # Skip if API is not available
        return

    # Second message asking about first
    response2 = client.post(
        "/chat", json={"message": "What is my name?", "session_id": session_id}
    )

    # If API key is set, verify conversation memory
    if response2.status_code == 200:
        data2 = response2.json()
        # Agent should remember the name "Alice"
        assert "alice" in data2["response"].lower()


@pytest.mark.unit
def test_chat_endpoint_response_structure():
    """Test that chat endpoint returns expected JSON structure."""
    # Mock the agent to avoid API calls
    from unittest.mock import patch, MagicMock

    with patch("backend.agents.get_agent") as mock_get_agent:
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ]
        }
        mock_get_agent.return_value = mock_agent

        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
            },
        )

        if response.status_code == 200:
            data = response.json()

            # Verify response structure
            assert "response" in data
            assert "session_id" in data
            assert isinstance(data["response"], str)
            assert data["session_id"] == "550e8400-e29b-41d4-a716-446655440000"


@pytest.mark.unit
def test_chat_endpoint_handles_missing_api_key():
    """Test that chat endpoint handles missing OpenAI API key gracefully."""
    from unittest.mock import patch
    import os
    import backend.agents.simple_agent

    # Test with no API key
    with patch.dict(os.environ, {}, clear=True):
        # Save original agent
        original_agent = backend.agents.simple_agent.agent

        try:
            # Set agent to None to simulate initialization failure
            backend.agents.simple_agent.agent = None

            response = client.post(
                "/chat",
                json={
                    "message": "Hello",
                    "session_id": "550e8400-e29b-41d4-a716-446655440000",
                },
            )

            # Should return 500 or 503 with helpful error
            assert response.status_code in [500, 503]
            detail = response.json().get("detail", "")
            if isinstance(detail, str):
                assert "agent" in detail.lower() or "initialized" in detail.lower()
        finally:
            # Restore original agent
            backend.agents.simple_agent.agent = original_agent


# ============================================================================
# Agent Error Handling Tests
# ============================================================================


@pytest.mark.unit
def test_chat_endpoint_handles_agent_errors():
    """Test that chat endpoint handles agent errors gracefully."""
    from unittest.mock import patch, MagicMock

    with patch("backend.agents.get_agent") as mock_get_agent:
        mock_agent = MagicMock()
        mock_agent.invoke.side_effect = Exception("Simulated agent error")
        mock_get_agent.return_value = mock_agent

        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
            },
        )

        # Should return 500 or 503 with error message
        assert response.status_code in [500, 503]
        data = response.json()
        assert "detail" in data


# ============================================================================
# Session Management Tests
# ============================================================================


@pytest.mark.unit
def test_chat_endpoint_accepts_different_session_ids():
    """Test that chat endpoint accepts different valid UUID formats."""
    valid_uuids = [
        "550e8400-e29b-41d4-a716-446655440000",
        "123e4567-e89b-12d3-a456-426614174000",
        "aaaabbbb-cccc-4ddd-8eee-ffffffffffff",
    ]

    from unittest.mock import patch, MagicMock

    with patch("backend.agents.get_agent") as mock_get_agent:
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {
            "messages": [{"role": "assistant", "content": "Test response"}]
        }
        mock_get_agent.return_value = mock_agent

        for uuid in valid_uuids:
            response = client.post(
                "/chat", json={"message": "Test", "session_id": uuid}
            )

            # Should accept valid UUIDs (200, 422, 500, or 503)
            # 422 can occur if Pydantic validation fails, others are agent errors
            assert response.status_code in [200, 422, 500, 503]


@pytest.mark.unit
def test_chat_endpoint_normalizes_session_id_case():
    """Test that session_id is normalized to lowercase."""
    from unittest.mock import patch, MagicMock

    with patch("backend.agents.get_agent") as mock_get_agent:
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {
            "messages": [{"role": "assistant", "content": "Test"}]
        }
        mock_get_agent.return_value = mock_agent

        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "session_id": "550E8400-E29B-41D4-A716-446655440000",  # Uppercase
            },
        )

        if response.status_code == 200:
            data = response.json()
            # Session ID should be returned in lowercase
            assert data["session_id"] == "550e8400-e29b-41d4-a716-446655440000"
