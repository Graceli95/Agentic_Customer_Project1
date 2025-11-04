"""
General Information Worker Agent for Multi-Agent System.

This module creates a specialized general information agent that handles
company info, service descriptions, FAQs, and general help. It's called as a tool
by the supervisor agent using the tool-calling pattern.

Phase: 4 - Additional Worker Agents
Phase: 5 - RAG/CAG Integration (Pure RAG strategy)
LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/multi-agent
Last Updated: November 4, 2025
"""

from langchain.agents import create_agent
from langchain.tools import tool
import os
import logging

# Import RAG tool for general documentation search
from agents.tools.rag_tools import general_docs_search

logger = logging.getLogger(__name__)


def create_general_info_agent():
    """
    Create a specialized general information agent.

    This agent is an expert in company information, service offerings, features,
    and general support. It will be wrapped as a tool for the supervisor to call
    when general inquiries are detected.

    The agent:
    - Provides company background and mission
    - Explains service offerings and features
    - Guides new users through getting started
    - Answers "how-to" questions for basic usage
    - Compares different service plans
    - Directs users to appropriate resources
    - Handles general inquiries and FAQs

    Returns:
        Agent: Configured LangChain general information agent

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set

    Example:
        >>> agent = create_general_info_agent()
        >>> result = agent.invoke({
        ...     "messages": [{"role": "user", "content": "What services do you offer?"}]
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

    logger.info("Creating general information worker agent")

    # System prompt: Defines general information specialist role
    system_prompt = """You are a General Information specialist with expertise in company services, features, and general support.

Your role is to:
- Provide information about company background and mission
- Explain service offerings and features in detail
- Guide new users through getting started
- Answer "how-to" questions for basic usage
- Compare different service plans and tiers
- Direct users to appropriate resources and documentation
- Handle general inquiries and frequently asked questions
- Offer helpful tips and best practices
- Use general_docs_search tool to find company and service information

Information Areas You Cover:
- Company background, mission, and values
- Service offerings and product lineup
- Feature descriptions and capabilities
- Getting started guides and onboarding
- Plan comparisons (Free, Basic, Premium, Enterprise)
- Pricing overview (non-detailed billing questions)
- Account setup and profile management
- Best practices and tips for effective use
- Feature tutorials and walkthroughs
- Integration capabilities and partnerships
- Platform availability (web, mobile, desktop)
- System requirements and compatibility
- General navigation and interface help
- Community resources (forums, documentation, tutorials)

Response Guidelines:
- Be friendly, welcoming, and approachable
- Use clear, jargon-free language
- Provide actionable, specific information
- Offer examples and real-world use cases when helpful
- Structure responses with headings and bullet points
- Include relevant links to documentation or resources
- Guide users to next steps naturally
- If question is specialized (technical issue, billing problem, policy matter), 
  acknowledge it and let them know specialized help is available
- Encourage exploration and learning
- Keep responses informative but concise

CRITICAL INSTRUCTION:
- The supervisor agent only sees your FINAL response
- Include ALL relevant information, examples, links, and next steps in your final message
- Don't assume follow-up - make your response complete and self-contained
- If redirecting to specialized help, explain why and what to expect

Example Good Response:
"Great question! Let me explain what services we offer:

**Our Service Offerings:**

1. **Customer Service AI Platform**
   - Multi-agent conversational AI system
   - Intelligent query routing
   - 24/7 automated support
   - Human handoff when needed

2. **Knowledge Base Management**
   - Centralized document repository
   - AI-powered search and retrieval
   - Automatic content updates
   - Multi-language support

3. **Analytics Dashboard**
   - Real-time conversation insights
   - Customer satisfaction tracking
   - Agent performance metrics
   - Custom reporting

**Service Tiers:**

| Feature | Free | Professional | Enterprise |
|---------|------|--------------|------------|
| Conversations/month | 100 | 10,000 | Unlimited |
| Agents | 1 | 5 | Custom |
| Analytics | Basic | Advanced | Full Suite |
| Support | Community | Email | Priority + Phone |

**Getting Started:**
1. Sign up at https://example.com/signup
2. Complete the 5-minute setup wizard
3. Import your knowledge base (optional)
4. Test with our interactive demo
5. Deploy to your website

**Popular Use Cases:**
- E-commerce customer support
- SaaS onboarding and help
- Healthcare appointment scheduling
- Financial services inquiries

**Next Steps:**
- Try our interactive demo: https://example.com/demo
- Watch our getting started video: https://example.com/videos
- Join our community: https://community.example.com

Would you like more details about any specific service or feature?"

Remember: Your response goes directly to the user through the supervisor.
Be helpful, informative, and guide them to success."""

    # Create general information agent using LangChain v1.0 pattern
    agent = create_agent(
        model="openai:gpt-4o-mini",  # Cost-effective model
        tools=[general_docs_search],  # Pure RAG: Search docs on every query
        system_prompt=system_prompt,
        checkpointer=None,  # No memory needed - called as tool, not directly
        name="general_info_agent",  # Required in LangChain v1.0
    )

    logger.info("General information worker agent created successfully")
    return agent


# Initialize agent once at module level for reuse
try:
    general_info_agent = create_general_info_agent()
    logger.info("General information agent initialized and ready")
except ValueError as e:
    logger.error(f"Failed to initialize general information agent: {e}")
    general_info_agent = None


def get_general_info_agent():
    """
    Get the initialized general information agent.

    Returns:
        Agent: The initialized general information agent instance

    Raises:
        RuntimeError: If agent failed to initialize (e.g., missing API key)

    Example:
        >>> agent = get_general_info_agent()
        >>> result = agent.invoke({...})
    """
    if general_info_agent is None:
        raise RuntimeError(
            "General information agent is not initialized. Check that OPENAI_API_KEY is set."
        )
    return general_info_agent


# Tool Wrapper for Supervisor Agent
@tool
def general_info_tool(query: str) -> str:
    """Handle general information questions about company, services, features, and getting started.

    Use this tool when the user has questions about:
    - Company background, mission, or values
    - Service offerings and product descriptions
    - Feature explanations and capabilities
    - Getting started guides and onboarding
    - Plan comparisons (Free, Basic, Premium, Enterprise)
    - General pricing overview (not specific billing issues)
    - Account setup and profile management
    - How-to questions for basic usage
    - Best practices and tips
    - Platform availability and compatibility
    - Navigation and interface help
    - Community resources and documentation
    - General FAQs not covered by other specialists

    Args:
        query: The user's general information question

    Returns:
        str: Complete informative response with examples and next steps

    Example:
        >>> response = general_info_tool("What's the difference between your plans?")
        >>> print(response)
    """
    logger.info(f"General information tool called with query: {query[:50]}...")

    # Get the general info agent
    agent = get_general_info_agent()

    # Invoke the agent with the query
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})

    # Extract the response from the last message
    response = result["messages"][-1].content

    logger.info(f"General information tool returning response: {response[:50]}...")

    return response
