"""
Agents Package

Phase 2: Simple Agent Foundation ✅
- simple_agent.py: Single customer service agent with conversation memory

Phase 3: Multi-Agent Supervisor Architecture ✅
- supervisor_agent.py: Supervisor agent with routing logic
- workers/: Specialized worker agents (Technical, Billing, Policy)
"""

# Phase 2: Simple Agent (for reference/fallback)
from agents.simple_agent import (
    create_customer_service_agent,
    get_agent,
)

# Phase 3: Supervisor Agent (primary for multi-agent routing)
from agents.supervisor_agent import (
    create_supervisor_agent,
    get_supervisor,
)

__all__ = [
    # Phase 2 exports
    "create_customer_service_agent",
    "get_agent",
    # Phase 3 exports
    "create_supervisor_agent",
    "get_supervisor",
]
