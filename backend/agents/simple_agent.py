"""
Simple Customer Service Agent using LangChain v1.0.

This module creates a single, stateful agent for Phase 2.
In Phase 3+, this will be replaced with a multi-agent system.

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Updated: November 3, 2025
"""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import os
import logging

logger = logging.getLogger(__name__)

# Initialize checkpointer for conversation memory
# InMemorySaver: Simple in-memory storage for development
# For production, upgrade to PostgresSaver or RedisSaver for persistence
checkpointer = InMemorySaver()


def create_customer_service_agent():
    """
    Create a simple customer service agent using LangChain v1.0.

    This agent:
    - Uses OpenAI GPT-4o-mini for cost-effective responses
    - Maintains conversation history via InMemorySaver checkpointer
    - Has no tools yet (Phase 3+ will add specialized tools)
    - Follows LangChain v1.0 best practices (using create_agent, not deprecated patterns)

    Returns:
        Agent: Configured LangChain agent with conversation memory

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set

    Example:
        >>> agent = create_customer_service_agent()
        >>> config = {"configurable": {"thread_id": "session-123"}}
        >>> result = agent.invoke(
        ...     {"messages": [{"role": "user", "content": "Hello"}]},
        ...     config
        ... )
        >>> print(result["messages"][-1].content)
    """
    # Validate OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable is not set")
        raise ValueError(
            "OPENAI_API_KEY must be set in environment variables. "
            "Please add it to your .env file."
        )

    logger.info("Creating customer service agent with GPT-4o-mini")

    # System prompt: Professional customer service persona
    system_prompt = """You are a helpful customer service assistant for our company.

Your role is to:
- Provide accurate, helpful information to customers
- Be professional, friendly, and empathetic
- Ask clarifying questions when needed
- Maintain context from the conversation history
- Address customer concerns with patience and understanding

Guidelines:
- Keep responses clear and concise while being thorough
- If you don't know something, say so honestly
- Suggest next steps or escalation when appropriate
- Use a warm, professional tone

Remember: You have access to the full conversation history, so reference 
previous messages when relevant to provide personalized assistance."""

    # Create agent using LangChain v1.0 pattern
    # ✅ DO: Use create_agent() from langchain.agents
    # ❌ DON'T: Use deprecated initialize_agent() or create_react_agent()
    agent = create_agent(
        model="openai:gpt-4o-mini",  # Cost-effective model for development
        # To upgrade to GPT-4: model="openai:gpt-4"
        # To use GPT-4 Turbo: model="openai:gpt-4-turbo"
        tools=[],  # No tools yet - Phase 3+ will add specialized agent tools
        system_prompt=system_prompt,
        checkpointer=checkpointer,  # Enables conversation memory per thread_id
        # Note: InMemorySaver loses data on restart
        # For production: Use PostgresSaver or RedisSaver
        name="customer_service_agent",  # Required in LangChain v1.0
        # Agent name helps with:
        # - Debugging and tracing in LangSmith
        # - Identifying agents in logs
        # - Multi-agent systems (Phase 3+)
    )

    logger.info("Customer service agent created successfully")
    return agent


# Initialize agent once at module level for reuse
# This avoids recreating the agent on every request
try:
    agent = create_customer_service_agent()
    logger.info("Agent initialized and ready for requests")
except ValueError as e:
    logger.error(f"Failed to initialize agent: {e}")
    agent = None


def get_agent():
    """
    Get the initialized customer service agent.

    Returns:
        Agent: The initialized agent instance

    Raises:
        RuntimeError: If agent failed to initialize (e.g., missing API key)
    """
    if agent is None:
        raise RuntimeError(
            "Agent is not initialized. Check that OPENAI_API_KEY is set."
        )
    return agent
