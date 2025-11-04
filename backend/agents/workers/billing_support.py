"""
Billing Support Worker Agent for Multi-Agent System.

This module creates a specialized billing support agent that handles
payment, invoice, subscription, and refund queries. It's called as a tool
by the supervisor agent using the tool-calling pattern.

Phase: 4 - Additional Worker Agents
Phase: 5 - RAG/CAG Integration (Hybrid RAG/CAG strategy)
LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/multi-agent
Last Updated: November 4, 2025
"""

from langchain.agents import create_agent
from langchain.tools import tool
import os
import logging

# Import Hybrid RAG/CAG tool for billing documentation
from agents.tools.rag_tools import billing_docs_search

logger = logging.getLogger(__name__)


def create_billing_support_agent():
    """
    Create a specialized billing support agent.

    This agent is an expert in payment processing, subscriptions, invoices,
    and financial inquiries. It will be wrapped as a tool for the supervisor
    to call when billing-related queries are detected.

    The agent:
    - Assists with payment method updates
    - Helps understand invoices and charges
    - Manages subscription changes
    - Processes refund requests
    - Clarifies pricing and billing cycles
    - Resolves billing errors and disputes

    Returns:
        Agent: Configured LangChain billing support agent

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set

    Example:
        >>> agent = create_billing_support_agent()
        >>> result = agent.invoke({
        ...     "messages": [{"role": "user", "content": "How do I update my payment method?"}]
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

    logger.info("Creating billing support worker agent")

    # System prompt: Defines billing specialist role
    system_prompt = """You are a Billing Support specialist with expertise in payment processing, subscriptions, and financial inquiries.

Your role is to:
- Assist with payment method updates and processing
- Help users understand their invoices and charges
- Manage subscription changes (upgrade, downgrade, cancellation)
- Process refund requests and explain refund policies
- Clarify pricing and billing cycles
- Resolve billing errors and disputes
- Provide account balance information
- Use billing_docs_search tool to find billing policies and pricing information (caches after first use)

Billing Areas You Cover:
- Payment methods (credit cards, PayPal, bank transfers)
- Invoice generation and access
- Subscription management (plans, upgrades, downgrades, cancellations)
- Billing cycles and due dates
- Refund requests and policies
- Pricing information and plan comparisons
- Account balance inquiries
- Payment failed errors and declined transactions
- Duplicate charges and billing disputes
- Tax and VAT questions

Response Guidelines:
- Be empathetic with billing issues and financial concerns
- Explain financial matters clearly and accurately
- Follow company billing policies strictly
- Provide specific amounts, dates, and transaction details when relevant
- Offer alternatives when possible (e.g., payment plans, different billing cycles)
- For refunds, explain the process and timeline clearly
- If you need account-specific information, guide them to proper channels
- Use professional, reassuring tone
- Escalate complex financial issues appropriately
- Never make promises about refunds without policy verification

CRITICAL INSTRUCTION:
- The supervisor agent only sees your FINAL response
- Include ALL billing details, amounts, dates, and next steps in your final message
- Don't assume follow-up - make your response complete and self-contained
- If you need account-specific information, explain how to provide it securely

Example Good Response:
"I understand you were charged twice for your subscription. I'm sorry for the inconvenience. Let me help you resolve this:

**What Happened:**
Duplicate charges can occur if:
1. Payment was retried after initial failure
2. Subscription renewal overlapped with manual payment
3. System processing delay

**Immediate Steps:**
1. **Check your transaction history**
   - Log in to your account → Billing → Transaction History
   - Look for the duplicate charge date and amount

2. **Document the issue**
   - Note both transaction IDs
   - Screenshot the duplicate charges
   - Check your bank/card statement to confirm

3. **Request a refund**
   - Go to Account → Billing → Request Refund
   - Or contact billing@example.com with:
     * Transaction IDs of both charges
     * Date charged
     * Amount of duplicate charge

**Refund Timeline:**
- Refunds are typically processed within 5-7 business days
- Amount will return to your original payment method
- You'll receive confirmation email once processed

**Prevent Future Issues:**
- Ensure only one active payment method
- Set up billing notifications in Account Settings

Is there anything else I can help clarify about your billing?"

Remember: Your response goes directly to the user through the supervisor.
Be thorough, empathetic, and provide complete guidance."""

    # Create billing support agent using LangChain v1.0 pattern
    agent = create_agent(
        model="openai:gpt-4o-mini",  # Cost-effective model
        tools=[billing_docs_search],  # Hybrid RAG/CAG: RAG first time, cache for session
        system_prompt=system_prompt,
        checkpointer=None,  # No memory needed - called as tool, not directly
        name="billing_support_agent",  # Required in LangChain v1.0
    )

    logger.info("Billing support worker agent created successfully")
    return agent


# Initialize agent once at module level for reuse
try:
    billing_agent = create_billing_support_agent()
    logger.info("Billing support agent initialized and ready")
except ValueError as e:
    logger.error(f"Failed to initialize billing support agent: {e}")
    billing_agent = None


def get_billing_agent():
    """
    Get the initialized billing support agent.

    Returns:
        Agent: The initialized billing support agent instance

    Raises:
        RuntimeError: If agent failed to initialize (e.g., missing API key)

    Example:
        >>> agent = get_billing_agent()
        >>> result = agent.invoke({...})
    """
    if billing_agent is None:
        raise RuntimeError(
            "Billing support agent is not initialized. "
            "Check that OPENAI_API_KEY is set."
        )
    return billing_agent


# Tool Wrapper for Supervisor Agent
@tool
def billing_support_tool(query: str) -> str:
    """Handle billing and payment questions including invoices, subscriptions, refunds, and pricing.

    Use this tool when the user has questions about:
    - Payment methods (updating, adding, removing credit cards, PayPal, etc.)
    - Invoices (viewing, downloading, understanding charges)
    - Subscriptions (upgrading, downgrading, canceling, plan changes)
    - Billing cycles and due dates
    - Refund requests and refund policy
    - Pricing information and plan comparisons
    - Account balance inquiries
    - Payment errors (declined, failed, duplicate charges)
    - Billing disputes and incorrect charges
    - Tax and VAT questions

    Args:
        query: The user's billing or payment question

    Returns:
        str: Complete billing support response with clear guidance and next steps

    Example:
        >>> response = billing_support_tool("I was charged twice this month")
        >>> print(response)
    """
    logger.info(f"Billing support tool called with query: {query[:50]}...")

    # Get the billing agent
    agent = get_billing_agent()

    # Invoke the agent with the query
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})

    # Extract the response from the last message
    response = result["messages"][-1].content

    logger.info(f"Billing support tool returning response: {response[:50]}...")

    return response
