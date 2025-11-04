"""
RAG/CAG Tools with Strategy-Specific Implementations.

This module implements three different retrieval strategies:
1. Pure RAG (Technical, General): Search vector store on every query
2. Hybrid RAG/CAG (Billing): RAG first time, cache results for session
3. Pure CAG (Compliance): Load static documents at module level

Phase: 5 - RAG/CAG Integration
LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/retrieval
Last Updated: November 4, 2025
"""

import logging
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command

from data.vectorstore import get_vectorstore
from data.document_loader import load_single_document

# Load environment variables (with override for cached env vars)
load_dotenv(override=True)

logger = logging.getLogger(__name__)

# ============================================================================
# Strategy 1: Pure RAG (Technical Support, General Info)
# ============================================================================
# Dynamic retrieval: Search vector store on EVERY query
# Use case: Frequently updated knowledge (bugs, features, documentation)
# ============================================================================


@tool
def technical_docs_search(query: str) -> str:
    """Search technical documentation for troubleshooting, error codes, and solutions.
    
    Use this tool when users have:
    - Error messages or codes
    - Software crashes or bugs
    - Installation or configuration issues
    - Performance problems
    - Technical "how-to" questions
    
    Strategy: Pure RAG - searches vector store every query for latest information.
    
    Args:
        query: The user's technical support question
        
    Returns:
        Relevant technical documentation with sources
        
    Example:
        >>> response = technical_docs_search("Error 500 internal server error")
        >>> print(response)
    """
    logger.info(f"[PURE RAG] Technical docs search: {query[:50]}...")
    
    try:
        # Get technical vector store
        vectorstore = get_vectorstore("technical")
        
        if vectorstore is None:
            logger.error("Technical vector store not available")
            return "Technical documentation is currently unavailable. Please try again later."
        
        # Search vector store (Pure RAG - always retrieves fresh)
        docs = vectorstore.similarity_search(query, k=3)
        
        if not docs:
            logger.warning(f"No technical docs found for query: {query[:50]}...")
            return "I couldn't find specific documentation for that issue. Could you provide more details about the error or problem you're experiencing?"
        
        # Format results with metadata
        formatted_results = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            # Extract filename from path
            source_file = Path(source).name if source != "Unknown" else "Unknown"
            
            formatted_results.append(
                f"**Source {i}: {source_file}**\n{doc.page_content}\n"
            )
        
        response = "\n\n".join(formatted_results)
        logger.info(f"[PURE RAG] Technical docs: Retrieved {len(docs)} documents")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in technical_docs_search: {e}", exc_info=True)
        return "An error occurred while searching technical documentation. Please try rephrasing your question."


@tool
def general_docs_search(query: str) -> str:
    """Search general information about company, services, features, and getting started.
    
    Use this tool when users ask about:
    - Company background and mission
    - Service offerings and features
    - Getting started guides
    - Plan comparisons and features
    - General product information
    - Platform capabilities
    
    Strategy: Pure RAG - searches vector store every query for latest information.
    
    Args:
        query: The user's general information question
        
    Returns:
        Relevant company/service information with sources
        
    Example:
        >>> response = general_docs_search("What services do you offer?")
        >>> print(response)
    """
    logger.info(f"[PURE RAG] General docs search: {query[:50]}...")
    
    try:
        # Get general vector store
        vectorstore = get_vectorstore("general")
        
        if vectorstore is None:
            logger.error("General vector store not available")
            return "General information is currently unavailable. Please try again later."
        
        # Search vector store (Pure RAG - always retrieves fresh)
        docs = vectorstore.similarity_search(query, k=3)
        
        if not docs:
            logger.warning(f"No general docs found for query: {query[:50]}...")
            return "I couldn't find specific information about that. Could you rephrase your question or ask about something more specific?"
        
        # Format results with metadata
        formatted_results = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            # Extract filename from path
            source_file = Path(source).name if source != "Unknown" else "Unknown"
            
            formatted_results.append(
                f"**Source {i}: {source_file}**\n{doc.page_content}\n"
            )
        
        response = "\n\n".join(formatted_results)
        logger.info(f"[PURE RAG] General docs: Retrieved {len(docs)} documents")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in general_docs_search: {e}", exc_info=True)
        return "An error occurred while searching for information. Please try again."


# ============================================================================
# Strategy 2: Hybrid RAG/CAG (Billing Support)
# ============================================================================
# First query: RAG (retrieve from vector store)
# Subsequent queries: CAG (use cached results from state)
# Use case: Static policies that rarely change, high query volume
# ============================================================================


@tool
def billing_docs_search(
    query: str,
    runtime: Annotated[ToolRuntime, "Runtime context with state access"]
) -> Command:
    """Search billing policies, pricing, refunds, and subscription information.
    
    Use this tool when users ask about:
    - Payment methods and processing
    - Invoices and charges
    - Subscription management (upgrade, downgrade, cancel)
    - Refund requests and policies
    - Pricing information and plans
    - Billing errors or disputes
    
    Strategy: Hybrid RAG/CAG - retrieves policies on first query, caches for session.
    This improves performance since billing policies rarely change within a conversation.
    
    Args:
        query: The user's billing question
        runtime: Tool runtime context with state access
        
    Returns:
        Command with billing information and cached state
        
    Example:
        >>> response = billing_docs_search("What's your refund policy?", runtime)
        >>> print(response.result)
    """
    logger.info(f"[HYBRID RAG/CAG] Billing docs search: {query[:50]}...")
    
    try:
        # Check if we already have cached billing policies (CAG)
        cached_policies = runtime.state.get("billing_policies")
        
        if cached_policies:
            logger.info("[HYBRID RAG/CAG] Using cached billing policies (CAG)")
            return Command(
                result=cached_policies
            )
        
        # First time: Retrieve from vector store (RAG)
        logger.info("[HYBRID RAG/CAG] First query - retrieving from vector store (RAG)")
        vectorstore = get_vectorstore("billing")
        
        if vectorstore is None:
            logger.error("Billing vector store not available")
            return Command(
                result="Billing information is currently unavailable. Please try again later."
            )
        
        # Search vector store
        docs = vectorstore.similarity_search(query, k=3)
        
        if not docs:
            logger.warning(f"No billing docs found for query: {query[:50]}...")
            return Command(
                result="I couldn't find specific billing information for that question. Could you provide more details?"
            )
        
        # Format results with metadata
        formatted_results = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            source_file = Path(source).name if source != "Unknown" else "Unknown"
            
            formatted_results.append(
                f"**Source {i}: {source_file}**\n{doc.page_content}\n"
            )
        
        response = "\n\n".join(formatted_results)
        logger.info(f"[HYBRID RAG/CAG] Retrieved {len(docs)} docs, caching for session")
        
        # Cache the policies for this session (CAG for subsequent queries)
        return Command(
            update={"billing_policies": response},
            result=response
        )
        
    except Exception as e:
        logger.error(f"Error in billing_docs_search: {e}", exc_info=True)
        return Command(
            result="An error occurred while searching billing information. Please try again."
        )


# ============================================================================
# Strategy 3: Pure CAG (Compliance)
# ============================================================================
# Load ALL compliance documents at module level (once)
# No retrieval tool - context injected directly into system prompt
# Use case: Fixed legal documents that must be consistent
# ============================================================================


def load_compliance_context() -> str:
    """
    Load all compliance documents at module startup (Pure CAG).
    
    This is called ONCE when the module is imported, not per query.
    Compliance documents (ToS, Privacy Policy) are static and rarely change,
    so we load them into memory for fast, consistent access.
    
    Returns:
        Combined compliance documentation as string
    """
    logger.info("[PURE CAG] Loading compliance documents at module startup...")
    
    try:
        docs_dir = Path(__file__).parent.parent.parent / "data" / "docs" / "compliance"
        
        # Load privacy policy
        privacy_path = docs_dir / "privacy-policy.md"
        privacy_content = load_single_document(privacy_path)
        
        # Load terms of service
        terms_path = docs_dir / "terms-of-service.md"
        terms_content = load_single_document(terms_path)
        
        if not privacy_content or not terms_content:
            logger.error("[PURE CAG] Failed to load compliance documents")
            return "Compliance documents could not be loaded."
        
        # Combine into single context
        context = f"""# PRIVACY POLICY

{privacy_content}

---

# TERMS OF SERVICE

{terms_content}"""
        
        logger.info(f"[PURE CAG] Loaded compliance context: {len(context)} characters")
        return context
        
    except Exception as e:
        logger.error(f"[PURE CAG] Error loading compliance context: {e}", exc_info=True)
        return "Compliance documents could not be loaded."


# Load compliance context ONCE at module level (Pure CAG)
COMPLIANCE_CONTEXT = load_compliance_context()

# Note: Compliance worker does NOT have a search tool
# It uses COMPLIANCE_CONTEXT directly in its system prompt
# This ensures consistent, fast responses without retrieval overhead

