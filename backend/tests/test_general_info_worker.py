"""
Unit tests for General Information Worker Agent.

Tests the general information worker agent creation, tool wrapper functionality,
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
class TestGeneralInfoWorkerCreation:
    """Test general information worker agent creation and configuration."""

    @patch("agents.workers.general_info.create_agent")
    def test_create_general_info_worker(self, mock_create_agent, mock_openai_key):
        """Test that general info worker agent can be created."""
        from agents.workers.general_info import create_general_info_agent

        # Mock the return value
        mock_agent = Mock()
        mock_agent.name = "general_info_agent"
        mock_create_agent.return_value = mock_agent

        # Create general info worker
        worker = create_general_info_agent()

        # Verify create_agent was called with correct parameters
        mock_create_agent.assert_called_once()
        call_kwargs = mock_create_agent.call_args[1]

        assert call_kwargs["model"] == "openai:gpt-4o-mini"
        assert call_kwargs["tools"] == []  # Worker has no tools
        assert call_kwargs["name"] == "general_info_agent"
        assert "system_prompt" in call_kwargs

        # Verify worker was created
        assert worker is not None
        assert worker.name == "general_info_agent"

    @patch("agents.workers.general_info.create_agent")
    def test_general_info_worker_system_prompt_is_specialized(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that general info worker has specialized system prompt."""
        from agents.workers.general_info import create_general_info_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_general_info_agent()

        # Get the system prompt from the call
        call_kwargs = mock_create_agent.call_args[1]
        system_prompt = call_kwargs["system_prompt"]

        # Verify general info concepts are in the prompt
        assert "general" in system_prompt.lower() or "information" in system_prompt.lower()
        assert any(
            word in system_prompt.lower()
            for word in ["company", "service", "feature", "information", "help"]
        )

    def test_create_general_info_worker_without_api_key(self):
        """Test that general info worker creation fails without API key."""
        from agents.workers.general_info import create_general_info_agent

        # Clear OPENAI_API_KEY
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        # Should raise ValueError
        with pytest.raises(ValueError, match="OPENAI_API_KEY must be set"):
            create_general_info_agent()

    @patch("agents.workers.general_info.create_agent")
    def test_general_info_worker_has_no_checkpointer(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that general info worker doesn't use checkpointer (supervisor handles memory)."""
        from agents.workers.general_info import create_general_info_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_general_info_agent()

        # Verify checkpointer is NOT passed (supervisor handles conversation memory)
        call_kwargs = mock_create_agent.call_args[1]
        assert (
            "checkpointer" not in call_kwargs or call_kwargs.get("checkpointer") is None
        )


class TestGeneralInfoWorkerGetter:
    """Test the get_general_info_agent() function."""

    @patch("agents.workers.general_info.general_info_agent", None)
    def test_get_general_info_agent_when_not_initialized(self):
        """Test that get_general_info_agent raises error when agent is None."""
        from agents.workers.general_info import get_general_info_agent

        with pytest.raises(RuntimeError, match="General information agent is not initialized"):
            get_general_info_agent()

    @patch("agents.workers.general_info.general_info_agent")
    def test_get_general_info_agent_when_initialized(self, mock_agent):
        """Test that get_general_info_agent returns the agent when initialized."""
        from agents.workers.general_info import get_general_info_agent

        mock_agent.name = "general_info_agent"

        agent = get_general_info_agent()

        assert agent is not None
        assert agent.name == "general_info_agent"


class TestGeneralInfoWorkerConfiguration:
    """Test general info worker agent configuration details."""

    @patch("agents.workers.general_info.create_agent")
    def test_general_info_worker_model_is_gpt4o_mini(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that general info worker uses GPT-4o-mini model."""
        from agents.workers.general_info import create_general_info_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_general_info_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["model"] == "openai:gpt-4o-mini"

    @patch("agents.workers.general_info.create_agent")
    def test_general_info_worker_has_descriptive_name(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that general info worker has a descriptive name for debugging."""
        from agents.workers.general_info import create_general_info_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_general_info_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["name"] == "general_info_agent"
        assert "general" in call_kwargs["name"] or "info" in call_kwargs["name"]

    @patch("agents.workers.general_info.create_agent")
    def test_general_info_worker_has_no_tools(self, mock_create_agent, mock_openai_key):
        """Test that general info worker has no tools (Phase 4 - tools added in Phase 5+)."""
        from agents.workers.general_info import create_general_info_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_general_info_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["tools"] == []


class TestGeneralInfoToolWrapper:
    """Test the general_info_tool wrapper functionality."""

    @patch("agents.workers.general_info.get_general_info_agent")
    def test_general_info_tool_wrapper_calls_agent(self, mock_get_agent, mock_openai_key):
        """Test that general_info_tool correctly invokes the general info agent."""
        from agents.workers.general_info import general_info_tool

        # Mock the general info agent
        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "We offer cloud services and support."
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        # Call the tool wrapper
        query = "What services do you offer?"
        result = general_info_tool.invoke({"query": query})

        # Verify agent was invoked with correct format
        mock_agent.invoke.assert_called_once()
        call_args = mock_agent.invoke.call_args[0][0]
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"] == query

        # Verify response was extracted correctly
        assert result == "We offer cloud services and support."

    @patch("agents.workers.general_info.get_general_info_agent")
    def test_general_info_tool_has_descriptive_name(self, mock_get_agent, mock_openai_key):
        """Test that general_info_tool has a descriptive name."""
        from agents.workers.general_info import general_info_tool

        assert general_info_tool.name == "general_info_tool"
        assert "general" in general_info_tool.name or "info" in general_info_tool.name

    @patch("agents.workers.general_info.get_general_info_agent")
    def test_general_info_tool_has_clear_description(
        self, mock_get_agent, mock_openai_key
    ):
        """Test that general_info_tool has a clear description for routing."""
        from agents.workers.general_info import general_info_tool

        description = general_info_tool.description

        # Should mention key general info concepts
        assert any(
            word in description.lower()
            for word in ["company", "service", "feature", "information", "general"]
        )

    @patch("agents.workers.general_info.get_general_info_agent")
    def test_general_info_tool_returns_string(self, mock_get_agent, mock_openai_key):
        """Test that general_info_tool returns a string response."""
        from agents.workers.general_info import general_info_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "General information response"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = general_info_tool.invoke({"query": "test query"})

        assert isinstance(result, str)
        assert result == "General information response"


class TestGeneralInfoWorkerResponses:
    """Test general info worker responses to various query types."""

    @patch("agents.workers.general_info.get_general_info_agent")
    def test_general_info_tool_handles_services_query(
        self, mock_get_agent, mock_openai_key
    ):
        """Test general info tool handles service queries."""
        from agents.workers.general_info import general_info_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "We provide cloud hosting, data storage, and analytics"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = general_info_tool.invoke({"query": "What services do you provide?"})

        assert "service" in result.lower() or "provide" in result.lower()

    @patch("agents.workers.general_info.get_general_info_agent")
    def test_general_info_tool_handles_company_query(
        self, mock_get_agent, mock_openai_key
    ):
        """Test general info tool handles company information queries."""
        from agents.workers.general_info import general_info_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "We are a leading tech company founded in 2020"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = general_info_tool.invoke({"query": "Tell me about your company"})

        assert "company" in result.lower() or "tech" in result.lower()

    @patch("agents.workers.general_info.get_general_info_agent")
    def test_general_info_tool_handles_features_query(
        self, mock_get_agent, mock_openai_key
    ):
        """Test general info tool handles feature queries."""
        from agents.workers.general_info import general_info_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Our platform features include automated backups and monitoring"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = general_info_tool.invoke({"query": "What features do you have?"})

        assert "feature" in result.lower() or "platform" in result.lower()


class TestGeneralInfoWorkerLogging:
    """Test general info worker logging behavior."""

    @patch("agents.workers.general_info.logger")
    @patch("agents.workers.general_info.create_agent")
    def test_general_info_worker_logs_creation(
        self, mock_create_agent, mock_logger, mock_openai_key
    ):
        """Test that general info worker logs creation."""
        from agents.workers.general_info import create_general_info_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_general_info_agent()

        # Verify logging occurred
        assert mock_logger.info.called
        log_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("general" in msg.lower() or "information" in msg.lower() for msg in log_messages)

    @patch("agents.workers.general_info.logger")
    @patch("agents.workers.general_info.get_general_info_agent")
    def test_general_info_tool_logs_invocation(
        self, mock_get_agent, mock_logger, mock_openai_key
    ):
        """Test that general_info_tool logs when it's called."""
        from agents.workers.general_info import general_info_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "General info response"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        general_info_tool.invoke({"query": "test query"})

        # Verify logging occurred
        assert mock_logger.info.called
        log_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any(
            "general" in msg.lower() or "info" in msg.lower() or "tool" in msg.lower() 
            for msg in log_messages
        )

