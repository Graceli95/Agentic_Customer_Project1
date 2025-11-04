"""
Worker Agents Package

Specialized agents for different domains:

Phase 3: ✅
- technical_support.py: Technical support worker

Phase 4: ✅
- billing_support.py: Billing and payment support worker
- compliance.py: Policy, privacy, and regulatory compliance worker
- general_info.py: Company info, services, and general help worker

Future (Phase 5+):
- RAG/CAG integration for all workers with document retrieval
"""

# Phase 3: Technical Support Worker
from agents.workers.technical_support import (
    create_technical_support_agent,
    get_technical_agent,
    technical_support_tool,
)

# Phase 4: Billing Support Worker
from agents.workers.billing_support import (
    create_billing_support_agent,
    get_billing_agent,
    billing_support_tool,
)

# Phase 4: Compliance Worker
from agents.workers.compliance import (
    create_compliance_agent,
    get_compliance_agent,
    compliance_tool,
)

# Phase 4: General Information Worker
from agents.workers.general_info import (
    create_general_info_agent,
    get_general_info_agent,
    general_info_tool,
)

__all__ = [
    # Technical Support Worker (Phase 3)
    "create_technical_support_agent",
    "get_technical_agent",
    "technical_support_tool",
    # Billing Support Worker (Phase 4)
    "create_billing_support_agent",
    "get_billing_agent",
    "billing_support_tool",
    # Compliance Worker (Phase 4)
    "create_compliance_agent",
    "get_compliance_agent",
    "compliance_tool",
    # General Information Worker (Phase 4)
    "create_general_info_agent",
    "get_general_info_agent",
    "general_info_tool",
]
