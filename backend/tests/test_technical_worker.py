"""
Unit tests for Technical Support Worker Agent.

Tests the technical support worker agent creation, tool wrapper functionality,
and configuration without making actual API calls to OpenAI.

Phase: 3 - Multi-Agent Supervisor Architecture
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os


# Test fixtures
@pytest.fixture
def mock_openai_key(monkeypatch):
    """Mock the OPENAI_API_KEY environment variable."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-mock-key-12345")


# Test Cases
class TestTechnicalWorkerCreation:
    """Test technical support worker agent creation and configuration."""

    @patch("agents.workers.technical_support.create_agent")
    def test_create_technical_worker(self, mock_create_agent, mock_openai_key):
        """Test that technical worker agent can be created."""
        from agents.workers.technical_support import create_technical_support_agent

        # Mock the return value
        mock_agent = Mock()
        mock_agent.name = "technical_support_agent"
        mock_create_agent.return_value = mock_agent

        # Create technical worker
        worker = create_technical_support_agent()

        # Verify create_agent was called with correct parameters
        mock_create_agent.assert_called_once()
        call_kwargs = mock_create_agent.call_args[1]

        assert call_kwargs["model"] == "openai:gpt-4o-mini"
        assert call_kwargs["tools"] == []  # Worker has no tools (for now)
        assert call_kwargs["name"] == "technical_support_agent"
        assert "system_prompt" in call_kwargs

        # Verify worker was created
        assert worker is not None
        assert worker.name == "technical_support_agent"

    @patch("agents.workers.technical_support.create_agent")
    def test_technical_worker_system_prompt_is_specialized(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that technical worker has specialized system prompt."""
        from agents.workers.technical_support import create_technical_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_technical_support_agent()

        # Get the system prompt from the call
        call_kwargs = mock_create_agent.call_args[1]
        system_prompt = call_kwargs["system_prompt"]

        # Verify technical support concepts are in the prompt
        assert "technical" in system_prompt.lower()
        assert "support" in system_prompt.lower()
        assert any(
            word in system_prompt.lower()
            for word in ["troubleshoot", "error", "bug", "issue", "problem"]
        )

    def test_create_technical_worker_without_api_key(self):
        """Test that technical worker creation fails without API key."""
        from agents.workers.technical_support import create_technical_support_agent

        # Clear OPENAI_API_KEY
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        # Should raise ValueError
        with pytest.raises(ValueError, match="OPENAI_API_KEY must be set"):
            create_technical_support_agent()

    @patch("agents.workers.technical_support.create_agent")
    def test_technical_worker_has_no_checkpointer(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that technical worker doesn't use checkpointer (supervisor handles memory)."""
        from agents.workers.technical_support import create_technical_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_technical_support_agent()

        # Verify checkpointer is NOT passed (supervisor handles conversation memory)
        call_kwargs = mock_create_agent.call_args[1]
        assert "checkpointer" not in call_kwargs or call_kwargs.get("checkpointer") is None


class TestTechnicalWorkerGetter:
    """Test the get_technical_agent() function."""

    @patch("agents.workers.technical_support.technical_agent", None)
    def test_get_technical_agent_when_not_initialized(self):
        """Test that get_technical_agent raises error when agent is None."""
        from agents.workers.technical_support import get_technical_agent

        with pytest.raises(RuntimeError, match="Technical support agent is not initialized"):
            get_technical_agent()

    @patch("agents.workers.technical_support.technical_agent")
    def test_get_technical_agent_when_initialized(self, mock_agent):
        """Test that get_technical_agent returns the agent when initialized."""
        from agents.workers.technical_support import get_technical_agent

        mock_agent.name = "technical_support_agent"

        agent = get_technical_agent()

        assert agent is not None
        assert agent.name == "technical_support_agent"


class TestTechnicalWorkerConfiguration:
    """Test technical worker agent configuration details."""

    @patch("agents.workers.technical_support.create_agent")
    def test_technical_worker_model_is_gpt4o_mini(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that technical worker uses GPT-4o-mini model."""
        from agents.workers.technical_support import create_technical_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_technical_support_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["model"] == "openai:gpt-4o-mini"

    @patch("agents.workers.technical_support.create_agent")
    def test_technical_worker_has_descriptive_name(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that technical worker has a descriptive name for logging/tracing."""
        from agents.workers.technical_support import create_technical_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_technical_support_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["name"] == "technical_support_agent"

    @patch("agents.workers.technical_support.create_agent")
    def test_technical_worker_has_no_tools(self, mock_create_agent, mock_openai_key):
        """Test that technical worker has no tools (responds directly)."""
        from agents.workers.technical_support import create_technical_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_technical_support_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["tools"] == []


class TestTechnicalSupportTool:
    """Test the technical_support_tool wrapper."""

    @patch("agents.workers.technical_support.get_technical_agent")
    def test_technical_support_tool_invokes_agent(self, mock_get_agent):
        """Test that the tool wrapper invokes the technical agent."""
        from agents.workers.technical_support import technical_support_tool

        # Mock the agent and its response
        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Here's how to fix the error..."
        mock_result = {"messages": [mock_message]}
        mock_agent.invoke.return_value = mock_result
        mock_get_agent.return_value = mock_agent

        # Call the tool using .invoke()
        query = "Error 500 on login"
        response = technical_support_tool.invoke({"query": query})

        # Verify agent was called
        mock_get_agent.assert_called_once()
        mock_agent.invoke.assert_called_once()

        # Verify the query was passed correctly
        call_args = mock_agent.invoke.call_args[0][0]
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"] == query

        # Verify response is returned
        assert response == "Here's how to fix the error..."

    def test_technical_support_tool_has_correct_name(self):
        """Test that the tool has the correct name."""
        from agents.workers.technical_support import technical_support_tool

        assert technical_support_tool.name == "technical_support_tool"

    def test_technical_support_tool_has_description(self):
        """Test that the tool has a description for routing."""
        from agents.workers.technical_support import technical_support_tool

        description = technical_support_tool.description

        # Verify description mentions technical support concepts
        assert description is not None
        assert len(description) > 0
        assert "technical" in description.lower() or "support" in description.lower()

    @patch("agents.workers.technical_support.get_technical_agent")
    def test_technical_support_tool_returns_string(self, mock_get_agent):
        """Test that the tool returns a string response."""
        from agents.workers.technical_support import technical_support_tool

        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_result = {"messages": [mock_message]}
        mock_agent.invoke.return_value = mock_result
        mock_get_agent.return_value = mock_agent

        response = technical_support_tool.invoke({"query": "Test query"})

        assert isinstance(response, str)
        assert response == "Test response"

    @patch("agents.workers.technical_support.get_technical_agent")
    def test_technical_support_tool_handles_long_queries(self, mock_get_agent):
        """Test that the tool handles long technical queries."""
        from agents.workers.technical_support import technical_support_tool

        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Detailed response..."
        mock_result = {"messages": [mock_message]}
        mock_agent.invoke.return_value = mock_result
        mock_get_agent.return_value = mock_agent

        # Long query
        long_query = "I'm getting Error 500 when logging in. " * 10
        response = technical_support_tool.invoke({"query": long_query})

        # Verify full query was passed
        call_args = mock_agent.invoke.call_args[0][0]
        assert call_args["messages"][0]["content"] == long_query
        assert isinstance(response, str)


class TestTechnicalWorkerLogging:
    """Test logging behavior of technical worker agent."""

    @patch("agents.workers.technical_support.create_agent")
    @patch("agents.workers.technical_support.logger")
    def test_technical_worker_logs_creation(
        self, mock_logger, mock_create_agent, mock_openai_key
    ):
        """Test that technical worker logs when created."""
        from agents.workers.technical_support import create_technical_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_technical_support_agent()

        # Verify logging calls
        mock_logger.info.assert_any_call("Creating technical support worker agent")
        mock_logger.info.assert_any_call(
            "Technical support worker agent created successfully"
        )

    @patch("agents.workers.technical_support.get_technical_agent")
    @patch("agents.workers.technical_support.logger")
    def test_technical_support_tool_logs_invocation(self, mock_logger, mock_get_agent):
        """Test that the tool logs when invoked."""
        from agents.workers.technical_support import technical_support_tool

        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Response"
        mock_result = {"messages": [mock_message]}
        mock_agent.invoke.return_value = mock_result
        mock_get_agent.return_value = mock_agent

        query = "Error 500"
        technical_support_tool.invoke({"query": query})

        # Verify logging includes query
        assert any(
            "Technical support tool called" in str(call)
            for call in mock_logger.info.call_args_list
        )


class TestTechnicalWorkerErrorHandling:
    """Test error handling in technical worker agent."""

    @patch("agents.workers.technical_support.logger")
    def test_technical_worker_logs_error_on_missing_key(self, mock_logger):
        """Test that technical worker logs error when API key is missing."""
        from agents.workers.technical_support import create_technical_support_agent

        # Clear API key
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        try:
            create_technical_support_agent()
        except ValueError:
            pass

        mock_logger.error.assert_called_once_with(
            "OPENAI_API_KEY environment variable is not set"
        )


class TestTechnicalWorkerIntegration:
    """Test technical worker in more realistic scenarios."""

    @patch("agents.workers.technical_support.get_technical_agent")
    def test_technical_tool_with_various_error_types(self, mock_get_agent):
        """Test that the tool handles various types of technical queries."""
        from agents.workers.technical_support import technical_support_tool

        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "Solution provided"
        mock_result = {"messages": [mock_message]}
        mock_agent.invoke.return_value = mock_result
        mock_get_agent.return_value = mock_agent

        # Test various error types
        error_queries = [
            "Error 500",
            "App crashes on startup",
            "Can't install the software",
            "Configuration not working",
            "Performance is very slow",
        ]

        for query in error_queries:
            response = technical_support_tool.invoke({"query": query})
            assert isinstance(response, str)
            assert len(response) > 0

    @patch("agents.workers.technical_support.get_technical_agent")
    def test_technical_tool_response_format(self, mock_get_agent):
        """Test that the tool returns properly formatted response."""
        from agents.workers.technical_support import technical_support_tool

        mock_agent = Mock()
        mock_message = Mock()
        mock_message.content = "1. First step\n2. Second step\n3. Third step"
        mock_result = {"messages": [mock_message]}
        mock_agent.invoke.return_value = mock_result
        mock_get_agent.return_value = mock_agent

        response = technical_support_tool.invoke({"query": "How to fix?"})

        # Verify response preserves formatting
        assert "1. First step" in response
        assert "\n" in response  # Preserves line breaks


# Run tests with: pytest backend/tests/test_technical_worker.py -v

