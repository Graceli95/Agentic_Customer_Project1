# Task List: Additional Worker Agents (Phase 4) - COMPRESSED FOR TIGHT DEADLINE ⚡

**Source PRD**: `0004-prd-additional-workers.md`  
**Phase**: Phase 4 - Additional Worker Agents  
**Status**: Ready for Implementation  
**Estimated Time**: 8-10 hours with AI assistance (vs 14-15 in original)

---

## 🚀 OPTIMIZATION STRATEGY

**Time Saved:** 4-5 hours by:
- ✅ Merging tool wrappers into worker creation (saves 3 branch cycles)
- ✅ Batching `__init__.py` exports (saves 2 branch cycles)
- ✅ Skipping supervisor unit tests update (low value add)
- ✅ Batching all documentation into one final task

**Original:** 23 sub-tasks  
**Compressed:** 11 tasks  
**Quality:** Same (all critical tests included)

---

## Relevant Files

### Backend Files
- `backend/agents/workers/billing_support.py` - **NEW**: Billing support worker + tool
- `backend/agents/workers/compliance.py` - **NEW**: Compliance worker + tool
- `backend/agents/workers/general_info.py` - **NEW**: General info worker + tool
- `backend/agents/workers/__init__.py` - **UPDATE**: Export all 3 workers at once
- `backend/agents/supervisor_agent.py` - **UPDATE**: Add 3 new tools, update prompt
- `backend/tests/test_billing_worker.py` - **NEW**: Unit tests for billing worker
- `backend/tests/test_compliance_worker.py` - **NEW**: Unit tests for compliance worker
- `backend/tests/test_general_info_worker.py` - **NEW**: Unit tests for general info worker
- `backend/tests/test_main.py` - **UPDATE**: Add routing tests for all workers

### Documentation Files
- `backend/README.md` - **UPDATE**: Add Phase 4 workers documentation
- `README.md` - **UPDATE**: Update with Phase 4 status and all 4 workers
- `MANUAL_TESTING.md` - **UPDATE**: Add Phase 4 test scenarios for new workers

---

## Tasks (COMPRESSED - 11 TASKS)

### 1.0 Backend: Create All 3 Workers (3 tasks)

- [ ] 1.1 Create `backend/agents/workers/billing_support.py` **with tool wrapper included** (branch: feat/phase4-1.1-billing-worker-and-tool)
  - Create `create_billing_support_agent()` function
  - Use gpt-4o-mini model
  - System prompt: billing/payment expertise (see PRD section 4.1)
  - Use InMemorySaver checkpointer
  - Name: "billing_support_agent"
  - Include module-level singleton pattern
  - Include `get_billing_agent()` getter function
  - **INCLUDE @tool decorator for `billing_support_tool` in same file**
  - Clear tool description for supervisor routing
  - Invoke billing agent with query
  - Extract and return response content
  - Comprehensive logging
  - **MERGED: Tasks 1.1 + 1.2 from original list**

- [ ] 1.2 Create `backend/agents/workers/compliance.py` **with tool wrapper included** (branch: feat/phase4-1.2-compliance-worker-and-tool)
  - Create `create_compliance_agent()` function
  - Use gpt-4o-mini model
  - System prompt: policy/regulatory expertise (see PRD section 4.2)
  - Use InMemorySaver checkpointer
  - Name: "compliance_agent"
  - Include module-level singleton pattern
  - Include `get_compliance_agent()` getter function
  - **INCLUDE @tool decorator for `compliance_tool` in same file**
  - Clear tool description for supervisor routing
  - Invoke compliance agent with query
  - Extract and return response content
  - Comprehensive logging
  - **MERGED: Tasks 2.1 + 2.2 from original list**

- [ ] 1.3 Create `backend/agents/workers/general_info.py` **with tool wrapper included** (branch: feat/phase4-1.3-general-info-worker-and-tool)
  - Create `create_general_info_agent()` function
  - Use gpt-4o-mini model
  - System prompt: company info/FAQ expertise (see PRD section 4.3)
  - Use InMemorySaver checkpointer
  - Name: "general_info_agent"
  - Include module-level singleton pattern
  - Include `get_general_info_agent()` getter function
  - **INCLUDE @tool decorator for `general_info_tool` in same file**
  - Clear tool description for supervisor routing
  - Invoke general info agent with query
  - Extract and return response content
  - Comprehensive logging
  - **MERGED: Tasks 3.1 + 3.2 from original list**

### 2.0 Backend: Export All Workers (1 task - MERGED)

- [ ] 2.1 Update `backend/agents/workers/__init__.py` to export **all 3 workers at once** (branch: feat/phase4-2.1-export-all-workers)
  - Import billing_support_agent, billing_support_tool
  - Import compliance_agent, compliance_tool
  - Import general_info_agent, general_info_tool
  - Add all to `__all__` exports
  - Update docstring
  - **MERGED: Tasks 1.3 + 2.3 + 3.3 from original list**

### 3.0 Backend: Supervisor Integration (1 task)

- [ ] 3.1 Update `backend/agents/supervisor_agent.py` to integrate all 4 workers (branch: feat/phase4-3.1-integrate-all-workers)
  - Import billing_support_tool
  - Import compliance_tool
  - Import general_info_tool
  - Update tools list to include all 4 tools
  - Update system prompt with routing logic for 4 workers (see PRD section 3.3)
  - Define clear domains for each worker
  - Maintain direct handling for simple queries
  - Update logging messages

### 4.0 Backend: Unit Tests for New Workers (3 tasks)

- [ ] 4.1 Create `backend/tests/test_billing_worker.py` (branch: feat/phase4-4.1-billing-worker-tests)
  - Test billing agent creation
  - Test billing agent configuration (model, name, checkpointer)
  - Test billing tool wrapper functionality
  - Test tool invocation with query
  - Test response extraction
  - Test system prompt content
  - Test error handling (missing API key)
  - Test logging behavior
  - Test singleton pattern
  - Target: 15-20 tests
  - All tests must pass
  - Mock OpenAI API calls

- [ ] 4.2 Create `backend/tests/test_compliance_worker.py` (branch: feat/phase4-4.2-compliance-worker-tests)
  - Test compliance agent creation
  - Test compliance agent configuration (model, name, checkpointer)
  - Test compliance tool wrapper functionality
  - Test tool invocation with query
  - Test response extraction
  - Test system prompt content
  - Test error handling (missing API key)
  - Test logging behavior
  - Test singleton pattern
  - Target: 15-20 tests
  - All tests must pass
  - Mock OpenAI API calls

- [ ] 4.3 Create `backend/tests/test_general_info_worker.py` (branch: feat/phase4-4.3-general-info-worker-tests)
  - Test general info agent creation
  - Test general info agent configuration (model, name, checkpointer)
  - Test general info tool wrapper functionality
  - Test tool invocation with query
  - Test response extraction
  - Test system prompt content
  - Test error handling (missing API key)
  - Test logging behavior
  - Test singleton pattern
  - Target: 15-20 tests
  - All tests must pass
  - Mock OpenAI API calls

### 5.0 Backend: Integration Tests for Routing (1 task)

- [ ] 5.1 Update `backend/tests/test_main.py` with routing tests for all workers (branch: feat/phase4-5.1-routing-integration-tests)
  - Test billing query routes to billing worker
  - Test compliance query routes to compliance worker
  - Test general info query routes to general info worker
  - Test technical query still routes correctly (regression)
  - Test mixed conversation with all 4 workers
  - Test context maintenance across different worker types
  - Test ambiguous queries handled appropriately
  - Test supervisor with all 4 tools registered
  - Test edge cases (overlap scenarios)
  - Target: 12-15 new integration tests
  - All tests must pass
  - Mock OpenAI API calls

### 6.0 Documentation: All Docs in One Task (1 task - MERGED)

- [ ] 6.1 Update **all 3 documentation files** (branch: feat/phase4-6.1-update-all-docs)
  
  **File 1: `backend/README.md`**
  - Update "Current Phase" to Phase 4
  - Update Key Features with all 4 workers
  - Update test count and coverage
  - Add section for each new worker:
    * Billing Support Worker details
    * Compliance Worker details
    * General Information Worker details
  - Update routing logic diagram/explanation
  - Update "Adding New Workers" section if needed
  - Update Phase completion status
  - Update examples to show all worker types
  
  **File 2: `README.md`**
  - Update "Current Status" to Phase 4 Complete
  - Update features list with all 4 workers
  - Update test count (80+ tests)
  - Update architecture diagram with all workers
  - Update "Try It Out" section with examples for all workers
  - Update "Next Phases" section
  - Update monorepo structure with Phase 4 files
  - Update completion status
  
  **File 3: `MANUAL_TESTING.md`**
  - Add "Phase 4: All Worker Routing Tests" section
  - Add 5 billing support test scenarios
  - Add 5 compliance test scenarios
  - Add 5 general information test scenarios
  - Add 5 mixed routing test scenarios (all 4 workers)
  - Add Phase 4 troubleshooting section
  - Update test results summary
  - Update next steps
  
  **MERGED: Tasks 8.1 + 9.1 + 10.1 from original list**

---

## ❌ SKIPPED TASKS (From Original List)

### Task 7.1 - Update Supervisor Unit Tests - **SKIPPED**
**Original task:** Update `backend/tests/test_supervisor.py` for 4 workers

**Why skipped:** 
- Existing Phase 3 supervisor tests will still pass
- New workers are tested independently (tasks 4.1-4.3)
- Integration tests verify routing (task 5.1)
- Only adds validation that "supervisor has 4 tools" which is low value
- If anything breaks, other tests will catch it

**Risk:** Low  
**Time saved:** ~30 minutes

---

## Task Workflow (Per Sub-Task)

Following our established Phase 3 workflow:

1. **Create Feature Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/phase4-X.X-description
   ```

2. **Implement Changes**
   - Write code following Phase 3 patterns
   - Add comprehensive logging
   - Include error handling
   - Add type hints
   - Follow LangChain v1.0 best practices

3. **Test Locally**
   ```bash
   # For backend tasks
   cd backend
   pytest  # Run all tests
   pytest tests/test_[specific].py -v  # Run specific tests
   pytest --run-integration  # Include integration tests
   ruff check .  # Check linting
   ruff format .  # Format code
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat(phase4): [description]

   - [change 1]
   - [change 2]
   - [change 3]
   
   Closes #[task number]"
   git push origin feat/phase4-X.X-description
   ```

5. **Merge to Main**
   ```bash
   git checkout main
   git merge feat/phase4-X.X-description
   git push origin main
   ```

6. **Pause for Approval**
   - Wait for user confirmation before proceeding to next task
   - User says "yes", "y", "proceed", or "continue" to move forward

---

## Branch Naming Convention

Follow this pattern for all Phase 4 branches:
```
feat/phase4-[task-number]-[brief-description]
```

Examples:
- `feat/phase4-1.1-billing-worker-and-tool`
- `feat/phase4-2.1-export-all-workers`
- `feat/phase4-3.1-integrate-all-workers`
- `feat/phase4-5.1-routing-integration-tests`

---

## Testing Requirements

### Per Task Testing:
- [ ] All pytest tests pass
- [ ] No Ruff linting errors
- [ ] Pre-commit hooks pass
- [ ] Manual testing if applicable

### Phase 4 Completion Testing:
- [ ] All unit tests passing (80+ tests total)
- [ ] All integration tests passing
- [ ] Test coverage >65%
- [ ] CI/CD pipeline passes
- [ ] Manual test scenarios work
- [ ] All 4 workers respond correctly

### Quality Checks:
- [ ] Code follows Phase 3 patterns and style
- [ ] Proper error handling
- [ ] Comprehensive logging
- [ ] Clear documentation
- [ ] Type hints throughout
- [ ] Descriptive agent names

---

## Estimated Timeline (COMPRESSED)

### With AI Assistance:
- Tasks 1.0: All 3 workers with tools (3-4 hours) ⚡
- Task 2.0: Export all workers (15 min)
- Task 3.0: Supervisor integration (45 min)
- Tasks 4.0: Worker unit tests (2-2.5 hours)
- Task 5.0: Routing integration tests (1 hour)
- Task 6.0: All documentation (1 hour)

**Total: 8-10 hours** (vs 14-15 in original)

**Time saved: 4-5 hours** through efficient batching!

---

## Phase 4 Completion Checklist

Before marking Phase 4 complete:

- [ ] All 11 compressed tasks completed
- [ ] All 3 new workers created and functional
- [ ] Supervisor integrated with all 4 workers
- [ ] All automated tests passing (80+ tests)
- [ ] Test coverage >65%
- [ ] Manual testing scenarios validated
- [ ] Documentation updated (3 files)
- [ ] Code committed and pushed to main
- [ ] CI/CD pipeline green
- [ ] No linter errors
- [ ] All 4 workers routing correctly
- [ ] No domain overlap or confusion
- [ ] Conversation memory maintained
- [ ] Ready for Phase 5 (RAG/CAG integration)

---

## Notes for Implementation

### Key Patterns to Follow:

1. **Worker Creation with Tool (MERGED PATTERN)**:
```python
# At top of file: backend/agents/workers/[worker_name].py
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import logging
import os

logger = logging.getLogger(__name__)

def create_[worker]_agent():
    """Create [domain] worker agent."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")
    
    checkpointer = InMemorySaver()
    
    system_prompt = """You are a [domain] specialist.
    
    CRITICAL: Include ALL details in your final response.
    """
    
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[],
        system_prompt=system_prompt,
        name="[worker]_agent",
    )
    
    logger.info(f"[Worker] agent created successfully")
    return agent

# Module-level singleton
_agent_instance = None

def get_[worker]_agent():
    """Get singleton instance of worker agent."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_[worker]_agent()
    return _agent_instance

# Tool wrapper (MERGED INTO SAME FILE)
@tool
def [worker]_tool(query: str) -> str:
    """Clear description of when to use this tool.
    
    Use for [specific domain queries].
    """
    logger.info(f"[Worker] tool called: {query[:50]}...")
    agent = get_[worker]_agent()
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    response = result["messages"][-1].content
    logger.info(f"[Worker] returning: {response[:50]}...")
    return response
```

2. **Export All Workers (MERGED PATTERN)**:
```python
# backend/agents/workers/__init__.py

# Phase 3: Technical Support Worker
from agents.workers.technical_support import (
    create_technical_support_agent,
    get_technical_agent,
    technical_support_tool,
)

# Phase 4: All 3 new workers (MERGED - all at once)
from agents.workers.billing_support import (
    create_billing_support_agent,
    get_billing_agent,
    billing_support_tool,
)

from agents.workers.compliance import (
    create_compliance_agent,
    get_compliance_agent,
    compliance_tool,
)

from agents.workers.general_info import (
    create_general_info_agent,
    get_general_info_agent,
    general_info_tool,
)

__all__ = [
    # Technical Support (Phase 3)
    "create_technical_support_agent",
    "get_technical_agent",
    "technical_support_tool",
    # Billing Support (Phase 4)
    "create_billing_support_agent",
    "get_billing_agent",
    "billing_support_tool",
    # Compliance (Phase 4)
    "create_compliance_agent",
    "get_compliance_agent",
    "compliance_tool",
    # General Info (Phase 4)
    "create_general_info_agent",
    "get_general_info_agent",
    "general_info_tool",
]
```

3. **Supervisor Tools Update**:
```python
from agents.workers import (
    technical_support_tool,
    billing_support_tool,
    compliance_tool,
    general_info_tool,
)

tools = [
    technical_support_tool,
    billing_support_tool,
    compliance_tool,
    general_info_tool,
]
```

4. **Test Pattern** (same as Phase 3):
```python
@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
@patch("agents.workers.[worker].create_agent")
def test_[worker]_creation(mock_create_agent):
    """Test [worker] agent creation."""
    mock_agent = Mock()
    mock_create_agent.return_value = mock_agent
    
    agent = create_[worker]_agent()
    
    assert agent is not None
    mock_create_agent.assert_called_once()
```

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| New Workers | 3 | billing, compliance, general_info |
| Total Workers | 4 | Including technical support |
| Unit Tests | 60+ new | ~20 per worker |
| Total Tests | 80+ | Phase 3 (54) + Phase 4 (60+) |
| Integration Tests | 15+ new | Routing for all workers |
| Test Coverage | >65% | pytest-cov |
| Routing Accuracy | >85% | Manual testing |
| Documentation | Complete | 3 files updated |
| **Time to Complete** | **8-10 hours** | **vs 14-15 original** |

---

## Domain Boundaries (Critical for Testing)

### Clear Separation:
- **Technical Support**: Errors, bugs, crashes, installation, performance issues
- **Billing Support**: Payments, invoices, subscriptions, refunds, pricing, charges
- **Compliance**: Policies, privacy, legal, terms of service, data deletion, GDPR
- **General Information**: Company info, services, features, FAQs, getting started

### Edge Cases to Test:
- "Refund policy" → Compliance (policy) NOT Billing (execution)
- "Payment failed error" → Could be Technical OR Billing (test both)
- "How to cancel" → Could be General Info OR Billing (needs context)
- "Data export" → Could be Compliance OR Technical (test both)

---

## Phase 4 File Inventory

### New Files (8):
1. `backend/agents/workers/billing_support.py`
2. `backend/agents/workers/compliance.py`
3. `backend/agents/workers/general_info.py`
4. `backend/tests/test_billing_worker.py`
5. `backend/tests/test_compliance_worker.py`
6. `backend/tests/test_general_info_worker.py`
7. `tasks/0004-prd-additional-workers.md`
8. `tasks/tasks-0004-prd-additional-workers-COMPRESSED.md` (this file)

### Modified Files (7):
1. `backend/agents/workers/__init__.py` (1 update - all 3 workers at once)
2. `backend/agents/supervisor_agent.py` (tools + prompt)
3. `backend/tests/test_main.py` (routing tests)
4. `backend/README.md` (all workers)
5. `README.md` (Phase 4 status)
6. `MANUAL_TESTING.md` (new scenarios)
7. ~~`backend/tests/test_supervisor.py`~~ (SKIPPED - not updating)

---

## 🎯 COMPARISON: Compressed vs Original

| Aspect | Original | Compressed | Change |
|--------|----------|------------|--------|
| **Total Tasks** | 23 | 11 | -12 tasks |
| **Worker Creation** | 9 tasks | 3 tasks | Merged tools |
| **Exports** | 3 tasks | 1 task | Batched |
| **Supervisor Tests** | 1 task | 0 tasks | Skipped |
| **Documentation** | 3 tasks | 1 task | Batched |
| **Branch Cycles** | 23 | 11 | -12 cycles |
| **Estimated Time** | 14-15 hours | 8-10 hours | **-4-5 hours** |
| **Test Coverage** | >65% | >65% | Same |
| **Quality** | High | High | Same |

---

**Version**: 1.0.0 (Phase 4 - COMPRESSED)  
**Created**: November 4, 2025  
**Status**: Ready for Implementation  
**Total Tasks**: 11 sub-tasks (compressed from 23)  
**Dependencies**: Phase 3 Complete ✅  
**Time Savings**: 4-5 hours through efficient batching ⚡

