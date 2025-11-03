"""
Worker Agents Package

Specialized agents for different domains:

Phase 3: ✅
- technical_support.py: Technical support worker (will add RAG in Phase 5)

Future (Phase 4+):
- billing_support.py: Hybrid RAG/CAG for billing queries
- policy_compliance.py: Pure CAG for policy queries
"""

# Phase 3: Technical Support Worker
from agents.workers.technical_support import (
    create_technical_support_agent,
    get_technical_agent,
    technical_support_tool,
)

__all__ = [
    # Technical Support Worker (Phase 3)
    "create_technical_support_agent",
    "get_technical_agent",
    "technical_support_tool",  # Primary export for supervisor
]
