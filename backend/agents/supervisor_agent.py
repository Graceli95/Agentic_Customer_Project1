"""
Supervisor Agent for Multi-Agent Customer Service System.

This module creates a supervisor agent that routes queries to specialized
worker agents using the tool-calling pattern (LangChain v1.0).

Phase: 3 - Multi-Agent Supervisor Architecture
LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/multi-agent
Last Updated: November 3, 2025
"""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import os
import logging

logger = logging.getLogger(__name__)

# Initialize checkpointer for conversation memory
# Same checkpointer used by all agents to maintain context across routing
checkpointer = InMemorySaver()


def create_supervisor_agent(tools: list):
    """
    Create a supervisor agent that routes queries to specialized workers.

    The supervisor analyzes incoming user queries and decides whether to:
    1. Route to a specialized worker agent (via tool calling)
    2. Handle the query directly (for general/simple queries)

    This implements the "tool-calling pattern" where worker agents are
    wrapped as tools that the supervisor can invoke.

    Args:
        tools: List of worker agent tools (e.g., [technical_support_tool])

    Returns:
        Agent: Configured LangChain supervisor agent with routing capability

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set

    Example:
        >>> from backend.agents.workers import technical_support_tool
        >>> supervisor = create_supervisor_agent(tools=[technical_support_tool])
        >>> config = {"configurable": {"thread_id": "session-123"}}
        >>> result = supervisor.invoke(
        ...     {"messages": [{"role": "user", "content": "Error 500"}]},
        ...     config
        ... )
    """
    # Validate OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable is not set")
        raise ValueError(
            "OPENAI_API_KEY must be set in environment variables. "
            "Please add it to your .env file."
        )

    logger.info(f"Creating supervisor agent with {len(tools)} worker tools")

    # System prompt: Defines supervisor's role and routing logic
    system_prompt = """You are a supervisor agent that coordinates customer service inquiries.

Your role is to:
1. Analyze the user's query to understand their intent
2. Route technical questions to the Technical Support specialist
3. Handle general queries (greetings, thanks, clarifications) directly yourself
4. Provide clear, helpful responses to users

Available Tools:
- technical_support_tool: For technical issues, errors, bugs, troubleshooting, software problems

Routing Guidelines:
- Use technical_support_tool for ANY technical question:
  * Error messages or error codes
  * Software crashes, freezes, or bugs
  * Installation or setup problems
  * Technical configuration issues
  * Performance problems
  * "How do I..." technical questions
  * Troubleshooting requests

- Handle these yourself (DO NOT use tools):
  * Greetings: "Hello", "Hi", "Good morning"
  * Gratitude: "Thank you", "Thanks"
  * General chat: "How are you?"
  * Clarification: "What do you mean?"
  * Feedback: "That helped!"

Response Guidelines:
- Maintain a friendly, professional tone
- When using a tool, trust its response and pass it to the user
- Don't add unnecessary commentary to tool responses
- If the query is ambiguous, ask the user for clarification
- Keep responses concise but complete

Remember: You're coordinating specialists, not doing specialized work yourself.
When in doubt about whether to use a tool, use it - specialists are experts in their domains."""

    # Create supervisor agent using LangChain v1.0 pattern
    # ✅ DO: Use create_agent() from langchain.agents
    # ❌ DON'T: Use deprecated initialize_agent() or create_react_agent()
    supervisor = create_agent(
        model="openai:gpt-4o-mini",  # Fast, cost-effective model for routing
        # To upgrade: model="openai:gpt-4o" for better routing quality
        tools=tools,  # Worker agents wrapped as tools
        system_prompt=system_prompt,
        checkpointer=checkpointer,  # Shared memory for conversation continuity
        name="supervisor_agent",  # Required in LangChain v1.0
        # Agent name helps with:
        # - Debugging and tracing in LangSmith
        # - Identifying agents in logs
        # - Multi-agent systems coordination
    )

    logger.info("Supervisor agent created successfully")
    return supervisor


# Initialize supervisor once at module level for reuse
# Note: Worker tools will be registered when workers module imports this
try:
    # Import worker tools (relative import for backend package structure)
    from agents.workers import technical_support_tool

    # Create supervisor with available tools
    supervisor = create_supervisor_agent(tools=[technical_support_tool])
    logger.info("Supervisor initialized with worker tools")
except ImportError as e:
    # Workers not yet created - will be initialized later
    logger.warning(f"Workers not available yet: {e}")
    supervisor = None
except ValueError as e:
    logger.error(f"Failed to initialize supervisor: {e}")
    supervisor = None


def get_supervisor():
    """
    Get the initialized supervisor agent.

    Returns:
        Agent: The initialized supervisor agent instance

    Raises:
        RuntimeError: If supervisor failed to initialize (e.g., missing API key)

    Example:
        >>> supervisor = get_supervisor()
        >>> result = supervisor.invoke({...})
    """
    if supervisor is None:
        raise RuntimeError(
            "Supervisor agent is not initialized. "
            "Check that OPENAI_API_KEY is set and workers are available."
        )
    return supervisor

