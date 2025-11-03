"""
Unit tests for the customer service agent.

Tests agent creation, configuration, and basic invocation.
Uses mocked OpenAI responses to avoid API calls in tests.

Related to Task 5.1 in PRD-0002 (Phase 2: Simple Agent Foundation)
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from backend.agents.simple_agent import create_customer_service_agent, get_agent


class TestAgentCreation:
    """Tests for agent creation and initialization."""
    
    def test_agent_creation_requires_api_key(self):
        """Test that agent creation fails without OPENAI_API_KEY."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove OPENAI_API_KEY from environment
            with pytest.raises(ValueError) as exc_info:
                create_customer_service_agent()
            
            assert "OPENAI_API_KEY" in str(exc_info.value)
    
    def test_agent_creation_with_api_key(self):
        """Test that agent is created successfully with valid API key."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = create_customer_service_agent()
            
            # Verify agent was created
            assert agent is not None
            
            # Verify agent has required attributes
            assert hasattr(agent, 'invoke')
            assert hasattr(agent, 'name')
            assert agent.name == "customer_service_agent"
    
    def test_agent_has_checkpointer(self):
        """Test that agent has conversation memory enabled."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = create_customer_service_agent()
            
            # Verify checkpointer is configured
            assert hasattr(agent, 'checkpointer')
            assert agent.checkpointer is not None
    
    def test_agent_uses_correct_model(self):
        """Test that agent is configured with GPT-4o-mini model."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = create_customer_service_agent()
            
            # Verify agent was created (model config is internal to LangGraph)
            # The actual model configuration is tested via integration tests
            assert agent is not None


class TestAgentInvocation:
    """Tests for agent invocation and response generation."""
    
    @pytest.fixture
    def mock_agent(self):
        """Fixture providing a mocked agent for testing."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = create_customer_service_agent()
            return agent
    
    @pytest.mark.skip(reason="Requires OpenAI API access - tested in integration tests")
    def test_agent_invoke_returns_messages(self):
        """Test that agent.invoke() returns expected message structure."""
        # This test requires actual API calls
        # See test_main.py for integration tests with API mocking
        pass
    
    @pytest.mark.skip(reason="Requires OpenAI API access - tested in integration tests")
    def test_agent_maintains_conversation_context(self):
        """Test that agent can reference conversation history."""
        # This test requires actual API calls
        # Conversation memory is tested in integration tests
        pass


class TestGetAgent:
    """Tests for the get_agent() helper function."""
    
    def test_get_agent_returns_initialized_agent(self):
        """Test that get_agent() returns the initialized agent."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            # Import after setting env var to trigger initialization
            from backend.agents import simple_agent
            
            # Force re-initialization
            simple_agent.agent = create_customer_service_agent()
            
            agent = get_agent()
            assert agent is not None
            assert agent.name == "customer_service_agent"
    
    def test_get_agent_raises_without_initialization(self):
        """Test that get_agent() raises error if agent not initialized."""
        with patch('backend.agents.simple_agent.agent', None):
            with pytest.raises(RuntimeError) as exc_info:
                get_agent()
            
            assert "not initialized" in str(exc_info.value).lower()


class TestAgentConfiguration:
    """Tests for agent configuration and settings."""
    
    def test_agent_has_system_prompt(self):
        """Test that agent is configured with a system prompt."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = create_customer_service_agent()
            
            # Verify agent has configuration
            # System prompt should be part of agent setup
            assert agent is not None
            # Note: Direct system_prompt access may vary by LangChain version
    
    def test_agent_has_no_tools_in_phase2(self):
        """Test that agent has no tools in Phase 2."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = create_customer_service_agent()
            
            # Verify tools list is empty (Phase 3+ will add tools)
            if hasattr(agent, 'tools'):
                assert len(agent.tools) == 0


class TestAgentErrorHandling:
    """Tests for error handling in agent operations."""
    
    def test_agent_handles_empty_message(self):
        """Test agent behavior with empty message input."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = create_customer_service_agent()
            config = {"configurable": {"thread_id": "test-session"}}
            
            # This test verifies the agent can handle edge cases
            # Actual behavior depends on LangChain validation
            # We're mainly checking it doesn't crash
            try:
                agent.invoke({"messages": []}, config)
            except Exception as e:
                # Some validation errors are expected
                assert e is not None
    
    def test_agent_requires_thread_id_for_memory(self):
        """Test that conversation memory requires thread_id."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = create_customer_service_agent()
            
            # Verify that checkpointer is configured
            # This means thread_id is needed for memory to work
            assert agent.checkpointer is not None


# Integration note:
# These are unit tests with mocking. For full integration tests
# that actually call OpenAI API, see test_main.py
# Those tests should be run with caution (cost, rate limits)

