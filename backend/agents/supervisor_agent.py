"""
Supervisor Agent for Multi-Agent Customer Service System.

This module creates a supervisor agent that routes queries to specialized
worker agents using the tool-calling pattern (LangChain v1.0).

Phase: 4 - Additional Worker Agents (4 workers total)
LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/multi-agent
Last Updated: November 4, 2025
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

    # System prompt: Defines supervisor's role and routing logic for all 4 workers
    system_prompt = """You are a supervisor agent that coordinates customer service inquiries across multiple specialized domains.

Your role is to:
1. Analyze the user's query to understand their intent and domain
2. Route queries to the appropriate specialist worker
3. Handle simple queries (greetings, thanks, clarifications) directly yourself
4. Provide clear, helpful responses to users

Available Specialist Workers (Tools):

1. **technical_support_tool** - Technical Support Specialist
   - Errors, bugs, crashes, software malfunctions
   - Installation and setup problems
   - Configuration and performance issues
   - Troubleshooting and diagnostics
   - Technical "how-to" questions

2. **billing_support_tool** - Billing Support Specialist
   - Payment methods and processing
   - Invoices and charges
   - Subscription management (upgrade, downgrade, cancel)
   - Refund requests and billing disputes
   - Pricing information
   - Account balance and payment errors

3. **compliance_tool** - Compliance Specialist
   - Terms of Service and policies
   - Privacy policy and data collection
   - GDPR, CCPA, and data protection regulations
   - Data deletion, export, and access requests
   - Cookie policy and consent
   - Legal and regulatory questions
   - Account termination policies

4. **general_info_tool** - General Information Specialist
   - Company background and mission
   - Service offerings and features
   - Getting started guides
   - Plan comparisons
   - General "how-to" for basic usage
   - Best practices and tips
   - Navigation and interface help

Routing Decision Matrix:

Route to Technical Support if query mentions:
- Error codes, crashes, bugs, "not working", "broken"
- Installation, setup, configuration
- Performance, slowness, loading issues
- Technical troubleshooting

Route to Billing Support if query mentions:
- Payment, invoice, charge, refund, subscription
- Billing cycle, due date, account balance
- Credit card, payment method
- Price, cost, upgrade, downgrade, cancel plan

Route to Compliance if query mentions:
- Terms of service, privacy policy, legal
- GDPR, CCPA, data protection, data deletion
- Cookies, consent, user rights
- Policies, regulations, compliance

Route to General Information if query mentions:
- "What is...", "Tell me about...", "How does... work"
- Company info, services, features, getting started
- Plan comparison, general pricing overview
- General navigation, basic usage

Handle directly yourself (NO tools needed):
- Greetings: "Hello", "Hi", "Good morning"
- Gratitude: "Thank you", "Thanks", "Appreciate it"
- Feedback: "That helped", "Great service"
- Simple clarifications: "What do you mean?"
- Goodbyes: "Bye", "See you later"

Important Routing Rules:
1. If query clearly fits ONE specialist's domain, route to that tool
2. If query could fit multiple domains, choose the PRIMARY domain:
   - "Refund policy" → Compliance (policy) NOT Billing (execution)
   - "Payment failed error" → Technical Support (error) NOT Billing
   - "How to cancel subscription" → Billing (action) NOT General Info
3. For ambiguous queries, ask clarifying questions before routing
4. Trust specialist responses - pass them directly to the user
5. Don't add unnecessary commentary to specialist responses
6. If unsure, route to the most relevant specialist

Response Guidelines:
- Maintain a friendly, professional, helpful tone
- Be concise but complete
- When using a tool, let the specialist's response speak for itself
- For simple queries, respond directly with warmth and clarity

Remember: You coordinate 4 specialized experts. Your job is intelligent routing, not doing specialized work.
Each specialist is an expert in their domain - trust their responses."""

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
# Phase 4: Register all 4 worker tools
try:
    # Import all worker tools (relative import for backend package structure)
    from agents.workers import (
        technical_support_tool,  # Phase 3
        billing_support_tool,  # Phase 4
        compliance_tool,  # Phase 4
        general_info_tool,  # Phase 4
    )

    # Create supervisor with all 4 specialized worker tools
    tools = [
        technical_support_tool,
        billing_support_tool,
        compliance_tool,
        general_info_tool,
    ]

    supervisor = create_supervisor_agent(tools=tools)
    logger.info(
        f"Supervisor initialized with {len(tools)} worker tools: "
        "technical_support, billing_support, compliance, general_info"
    )
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
