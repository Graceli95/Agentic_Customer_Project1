"""
Unit tests for Supervisor Agent.

Tests the supervisor agent creation, configuration, and basic functionality
without making actual API calls to OpenAI.

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


@pytest.fixture
def mock_tool():
    """Create a mock tool for testing."""
    tool = Mock()
    tool.name = "test_tool"
    tool.description = "A test tool"
    return tool


# Test Cases
class TestSupervisorAgentCreation:
    """Test supervisor agent creation and configuration."""

    @patch("agents.supervisor_agent.create_agent")
    def test_create_supervisor_with_tools(self, mock_create_agent, mock_openai_key, mock_tool):
        """Test that supervisor agent can be created with tools."""
        from agents.supervisor_agent import create_supervisor_agent

        # Mock the return value
        mock_agent = Mock()
        mock_agent.name = "supervisor_agent"
        mock_create_agent.return_value = mock_agent

        # Create supervisor with mock tool
        supervisor = create_supervisor_agent(tools=[mock_tool])

        # Verify create_agent was called with correct parameters
        mock_create_agent.assert_called_once()
        call_kwargs = mock_create_agent.call_args[1]

        assert call_kwargs["model"] == "openai:gpt-4o-mini"
        assert call_kwargs["tools"] == [mock_tool]
        assert call_kwargs["name"] == "supervisor_agent"
        assert "system_prompt" in call_kwargs
        assert "checkpointer" in call_kwargs

        # Verify supervisor was created
        assert supervisor is not None
        assert supervisor.name == "supervisor_agent"

    @patch("agents.supervisor_agent.create_agent")
    def test_supervisor_system_prompt_contains_routing_logic(
        self, mock_create_agent, mock_openai_key, mock_tool
    ):
        """Test that supervisor system prompt includes routing guidelines."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_supervisor_agent(tools=[mock_tool])

        # Get the system prompt from the call
        call_kwargs = mock_create_agent.call_args[1]
        system_prompt = call_kwargs["system_prompt"]

        # Verify key routing concepts are in the prompt
        assert "supervisor" in system_prompt.lower()
        assert "route" in system_prompt.lower() or "routing" in system_prompt.lower()
        assert "technical" in system_prompt.lower()
        assert "tool" in system_prompt.lower()

    def test_create_supervisor_without_api_key(self, mock_tool):
        """Test that supervisor creation fails without API key."""
        from agents.supervisor_agent import create_supervisor_agent

        # Clear OPENAI_API_KEY
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        # Should raise ValueError
        with pytest.raises(ValueError, match="OPENAI_API_KEY must be set"):
            create_supervisor_agent(tools=[mock_tool])

    @patch("agents.supervisor_agent.create_agent")
    def test_supervisor_uses_checkpointer(
        self, mock_create_agent, mock_openai_key, mock_tool
    ):
        """Test that supervisor is configured with checkpointer for memory."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_supervisor_agent(tools=[mock_tool])

        # Verify checkpointer is passed
        call_kwargs = mock_create_agent.call_args[1]
        assert "checkpointer" in call_kwargs
        assert call_kwargs["checkpointer"] is not None


class TestSupervisorAgentGetter:
    """Test the get_supervisor() function."""

    @patch("agents.supervisor_agent.supervisor", None)
    def test_get_supervisor_when_not_initialized(self):
        """Test that get_supervisor raises error when supervisor is None."""
        from agents.supervisor_agent import get_supervisor

        with pytest.raises(RuntimeError, match="Supervisor agent is not initialized"):
            get_supervisor()

    @patch("agents.supervisor_agent.supervisor")
    def test_get_supervisor_when_initialized(self, mock_supervisor):
        """Test that get_supervisor returns the supervisor when initialized."""
        from agents.supervisor_agent import get_supervisor

        mock_supervisor.name = "supervisor_agent"

        supervisor = get_supervisor()

        assert supervisor is not None
        assert supervisor.name == "supervisor_agent"


class TestSupervisorConfiguration:
    """Test supervisor agent configuration details."""

    @patch("agents.supervisor_agent.create_agent")
    def test_supervisor_model_is_gpt4o_mini(
        self, mock_create_agent, mock_openai_key, mock_tool
    ):
        """Test that supervisor uses GPT-4o-mini model."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_supervisor_agent(tools=[mock_tool])

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["model"] == "openai:gpt-4o-mini"

    @patch("agents.supervisor_agent.create_agent")
    def test_supervisor_has_descriptive_name(
        self, mock_create_agent, mock_openai_key, mock_tool
    ):
        """Test that supervisor has a descriptive name for logging/tracing."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_supervisor_agent(tools=[mock_tool])

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["name"] == "supervisor_agent"

    @patch("agents.supervisor_agent.create_agent")
    def test_supervisor_accepts_multiple_tools(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that supervisor can be created with multiple tools."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        # Create multiple mock tools
        tool1 = Mock()
        tool1.name = "technical_support"
        tool2 = Mock()
        tool2.name = "billing_support"

        create_supervisor_agent(tools=[tool1, tool2])

        call_kwargs = mock_create_agent.call_args[1]
        assert len(call_kwargs["tools"]) == 2
        assert call_kwargs["tools"] == [tool1, tool2]


class TestSupervisorLogging:
    """Test logging behavior of supervisor agent."""

    @patch("agents.supervisor_agent.create_agent")
    @patch("agents.supervisor_agent.logger")
    def test_supervisor_logs_creation(
        self, mock_logger, mock_create_agent, mock_openai_key, mock_tool
    ):
        """Test that supervisor logs when created."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_supervisor_agent(tools=[mock_tool])

        # Verify logging calls
        mock_logger.info.assert_any_call("Creating supervisor agent with 1 worker tools")
        mock_logger.info.assert_any_call("Supervisor agent created successfully")

    @patch("agents.supervisor_agent.create_agent")
    @patch("agents.supervisor_agent.logger")
    def test_supervisor_logs_tool_count(
        self, mock_logger, mock_create_agent, mock_openai_key
    ):
        """Test that supervisor logs the number of tools."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        # Create with 3 tools
        tools = [Mock() for _ in range(3)]
        create_supervisor_agent(tools=tools)

        mock_logger.info.assert_any_call("Creating supervisor agent with 3 worker tools")


class TestSupervisorErrorHandling:
    """Test error handling in supervisor agent."""

    @patch("agents.supervisor_agent.logger")
    def test_supervisor_logs_error_on_missing_key(self, mock_logger):
        """Test that supervisor logs error when API key is missing."""
        from agents.supervisor_agent import create_supervisor_agent

        # Clear API key
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        try:
            create_supervisor_agent(tools=[])
        except ValueError:
            pass

        mock_logger.error.assert_called_once_with(
            "OPENAI_API_KEY environment variable is not set"
        )

    @patch("agents.supervisor_agent.create_agent")
    def test_supervisor_with_empty_tools_list(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that supervisor can be created with empty tools list."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        # Should not raise error
        supervisor = create_supervisor_agent(tools=[])

        assert supervisor is not None
        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["tools"] == []


# Integration-like tests (still mocked but closer to real usage)
class TestSupervisorIntegration:
    """Test supervisor agent in more realistic scenarios."""

    @patch("agents.supervisor_agent.create_agent")
    def test_supervisor_with_technical_support_tool_structure(
        self, mock_create_agent, mock_openai_key
    ):
        """Test supervisor with a tool structure similar to technical_support_tool."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        # Create a mock tool that mimics technical_support_tool
        mock_tech_tool = Mock()
        mock_tech_tool.name = "technical_support_tool"
        mock_tech_tool.description = "Handle technical support questions"

        supervisor = create_supervisor_agent(tools=[mock_tech_tool])

        assert supervisor is not None

        # Verify the tool was passed correctly
        call_kwargs = mock_create_agent.call_args[1]
        assert len(call_kwargs["tools"]) == 1
        assert call_kwargs["tools"][0].name == "technical_support_tool"

    @patch("agents.supervisor_agent.create_agent")
    def test_supervisor_system_prompt_mentions_workers(
        self, mock_create_agent, mock_openai_key, mock_tool
    ):
        """Test that system prompt references worker agents."""
        from agents.supervisor_agent import create_supervisor_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_supervisor_agent(tools=[mock_tool])

        call_kwargs = mock_create_agent.call_args[1]
        system_prompt = call_kwargs["system_prompt"].lower()

        # Should mention concepts related to workers
        assert any(
            word in system_prompt
            for word in ["worker", "specialist", "support", "technical"]
        )


# Run tests with: pytest backend/tests/test_supervisor.py -v

