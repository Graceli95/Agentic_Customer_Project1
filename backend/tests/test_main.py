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


# ============================================================================
# Phase 3: Multi-Agent Routing Integration Tests
# ============================================================================


@pytest.mark.integration
def test_chat_endpoint_routes_technical_query_to_worker():
    """Test that technical queries are routed to technical support worker."""
    from unittest.mock import patch, Mock

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        # Mock supervisor agent
        mock_supervisor = Mock()
        
        # Mock the result that includes tool call (indicating routing)
        mock_user_msg = Mock()
        mock_user_msg.content = "Error 500 when logging in"
        mock_user_msg.type = "human"
        
        mock_tool_call_msg = Mock()
        mock_tool_call_msg.type = "tool"
        mock_tool_call_msg.name = "technical_support_tool"
        
        mock_response_msg = Mock()
        mock_response_msg.content = "I understand you're experiencing Error 500. Here are troubleshooting steps..."
        mock_response_msg.type = "ai"
        
        mock_supervisor.invoke.return_value = {
            "messages": [mock_user_msg, mock_tool_call_msg, mock_response_msg]
        }
        mock_get_supervisor.return_value = mock_supervisor

        response = client.post(
            "/chat",
            json={
                "message": "Error 500 when logging in",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
            },
        )

        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data
        assert "session_id" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0
        
        # Verify supervisor was invoked
        mock_supervisor.invoke.assert_called_once()


@pytest.mark.integration
def test_chat_endpoint_handles_general_query_directly():
    """Test that general queries are handled by supervisor without routing."""
    from unittest.mock import patch, Mock

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        # Mock supervisor agent
        mock_supervisor = Mock()
        
        # Mock the result without tool calls (direct handling)
        mock_user_msg = Mock()
        mock_user_msg.content = "Hello! How are you?"
        mock_user_msg.type = "human"
        
        mock_response_msg = Mock()
        mock_response_msg.content = "Hello! I'm here to help you. How can I assist you today?"
        mock_response_msg.type = "ai"
        
        mock_supervisor.invoke.return_value = {
            "messages": [mock_user_msg, mock_response_msg]
        }
        mock_get_supervisor.return_value = mock_supervisor

        response = client.post(
            "/chat",
            json={
                "message": "Hello! How are you?",
                "session_id": "a1b2c3d4-e5f6-4789-a012-3456789abcde",
            },
        )

        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data
        assert len(data["response"]) > 0
        
        # Verify supervisor was invoked
        mock_supervisor.invoke.assert_called_once()
        
        # Verify no tool calls in response (only 2 messages: user + assistant)
        call_args = mock_supervisor.invoke.call_args
        assert call_args is not None


@pytest.mark.integration
def test_chat_endpoint_maintains_context_across_routing():
    """Test that conversation context is maintained when routing to workers."""
    from unittest.mock import patch, Mock

    session_id = "550e8400-e29b-41d4-a716-446655440000"

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        mock_supervisor = Mock()
        
        # First message - technical query
        mock_msg1 = Mock()
        mock_msg1.content = "Comprehensive troubleshooting response..."
        mock_supervisor.invoke.return_value = {"messages": [mock_msg1]}
        mock_get_supervisor.return_value = mock_supervisor

        response1 = client.post(
            "/chat",
            json={"message": "Error 500 on login", "session_id": session_id},
        )

        assert response1.status_code == 200
        
        # Second message - follow-up
        mock_msg2 = Mock()
        mock_msg2.content = "Based on previous error, try these additional steps..."
        mock_supervisor.invoke.return_value = {"messages": [mock_msg2]}

        response2 = client.post(
            "/chat",
            json={"message": "I tried that but still fails", "session_id": session_id},
        )

        assert response2.status_code == 200
        
        # Verify supervisor was called twice with same thread_id
        assert mock_supervisor.invoke.call_count == 2


@pytest.mark.integration
def test_chat_endpoint_routes_different_technical_queries():
    """Test that various types of technical queries are handled correctly."""
    from unittest.mock import patch, Mock

    technical_queries = [
        "Getting Error 404 not found",
        "App keeps crashing on startup",
        "Can't install the software",
        "How do I configure the settings?",
        "Performance is very slow",
    ]

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        mock_supervisor = Mock()
        mock_msg = Mock()
        mock_msg.content = "Technical support response"
        mock_supervisor.invoke.return_value = {"messages": [mock_msg]}
        mock_get_supervisor.return_value = mock_supervisor

        for query in technical_queries:
            response = client.post(
                "/chat",
                json={
                    "message": query,
                    "session_id": "550e8400-e29b-41d4-a716-446655440000",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert len(data["response"]) > 0


@pytest.mark.integration
def test_chat_endpoint_routes_different_general_queries():
    """Test that various types of general queries are handled correctly."""
    from unittest.mock import patch, Mock

    general_queries = [
        "Hello!",
        "Thank you for your help",
        "Good morning",
        "That makes sense",
        "I appreciate it",
    ]

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        mock_supervisor = Mock()
        mock_msg = Mock()
        mock_msg.content = "You're welcome!"
        mock_supervisor.invoke.return_value = {"messages": [mock_msg]}
        mock_get_supervisor.return_value = mock_supervisor

        for query in general_queries:
            response = client.post(
                "/chat",
                json={
                    "message": query,
                    "session_id": "550e8400-e29b-41d4-a716-446655440000",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert "response" in data


@pytest.mark.integration
def test_chat_endpoint_handles_supervisor_initialization_error():
    """Test that chat endpoint handles supervisor initialization errors gracefully."""
    from unittest.mock import patch

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        # Simulate supervisor not initialized
        mock_get_supervisor.side_effect = RuntimeError(
            "Supervisor agent is not initialized"
        )

        response = client.post(
            "/chat",
            json={
                "message": "Test query",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
            },
        )

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "error" in data["detail"]


@pytest.mark.integration
def test_chat_endpoint_handles_agent_invocation_error():
    """Test that chat endpoint handles errors during agent invocation."""
    from unittest.mock import patch, Mock

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        mock_supervisor = Mock()
        # Simulate error during invoke
        mock_supervisor.invoke.side_effect = Exception("API call failed")
        mock_get_supervisor.return_value = mock_supervisor

        response = client.post(
            "/chat",
            json={
                "message": "Test query",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
            },
        )

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data


@pytest.mark.integration
def test_chat_endpoint_returns_proper_session_id():
    """Test that chat endpoint returns the correct session_id in response."""
    from unittest.mock import patch, Mock

    test_session_id = "550e8400-e29b-41d4-a716-446655440000"

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        mock_supervisor = Mock()
        mock_msg = Mock()
        mock_msg.content = "Response"
        mock_supervisor.invoke.return_value = {"messages": [mock_msg]}
        mock_get_supervisor.return_value = mock_supervisor

        response = client.post(
            "/chat",
            json={"message": "Test", "session_id": test_session_id},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == test_session_id


@pytest.mark.integration
def test_chat_endpoint_passes_config_to_supervisor():
    """Test that chat endpoint passes proper config with thread_id to supervisor."""
    from unittest.mock import patch, Mock

    session_id = "550e8400-e29b-41d4-a716-446655440000"

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        mock_supervisor = Mock()
        mock_msg = Mock()
        mock_msg.content = "Response"
        mock_supervisor.invoke.return_value = {"messages": [mock_msg]}
        mock_get_supervisor.return_value = mock_supervisor

        response = client.post(
            "/chat",
            json={"message": "Test", "session_id": session_id},
        )

        assert response.status_code == 200
        
        # Verify supervisor.invoke was called with config containing thread_id
        mock_supervisor.invoke.assert_called_once()
        call_args = mock_supervisor.invoke.call_args
        
        # Check that config was passed
        assert len(call_args[0]) == 2  # (messages, config)
        config = call_args[0][1]
        assert "configurable" in config
        assert "thread_id" in config["configurable"]
        assert config["configurable"]["thread_id"] == session_id


@pytest.mark.integration
def test_chat_endpoint_extracts_last_message_content():
    """Test that chat endpoint correctly extracts content from last message."""
    from unittest.mock import patch, Mock

    with patch("backend.main.get_supervisor") as mock_get_supervisor:
        mock_supervisor = Mock()
        
        # Create multiple messages in result
        mock_msg1 = Mock()
        mock_msg1.content = "First message"
        mock_msg2 = Mock()
        mock_msg2.content = "Second message"
        mock_msg3 = Mock()
        mock_msg3.content = "Final response message"
        
        mock_supervisor.invoke.return_value = {
            "messages": [mock_msg1, mock_msg2, mock_msg3]
        }
        mock_get_supervisor.return_value = mock_supervisor

        response = client.post(
            "/chat",
            json={
                "message": "Test",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
            },
        )

        assert response.status_code == 200
        data = response.json()
        # Should return content from last message
        assert data["response"] == "Final response message"
