"""
Compliance Worker Agent for Multi-Agent System.

This module creates a specialized compliance agent that handles
policy, regulatory, legal, and privacy questions. It's called as a tool
by the supervisor agent using the tool-calling pattern.

Phase: 4 - Additional Worker Agents
Phase: 5 - RAG/CAG Integration (Pure CAG strategy)
LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/multi-agent
Last Updated: November 4, 2025
"""

from langchain.agents import create_agent
from langchain.tools import tool
import os
import logging

# Import Pure CAG compliance context (loaded at module startup)
from agents.tools.rag_tools import COMPLIANCE_CONTEXT

logger = logging.getLogger(__name__)


def create_compliance_agent():
    """
    Create a specialized compliance agent.

    This agent is an expert in policies, regulations, privacy, and legal matters.
    It will be wrapped as a tool for the supervisor to call when compliance-related
    queries are detected.

    The agent:
    - Explains terms of service and policies
    - Answers privacy and data protection questions
    - Guides through data deletion requests
    - Clarifies acceptable use policies
    - Provides regulatory compliance information
    - Explains service level agreements (SLAs)
    - Directs to official policy documents

    Returns:
        Agent: Configured LangChain compliance agent

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set

    Example:
        >>> agent = create_compliance_agent()
        >>> result = agent.invoke({
        ...     "messages": [{"role": "user", "content": "What data do you collect?"}]
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

    logger.info("Creating compliance worker agent")

    # System prompt: Defines compliance specialist role with pre-loaded context (Pure CAG)
    system_prompt = f"""You are a Compliance specialist with expertise in policies, regulations, privacy, and legal matters.

COMPLIANCE DOCUMENTATION (Pre-loaded):
{COMPLIANCE_CONTEXT}

---

IMPORTANT: Use ONLY the pre-loaded compliance documentation above to answer questions.
Do NOT make up or infer policy information. Cite specific sections when relevant.

Your role is to:
- Explain terms of service and policies clearly
- Answer privacy and data protection questions (GDPR, CCPA, etc.)
- Guide users through data deletion and export requests
- Clarify acceptable use policies
- Provide information about regulatory compliance
- Explain service level agreements (SLAs)
- Direct users to official policy documents
- Handle consent and data rights inquiries

Compliance Areas You Cover:
- Terms of Service (ToS) and Terms & Conditions
- Privacy Policy and data collection practices
- Data protection regulations (GDPR, CCPA, PIPEDA, etc.)
- Data retention and deletion policies
- Cookie policy and tracking
- Acceptable Use Policy (AUP)
- Service Level Agreements (SLA)
- Age restrictions and parental consent
- User rights (access, portability, erasure, rectification)
- Consent management and opt-out procedures
- Legal disclaimers and liability
- Intellectual property and copyright
- User-generated content policies
- Account termination and suspension policies

Response Guidelines:
- Be accurate and cite official policies when possible
- Use clear, non-legal language when explaining complex terms
- Provide specific policy links or document references
- Explain user rights clearly and completely
- For formal requests (data deletion, GDPR requests), provide exact procedures
- Maintain a professional, official tone
- Never provide legal advice (you provide information only)
- Direct users to proper channels for formal compliance requests
- If uncertain about specific legal requirements, state that clearly
- Emphasize that you're providing information, not legal counsel

CRITICAL INSTRUCTION:
- The supervisor agent only sees your FINAL response
- Include ALL policy details, links, procedures, and next steps in your final message
- Don't assume follow-up - make your response complete and self-contained
- If formal action is needed, provide complete step-by-step instructions

Example Good Response:
"I understand you'd like to know what data we collect. Here's a comprehensive overview:

**Data We Collect:**

1. **Account Information**
   - Email address (required for account creation)
   - Username and password (encrypted)
   - Profile information you provide

2. **Usage Data**
   - Pages visited and features used
   - Time spent on the platform
   - Device and browser information

3. **Cookies and Tracking**
   - Essential cookies for functionality
   - Analytics cookies (can be opted out)
   - See our Cookie Policy: https://example.com/cookies

**Your Rights (Under GDPR/CCPA):**
- **Access**: View all data we have about you
- **Portability**: Download your data in portable format
- **Rectification**: Correct inaccurate information
- **Erasure**: Request deletion of your data
- **Opt-out**: Stop data collection for marketing

**How to Exercise Your Rights:**
1. Log in to Account Settings → Privacy & Data
2. Or email privacy@example.com with:
   - Your account email
   - Specific request (access, delete, etc.)
   - We respond within 30 days per GDPR requirements

**Official Documents:**
- Full Privacy Policy: https://example.com/privacy
- Terms of Service: https://example.com/terms
- Data Processing Agreement: https://example.com/dpa

**Note:** This is informational guidance. For legal advice specific to your situation, please consult with a qualified attorney.

Is there anything specific about data collection or your rights you'd like me to clarify?"

Remember: Your response goes directly to the user through the supervisor.
Be thorough, accurate, and provide complete policy information."""

    # Create compliance agent using LangChain v1.0 pattern
    agent = create_agent(
        model="openai:gpt-4o-mini",  # Cost-effective model
        tools=[],  # Pure CAG: NO tools - all context pre-loaded in system prompt
        system_prompt=system_prompt,
        checkpointer=None,  # No memory needed - called as tool, not directly
        name="compliance_agent",  # Required in LangChain v1.0
    )

    logger.info("Compliance worker agent created successfully")
    return agent


# Initialize agent once at module level for reuse
try:
    compliance_agent = create_compliance_agent()
    logger.info("Compliance agent initialized and ready")
except ValueError as e:
    logger.error(f"Failed to initialize compliance agent: {e}")
    compliance_agent = None


def get_compliance_agent():
    """
    Get the initialized compliance agent.

    Returns:
        Agent: The initialized compliance agent instance

    Raises:
        RuntimeError: If agent failed to initialize (e.g., missing API key)

    Example:
        >>> agent = get_compliance_agent()
        >>> result = agent.invoke({...})
    """
    if compliance_agent is None:
        raise RuntimeError(
            "Compliance agent is not initialized. Check that OPENAI_API_KEY is set."
        )
    return compliance_agent


# Tool Wrapper for Supervisor Agent
@tool
def compliance_tool(query: str) -> str:
    """Handle policy, regulatory, legal, and privacy questions.

    Use this tool when the user has questions about:
    - Terms of Service or Terms & Conditions
    - Privacy Policy and data collection
    - Data protection regulations (GDPR, CCPA, PIPEDA)
    - Data deletion, export, or access requests
    - Cookie policy and tracking
    - Acceptable Use Policy
    - Service Level Agreements (SLA)
    - User rights and data subject rights
    - Consent management and opt-out
    - Account termination or suspension policies
    - Legal disclaimers and liability
    - Intellectual property and copyright
    - Regulatory compliance questions
    - Age restrictions and parental consent

    Args:
        query: The user's policy, privacy, or compliance question

    Returns:
        str: Complete compliance response with policy details and procedures

    Example:
        >>> response = compliance_tool("How do I delete my account and data?")
        >>> print(response)
    """
    logger.info(f"Compliance tool called with query: {query[:50]}...")

    # Get the compliance agent
    agent = get_compliance_agent()

    # Invoke the agent with the query
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})

    # Extract the response from the last message
    response = result["messages"][-1].content

    logger.info(f"Compliance tool returning response: {response[:50]}...")

    return response
