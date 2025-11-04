"""
Unit tests for Billing Support Worker Agent.

Tests the billing support worker agent creation, tool wrapper functionality,
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
class TestBillingWorkerCreation:
    """Test billing support worker agent creation and configuration."""

    @patch("agents.workers.billing_support.create_agent")
    def test_create_billing_worker(self, mock_create_agent, mock_openai_key):
        """Test that billing worker agent can be created."""
        from agents.workers.billing_support import create_billing_support_agent

        # Mock the return value
        mock_agent = Mock()
        mock_agent.name = "billing_support_agent"
        mock_create_agent.return_value = mock_agent

        # Create billing worker
        worker = create_billing_support_agent()

        # Verify create_agent was called with correct parameters
        mock_create_agent.assert_called_once()
        call_kwargs = mock_create_agent.call_args[1]

        assert call_kwargs["model"] == "openai:gpt-4o-mini"
        assert call_kwargs["tools"] == []  # Worker has no tools
        assert call_kwargs["name"] == "billing_support_agent"
        assert "system_prompt" in call_kwargs

        # Verify worker was created
        assert worker is not None
        assert worker.name == "billing_support_agent"

    @patch("agents.workers.billing_support.create_agent")
    def test_billing_worker_system_prompt_is_specialized(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that billing worker has specialized system prompt."""
        from agents.workers.billing_support import create_billing_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_billing_support_agent()

        # Get the system prompt from the call
        call_kwargs = mock_create_agent.call_args[1]
        system_prompt = call_kwargs["system_prompt"]

        # Verify billing support concepts are in the prompt
        assert "billing" in system_prompt.lower() or "payment" in system_prompt.lower()
        assert any(
            word in system_prompt.lower()
            for word in ["payment", "invoice", "subscription", "refund", "charge"]
        )

    def test_create_billing_worker_without_api_key(self):
        """Test that billing worker creation fails without API key."""
        from agents.workers.billing_support import create_billing_support_agent

        # Clear OPENAI_API_KEY
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        # Should raise ValueError
        with pytest.raises(ValueError, match="OPENAI_API_KEY must be set"):
            create_billing_support_agent()

    @patch("agents.workers.billing_support.create_agent")
    def test_billing_worker_has_no_checkpointer(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that billing worker doesn't use checkpointer (supervisor handles memory)."""
        from agents.workers.billing_support import create_billing_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_billing_support_agent()

        # Verify checkpointer is NOT passed (supervisor handles conversation memory)
        call_kwargs = mock_create_agent.call_args[1]
        assert (
            "checkpointer" not in call_kwargs or call_kwargs.get("checkpointer") is None
        )


class TestBillingWorkerGetter:
    """Test the get_billing_agent() function."""

    @patch("agents.workers.billing_support.billing_agent", None)
    def test_get_billing_agent_when_not_initialized(self):
        """Test that get_billing_agent raises error when agent is None."""
        from agents.workers.billing_support import get_billing_agent

        with pytest.raises(
            RuntimeError, match="Billing support agent is not initialized"
        ):
            get_billing_agent()

    @patch("agents.workers.billing_support.billing_agent")
    def test_get_billing_agent_when_initialized(self, mock_agent):
        """Test that get_billing_agent returns the agent when initialized."""
        from agents.workers.billing_support import get_billing_agent

        mock_agent.name = "billing_support_agent"

        agent = get_billing_agent()

        assert agent is not None
        assert agent.name == "billing_support_agent"


class TestBillingWorkerConfiguration:
    """Test billing worker agent configuration details."""

    @patch("agents.workers.billing_support.create_agent")
    def test_billing_worker_model_is_gpt4o_mini(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that billing worker uses GPT-4o-mini model."""
        from agents.workers.billing_support import create_billing_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_billing_support_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["model"] == "openai:gpt-4o-mini"

    @patch("agents.workers.billing_support.create_agent")
    def test_billing_worker_has_descriptive_name(
        self, mock_create_agent, mock_openai_key
    ):
        """Test that billing worker has a descriptive name for debugging."""
        from agents.workers.billing_support import create_billing_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_billing_support_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["name"] == "billing_support_agent"
        assert "billing" in call_kwargs["name"]

    @patch("agents.workers.billing_support.create_agent")
    def test_billing_worker_has_no_tools(self, mock_create_agent, mock_openai_key):
        """Test that billing worker has no tools (Phase 4 - tools added in Phase 5+)."""
        from agents.workers.billing_support import create_billing_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_billing_support_agent()

        call_kwargs = mock_create_agent.call_args[1]
        assert call_kwargs["tools"] == []


class TestBillingToolWrapper:
    """Test the billing_support_tool wrapper functionality."""

    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_wrapper_calls_agent(self, mock_get_agent, mock_openai_key):
        """Test that billing_support_tool correctly invokes the billing agent."""
        from agents.workers.billing_support import billing_support_tool

        # Mock the billing agent
        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "I can help you with that billing issue."
        mock_agent.invoke.return_value = {"messages": [mock_response]}  # Last message
        mock_get_agent.return_value = mock_agent

        # Call the tool wrapper
        query = "I was charged twice for my subscription"
        result = billing_support_tool.invoke({"query": query})

        # Verify agent was invoked with correct format
        mock_agent.invoke.assert_called_once()
        call_args = mock_agent.invoke.call_args[0][0]
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"] == query

        # Verify response was extracted correctly
        assert result == "I can help you with that billing issue."

    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_has_descriptive_name(self, mock_get_agent, mock_openai_key):
        """Test that billing_support_tool has a descriptive name."""
        from agents.workers.billing_support import billing_support_tool

        assert billing_support_tool.name == "billing_support_tool"
        assert "billing" in billing_support_tool.name

    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_has_clear_description(self, mock_get_agent, mock_openai_key):
        """Test that billing_support_tool has a clear description for routing."""
        from agents.workers.billing_support import billing_support_tool

        description = billing_support_tool.description

        # Should mention key billing concepts
        assert any(
            word in description.lower()
            for word in ["billing", "payment", "invoice", "subscription", "refund"]
        )

    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_returns_string(self, mock_get_agent, mock_openai_key):
        """Test that billing_support_tool returns a string response."""
        from agents.workers.billing_support import billing_support_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Billing response text"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = billing_support_tool.invoke({"query": "test query"})

        assert isinstance(result, str)
        assert result == "Billing response text"


class TestBillingWorkerResponses:
    """Test billing worker responses to various query types."""

    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_handles_payment_query(self, mock_get_agent, mock_openai_key):
        """Test billing tool handles payment-related queries."""
        from agents.workers.billing_support import billing_support_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "To update your payment method, go to Account Settings"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = billing_support_tool.invoke(
            {"query": "How do I update my payment method?"}
        )

        assert "payment method" in result.lower() or "account" in result.lower()

    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_handles_refund_query(self, mock_get_agent, mock_openai_key):
        """Test billing tool handles refund requests."""
        from agents.workers.billing_support import billing_support_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "To request a refund, please contact billing support"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = billing_support_tool.invoke({"query": "I need a refund"})

        assert "refund" in result.lower() or "billing" in result.lower()

    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_handles_subscription_query(
        self, mock_get_agent, mock_openai_key
    ):
        """Test billing tool handles subscription management queries."""
        from agents.workers.billing_support import billing_support_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = (
            "You can cancel your subscription in Account Settings → Subscription"
        )
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = billing_support_tool.invoke(
            {"query": "How do I cancel my subscription?"}
        )

        assert "subscription" in result.lower() or "cancel" in result.lower()


class TestBillingWorkerLogging:
    """Test billing worker logging behavior."""

    @patch("agents.workers.billing_support.logger")
    @patch("agents.workers.billing_support.create_agent")
    def test_billing_worker_logs_creation(
        self, mock_create_agent, mock_logger, mock_openai_key
    ):
        """Test that billing worker logs creation."""
        from agents.workers.billing_support import create_billing_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_billing_support_agent()

        # Verify logging occurred
        assert mock_logger.info.called
        log_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("billing" in msg.lower() for msg in log_messages)

    @patch("agents.workers.billing_support.logger")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_logs_invocation(
        self, mock_get_agent, mock_logger, mock_openai_key
    ):
        """Test that billing_support_tool logs when it's called."""
        from agents.workers.billing_support import billing_support_tool

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Billing response"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        billing_support_tool.invoke({"query": "test query"})

        # Verify logging occurred
        assert mock_logger.info.called
        log_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any(
            "billing" in msg.lower() or "tool" in msg.lower() for msg in log_messages
        )
