"""
RAG/CAG Tools for Multi-Agent System.

This module provides retrieval tools with different strategies:
- Pure RAG: Technical Support, General Info (dynamic retrieval every query)
- Hybrid RAG/CAG: Billing Support (RAG first time, cache for session)
- Pure CAG: Compliance (static context, no retrieval tool)

Phase: 5 - RAG/CAG Integration
LangChain Version: v1.0+
Last Updated: November 4, 2025
"""

from .rag_tools import (
    technical_docs_search,
    billing_docs_search,
    general_docs_search,
    COMPLIANCE_CONTEXT,
)

__all__ = [
    "technical_docs_search",
    "billing_docs_search",
    "general_docs_search",
    "COMPLIANCE_CONTEXT",
]

