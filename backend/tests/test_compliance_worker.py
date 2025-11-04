"""
Unit tests for Compliance Worker Agent.

Tests the compliance worker agent creation, tool wrapper functionality,
and configuration without making actual API calls to OpenAI.

Phase: 4 - Additional Worker Agents
"""

import pytest
from unittest.mock import Mock, patch
import os


# Test fixtures
@pytest.fixture
def mock_openai_key(monkeypatch):
    """Mock the OPENAI_API_KEY environment variable."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-mock-key-12345")


# Test Cases
class TestComplianceWorkerCreation:
    """Test compliance worker agent creation and configuration."""

    @patch("agents.workers.compliance.create_agent")
    def test_create_compliance_worker(self, mock_create_agent, mock_openai_key):
        """Test that compliance worker agent can be created."""
        from agents.workers.compliance import create_compliance_agent

        # Mock the return value
        mock_agent = Mock()
        mock_agent.name = "compliance_agent"
        mock_create_agent.return_value = mock_agent

        # Create compliance worker
        worker = create_compliance_agent()

        # Verify create_agent was called with correct parameters
        mock_create_agent.assert_called_once()
        call_kwargs = mock_create_agent.call_args[1]

        assert call_kwargs["model"] == "openai:gpt-4o-mini"
        assert call_kwargs["tools"] == []  # Worker has no tools
        assert call_kwargs["name"] == "compliance_agent"
        assert "system_prompt" in call_kwargs

        # Verify worker was created
        assert worker is not None
        assert worker.name == "compliance_agent"

    @patch("agents.workers.compliance.create_agent")
    def test_compliance_worker_system_prompt_is_specialized(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that compliance worker has specialized system prompt."""
        from agents.workers.compliance import create_compliance_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_compliance_agent()

        # Get the system prompt from the call
        call_kwargs = mock_create_agent.call_args[1]
        system_prompt = call_kwargs["system_prompt"]

        # Verify compliance concepts are in the prompt
        assert "compliance" in system_prompt.lower() or "policy" in system_prompt.lower()
        assert any(
            word in system_prompt.lower()
            for word in ["policy", "privacy", "terms", "gdpr", "ccpa", "legal"]
        )

    def test_create_compliance_worker_without_api_key(self):
        """Test that compliance worker creation fails without API key."""
        from agents.workers.compliance import create_compliance_agent

        # Clear OPENAI_API_KEY
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        # Should raise ValueError
        with pytest.raises(ValueError, match="OPENAI_API_KEY must be set"):
            create_compliance_agent()

    @patch("agents.workers.compliance.create_agent")
    def test_compliance_worker_has_no_checkpointer(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that compliance worker doesn't use checkpointer (supervisor handles memory)."""
        from agents.workers.compliance import create_compliance_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_compliance_agent()

        # Verify checkpointer is NOT passed (supervisor handles conversation memory)
        call_kwargs = mock_create_agent.call_args[1]
        assert (
            "checkpointer" not in call_kwargs or call_kwargs.get("checkpointer") is None
        )


class TestComplianceWorkerGetter:
    """Test the get_compliance_agent() function."""

    @patch("agents.workers.compliance.compliance_agent", None)
    def test_get_compliance_agent_when_not_initialized(self):
        """Test that get_compliance_agent raises error when agent is None."""
        from agents.workers.compliance import get_compliance_agent

        with pytest.raises(RuntimeError, match="Compliance agent is not initialized"):
            get_compliance_agent()

    @patch("agents.workers.compliance.compliance_agent")
    def test_get_compliance_agent_when_initialized(self, mock_agent):
        """Test that get_compliance_agent returns the agent when initialized."""
        from agents.workers.compliance import get_compliance_agent

        mock_agent.name = "compliance_agent"

        agent = get_compliance_agent()

        assert agent is not None
        assert agent.name == "compliance_agent"


class TestComplianceWorkerConfiguration:
    """Test compliance worker agent configuration details."""

    @patch("agents.workers.compliance.create_agent")
    def test_compliance_worker_model_is_gpt4o_mini(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that compliance worker uses GPT-4o-mini model."""
        from agents.workers.compliance import create_compliance_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_compliance_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["model"] == "openai:gpt-4o-mini"

    @patch("agents.workers.compliance.create_agent")
    def test_compliance_worker_has_descriptive_name(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that compliance worker has a descriptive name for debugging."""
        from agents.workers.compliance import create_compliance_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_compliance_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["name"] == "compliance_agent"
        assert "compliance" in call_kwargs["name"]

    @patch("agents.workers.compliance.create_agent")
    def test_compliance_worker_has_no_tools(self, mock_create_agent, mock_openai_key):
        """Test that compliance worker has no tools (Phase 4 - tools added in Phase 5+)."""
        from agents.workers.compliance import create_compliance_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_compliance_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["tools"] == []


class TestComplianceToolWrapper:
    """Test the compliance_tool wrapper functionality."""

    @patch("agents.workers.compliance.get_compliance_agent")
    def test_compliance_tool_wrapper_calls_agent(self, mock_get_agent, mock_openai_key):
        """Test that compliance_tool correctly invokes the compliance agent."""
        from agents.workers.compliance import compliance_tool

        # Mock the compliance agent
        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Our privacy policy complies with GDPR."
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        # Call the tool wrapper
        query = "What is your privacy policy?"
        result = compliance_tool.invoke({"query": query})

        # Verify agent was invoked with correct format
        mock_agent.invoke.assert_called_once()
        call_args = mock_agent.invoke.call_args[0][0]
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"] == query

        # Verify response was extracted correctly
        assert result == "Our privacy policy complies with GDPR."

    @patch("agents.workers.compliance.get_compliance_agent")
    def test_compliance_tool_has_descriptive_name(self, mock_get_agent, mock_openai_key):
        """Test that compliance_tool has a descriptive name."""
        from agents.workers.compliance import compliance_tool

        assert compliance_tool.name == "compliance_tool"
        assert "compliance" in compliance_tool.name

    @patch("agents.workers.compliance.get_compliance_agent")
    def test_compliance_tool_has_clear_description(
        self, mock_get_agent, mock_openai_key
    ):
        """Test that compliance_tool has a clear description for routing."""
        from agents.workers.compliance import compliance_tool

        description = compliance_tool.description

        # Should mention key compliance concepts
        assert any(
            word in description.lower()
            for word in ["policy", "privacy", "terms", "compliance", "gdpr", "ccpa"]
        )

    @patch("agents.workers.compliance.get_compliance_agent")
    def test_compliance_tool_returns_string(self, mock_get_agent, mock_openai_key):
        """Test that compliance_tool returns a string response."""
        from agents.workers.compliance import compliance_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Compliance response text"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = compliance_tool.invoke({"query": "test query"})

        assert isinstance(result, str)
        assert result == "Compliance response text"


class TestComplianceWorkerResponses:
    """Test compliance worker responses to various query types."""

    @patch("agents.workers.compliance.get_compliance_agent")
    def test_compliance_tool_handles_privacy_query(
        self, mock_get_agent, mock_openai_key
    ):
        """Test compliance tool handles privacy-related queries."""
        from agents.workers.compliance import compliance_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "We collect data according to our privacy policy"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = compliance_tool.invoke({"query": "What data do you collect?"})

        assert "privacy" in result.lower() or "data" in result.lower()

    @patch("agents.workers.compliance.get_compliance_agent")
    def test_compliance_tool_handles_gdpr_query(self, mock_get_agent, mock_openai_key):
        """Test compliance tool handles GDPR requests."""
        from agents.workers.compliance import compliance_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "To delete your data under GDPR, please contact us"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = compliance_tool.invoke({"query": "I want to delete my data"})

        assert "data" in result.lower() or "gdpr" in result.lower()

    @patch("agents.workers.compliance.get_compliance_agent")
    def test_compliance_tool_handles_terms_query(
        self, mock_get_agent, mock_openai_key
    ):
        """Test compliance tool handles terms of service queries."""
        from agents.workers.compliance import compliance_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Our Terms of Service can be found at..."
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = compliance_tool.invoke({"query": "Where are your terms of service?"})

        assert "terms" in result.lower() or "service" in result.lower()


class TestComplianceWorkerLogging:
    """Test compliance worker logging behavior."""

    @patch("agents.workers.compliance.logger")
    @patch("agents.workers.compliance.create_agent")
    def test_compliance_worker_logs_creation(
        self, mock_create_agent, mock_logger, mock_openai_key
    ):
        """Test that compliance worker logs creation."""
        from agents.workers.compliance import create_compliance_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_compliance_agent()

        # Verify logging occurred
        assert mock_logger.info.called
        log_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("compliance" in msg.lower() for msg in log_messages)

    @patch("agents.workers.compliance.logger")
    @patch("agents.workers.compliance.get_compliance_agent")
    def test_compliance_tool_logs_invocation(
        self, mock_get_agent, mock_logger, mock_openai_key
    ):
        """Test that compliance_tool logs when it's called."""
        from agents.workers.compliance import compliance_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Compliance response"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        compliance_tool.invoke({"query": "test query"})

        # Verify logging occurred
        assert mock_logger.info.called
        log_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any(
            "compliance" in msg.lower() or "tool" in msg.lower() for msg in log_messages
        )
