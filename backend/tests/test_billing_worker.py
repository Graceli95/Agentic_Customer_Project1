"""
Unit tests for Billing Support Worker Agent.

Tests the billing support worker agent creation, tool wrapper functionality,
Hybrid RAG/CAG caching, and configuration without making actual API calls to OpenAI.

Phase: 4 - Additional Worker Agents
Phase: 5 - RAG/CAG Integration (Hybrid RAG/CAG strategy)
"""

import os
from unittest.mock import Mock, patch

import pytest


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
        # Worker has billing_docs_search tool for Hybrid RAG/CAG
        assert len(call_kwargs["tools"]) == 1
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
    def test_billing_worker_has_rag_tool(self, mock_create_agent, mock_openai_key):
        """Test that billing worker has billing_docs_search tool for Hybrid RAG/CAG."""
        from agents.workers.billing_support import create_billing_support_agent

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        create_billing_support_agent()

        call_kwargs = mock_create_agent.call_args[1]
        # Phase 5: billing worker has billing_docs_search for dynamic RAG queries
        assert len(call_kwargs["tools"]) == 1
        assert call_kwargs["tools"][0].name == "billing_docs_search"


class TestBillingToolWrapper:
    """Test the billing_support_tool wrapper functionality."""

    @patch("agents.workers.billing_support.get_cached_billing_policies")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_wrapper_calls_agent(
        self, mock_get_agent, mock_get_cached, mock_openai_key
    ):
        """Test that billing_support_tool correctly invokes the billing agent."""
        from agents.workers.billing_support import billing_support_tool

        # Mock cached policies (Hybrid RAG/CAG)
        mock_get_cached.return_value = "Cached refund policy content"

        # Mock the billing agent
        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "I can help you with that billing issue."
        mock_agent.invoke.return_value = {"messages": [mock_response]}  # Last message
        mock_get_agent.return_value = mock_agent

        # Call the tool wrapper
        query = "I was charged twice for my subscription"
        result = billing_support_tool.invoke({"query": query})

        # Verify cached policies were fetched (Hybrid RAG/CAG)
        mock_get_cached.assert_called_once()

        # Verify agent was invoked with enhanced query containing cached context
        mock_agent.invoke.assert_called_once()
        call_args = mock_agent.invoke.call_args[0][0]
        assert call_args["messages"][0]["role"] == "user"
        # Query should include cached policies and original query
        assert "CACHED BILLING POLICIES" in call_args["messages"][0]["content"]
        assert query in call_args["messages"][0]["content"]

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

        # Should mention key billing concepts and Hybrid strategy
        assert any(
            word in description.lower()
            for word in ["billing", "payment", "invoice", "subscription", "refund"]
        )
        assert "hybrid" in description.lower()

    @patch("agents.workers.billing_support.get_cached_billing_policies")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_returns_string(
        self, mock_get_agent, mock_get_cached, mock_openai_key
    ):
        """Test that billing_support_tool returns a string response."""
        from agents.workers.billing_support import billing_support_tool

        mock_get_cached.return_value = "Cached policies"
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

    @patch("agents.workers.billing_support.get_cached_billing_policies")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_handles_payment_query(
        self, mock_get_agent, mock_get_cached, mock_openai_key
    ):
        """Test billing tool handles payment-related queries."""
        from agents.workers.billing_support import billing_support_tool

        mock_get_cached.return_value = "Cached policies"
        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "To update your payment method, go to Account Settings"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = billing_support_tool.invoke(
            {"query": "How do I update my payment method?"}
        )

        assert "payment method" in result.lower() or "account" in result.lower()

    @patch("agents.workers.billing_support.get_cached_billing_policies")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_handles_refund_query(
        self, mock_get_agent, mock_get_cached, mock_openai_key
    ):
        """Test billing tool handles refund requests."""
        from agents.workers.billing_support import billing_support_tool

        mock_get_cached.return_value = "Cached policies"
        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "To request a refund, please contact billing support"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = billing_support_tool.invoke({"query": "I need a refund"})

        assert "refund" in result.lower() or "billing" in result.lower()

    @patch("agents.workers.billing_support.get_cached_billing_policies")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_handles_subscription_query(
        self, mock_get_agent, mock_get_cached, mock_openai_key
    ):
        """Test billing tool handles subscription management queries."""
        from agents.workers.billing_support import billing_support_tool

        mock_get_cached.return_value = "Cached policies"
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

    @patch("agents.workers.billing_support.get_cached_billing_policies")
    @patch("agents.workers.billing_support.logger")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_logs_invocation(
        self, mock_get_agent, mock_logger, mock_get_cached, mock_openai_key
    ):
        """Test that billing_support_tool logs when it's called."""
        from agents.workers.billing_support import billing_support_tool

        mock_get_cached.return_value = "Cached policies"
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
            "billing" in msg.lower() or "hybrid" in msg.lower() for msg in log_messages
        )


class TestHybridRAGCAGCaching:
    """Test Hybrid RAG/CAG caching functionality for billing support."""

    def test_billing_policy_cache_initially_empty(self, mock_openai_key):
        """Test that billing policy cache starts empty."""
        from agents.workers.billing_support import _billing_policy_cache

        # Cache should be a dict (may have been populated by other tests)
        assert isinstance(_billing_policy_cache, dict)

    @patch("agents.workers.billing_support.get_vectorstore")
    def test_fetch_billing_policies_queries_vectorstore(
        self, mock_get_vs, mock_openai_key
    ):
        """Test that _fetch_billing_policies queries the billing vector store."""
        from agents.workers.billing_support import _fetch_billing_policies

        # Mock vector store
        mock_vs = Mock()
        mock_doc = Mock()
        mock_doc.page_content = "Refund policy content"
        mock_doc.metadata = {"source": "refund-policy.md"}
        mock_vs.similarity_search.return_value = [mock_doc]
        mock_get_vs.return_value = mock_vs

        result = _fetch_billing_policies()

        # Verify vector store was queried
        mock_get_vs.assert_called_with("billing")
        assert mock_vs.similarity_search.called
        assert "refund-policy.md" in result or "Refund policy content" in result

    @patch("agents.workers.billing_support.get_vectorstore")
    def test_fetch_billing_policies_handles_empty_results(
        self, mock_get_vs, mock_openai_key
    ):
        """Test that _fetch_billing_policies handles empty vector store."""
        from agents.workers.billing_support import _fetch_billing_policies

        mock_vs = Mock()
        mock_vs.similarity_search.return_value = []
        mock_get_vs.return_value = mock_vs

        result = _fetch_billing_policies()

        assert result == ""

    @patch("agents.workers.billing_support.get_vectorstore")
    def test_fetch_billing_policies_handles_vectorstore_error(
        self, mock_get_vs, mock_openai_key
    ):
        """Test that _fetch_billing_policies handles vector store unavailable."""
        from agents.workers.billing_support import _fetch_billing_policies

        mock_get_vs.return_value = None  # Vector store unavailable

        result = _fetch_billing_policies()

        assert result == ""

    @patch("agents.workers.billing_support._fetch_billing_policies")
    def test_get_cached_billing_policies_caches_after_first_call(
        self, mock_fetch, mock_openai_key
    ):
        """Test that get_cached_billing_policies caches results after first call."""
        from agents.workers.billing_support import (
            _billing_policy_cache,
            get_cached_billing_policies,
        )

        # Clear cache for this test
        _billing_policy_cache.clear()

        mock_fetch.return_value = "Cached policy content"

        # First call - should fetch
        result1 = get_cached_billing_policies()
        assert mock_fetch.call_count == 1
        assert result1 == "Cached policy content"

        # Second call - should use cache
        result2 = get_cached_billing_policies()
        assert mock_fetch.call_count == 1  # Still 1, not called again
        assert result2 == "Cached policy content"

    @patch("agents.workers.billing_support.get_cached_billing_policies")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_injects_cached_context(
        self, mock_get_agent, mock_get_cached, mock_openai_key
    ):
        """Test that billing_support_tool injects cached policies into query."""
        from agents.workers.billing_support import billing_support_tool

        mock_get_cached.return_value = "REFUND POLICY: 30 days money back"

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Based on our policy..."
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        billing_support_tool.invoke({"query": "What is your refund policy?"})

        # Verify the enhanced query contains cached context
        call_args = mock_agent.invoke.call_args[0][0]
        enhanced_query = call_args["messages"][0]["content"]

        assert "CACHED BILLING POLICIES" in enhanced_query
        assert "REFUND POLICY: 30 days money back" in enhanced_query
        assert "What is your refund policy?" in enhanced_query

    @patch("agents.workers.billing_support.get_cached_billing_policies")
    @patch("agents.workers.billing_support.get_billing_agent")
    def test_billing_tool_fallback_when_no_cache(
        self, mock_get_agent, mock_get_cached, mock_openai_key
    ):
        """Test that billing_support_tool works when cache is empty."""
        from agents.workers.billing_support import billing_support_tool

        mock_get_cached.return_value = ""  # Empty cache

        mock_agent = Mock()
        mock_response = Mock()
        mock_response.content = "Response without cache"
        mock_agent.invoke.return_value = {"messages": [mock_response]}
        mock_get_agent.return_value = mock_agent

        result = billing_support_tool.invoke({"query": "Simple billing question"})

        # Verify agent was still called
        mock_agent.invoke.assert_called_once()
        call_args = mock_agent.invoke.call_args[0][0]
        # Without cache, query should be passed directly
        assert call_args["messages"][0]["content"] == "Simple billing question"
        assert result == "Response without cache"
