"""
Agents Package

Phase 2: Simple Agent Foundation
- simple_agent.py: Single customer service agent with conversation memory

Future (Phase 3+):
- orchestrator.py: Main agent coordinator and supervisor
- workers/: Specialized worker agents (Technical, Billing, Policy)
"""

from agents.simple_agent import (
    create_customer_service_agent,
    get_agent,
)

__all__ = [
    "create_customer_service_agent",
    "get_agent",
]
