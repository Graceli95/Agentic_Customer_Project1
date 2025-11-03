"""
Technical Support Worker Agent for Multi-Agent System.

This module creates a specialized technical support agent that handles
technical queries, troubleshooting, errors, and bugs. It's called as a tool
by the supervisor agent using the tool-calling pattern.

Phase: 3 - Multi-Agent Supervisor Architecture
LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/multi-agent
Last Updated: November 3, 2025
"""

from langchain.agents import create_agent
import os
import logging

logger = logging.getLogger(__name__)


def create_technical_support_agent():
    """
    Create a specialized technical support agent.

    This agent is an expert in troubleshooting technical issues, diagnosing
    problems, and providing step-by-step solutions. It will be wrapped as
    a tool for the supervisor to call when technical queries are detected.

    The agent:
    - Diagnoses technical problems
    - Explains error messages
    - Provides troubleshooting steps
    - Suggests solutions and workarounds
    - No tools yet (Phase 5 will add RAG for technical docs)

    Returns:
        Agent: Configured LangChain technical support agent

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set

    Example:
        >>> agent = create_technical_support_agent()
        >>> result = agent.invoke({
        ...     "messages": [{"role": "user", "content": "Error 500 on login"}]
        ... })
        >>> print(result["messages"][-1].content)
    """
    # Validate OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable is not set")
        raise ValueError(
            "OPENAI_API_KEY must be set in environment variables. "
            "Please add it to your .env file."
        )

    logger.info("Creating technical support worker agent")

    # System prompt: Defines technical specialist role
    system_prompt = """You are a technical support specialist with expertise in troubleshooting software issues.

Your role is to:
- Diagnose technical problems thoroughly
- Provide clear, step-by-step solutions
- Explain error messages in user-friendly language
- Guide users through troubleshooting processes
- Suggest preventive measures when appropriate
- Ask clarifying questions when you need more information

Technical Areas You Cover:
- Software errors and error codes (500, 404, 403, etc.)
- Application crashes and freezes
- Installation and setup problems
- Configuration issues
- Performance and slowness problems
- Login and authentication issues
- Feature malfunctions
- Bug reports and unexpected behavior

Response Guidelines:
- Start by acknowledging the issue
- Ask for specific details if needed (error messages, steps to reproduce, etc.)
- Provide numbered troubleshooting steps
- Explain WHY each step helps (educate the user)
- Use clear, non-technical language when possible
- Offer multiple solutions if available (workarounds, permanent fixes)
- End with "Let me know if this resolves the issue or if you need further help"

CRITICAL INSTRUCTION:
- The supervisor agent only sees your FINAL response
- Include ALL findings, steps, and solutions in your final message
- Don't assume follow-up - make your response complete and self-contained
- If you need more information, ask in your response

Example Good Response:
"I understand you're experiencing Error 500 during login. This is a server error that usually indicates a backend issue. Let me help you troubleshoot:

1. **Clear your browser cache and cookies**
   - This resolves most login issues caused by stale session data
   - Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)

2. **Try a different browser**
   - This helps identify if it's browser-specific

3. **Check if the service is operational**
   - Visit our status page at status.example.com

If these steps don't work, the issue is likely on our end. Please let me know:
- What browser are you using?
- When did the error first occur?
- Can you share the exact error message?

This will help me investigate further."

Remember: Your response goes directly to the user through the supervisor.
Make it thorough, helpful, and complete."""

    # Create technical support agent using LangChain v1.0 pattern
    agent = create_agent(
        model="openai:gpt-4o-mini",  # Cost-effective model
        # To upgrade: model="openai:gpt-4o" for higher quality responses
        tools=[],  # No tools yet - Phase 5 will add RAG search tool
        system_prompt=system_prompt,
        checkpointer=None,  # No memory needed - called as tool, not directly
        # Each call is independent - supervisor maintains conversation context
        name="technical_support_agent",  # Required in LangChain v1.0
    )

    logger.info("Technical support worker agent created successfully")
    return agent


# Initialize agent once at module level for reuse
try:
    technical_agent = create_technical_support_agent()
    logger.info("Technical support agent initialized and ready")
except ValueError as e:
    logger.error(f"Failed to initialize technical support agent: {e}")
    technical_agent = None


def get_technical_agent():
    """
    Get the initialized technical support agent.

    Returns:
        Agent: The initialized technical support agent instance

    Raises:
        RuntimeError: If agent failed to initialize (e.g., missing API key)

    Example:
        >>> agent = get_technical_agent()
        >>> result = agent.invoke({...})
    """
    if technical_agent is None:
        raise RuntimeError(
            "Technical support agent is not initialized. "
            "Check that OPENAI_API_KEY is set."
        )
    return technical_agent
