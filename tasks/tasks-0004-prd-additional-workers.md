# Task List: Additional Worker Agents (Phase 4)

**Source PRD**: `0004-prd-additional-workers.md`  
**Phase**: Phase 4 - Additional Worker Agents  
**Status**: Ready for Implementation  
**Estimated Time**: 8-12 hours with AI assistance

---

## Relevant Files

### Backend Files
- `backend/agents/workers/billing_support.py` - **NEW**: Billing support worker agent
- `backend/agents/workers/compliance.py` - **NEW**: Compliance worker agent
- `backend/agents/workers/general_info.py` - **NEW**: General information worker agent
- `backend/agents/workers/__init__.py` - **UPDATE**: Export new workers and tools
- `backend/agents/supervisor_agent.py` - **UPDATE**: Add 3 new tools, update prompt
- `backend/tests/test_billing_worker.py` - **NEW**: Unit tests for billing worker
- `backend/tests/test_compliance_worker.py` - **NEW**: Unit tests for compliance worker
- `backend/tests/test_general_info_worker.py` - **NEW**: Unit tests for general info worker
- `backend/tests/test_supervisor.py` - **UPDATE**: Test with 4 workers
- `backend/tests/test_main.py` - **UPDATE**: Add routing tests for all workers

### Documentation Files
- `backend/README.md` - **UPDATE**: Add Phase 4 workers documentation
- `README.md` - **UPDATE**: Update with Phase 4 status and all 4 workers
- `MANUAL_TESTING.md` - **UPDATE**: Add Phase 4 test scenarios for new workers

### Notes
- Follow Phase 3 workflow: feature branch → implement → test → commit → push → merge → pause
- Each worker follows same pattern as technical_support.py
- All workers use gpt-4o-mini model
- Maintain same testing standards (pytest for backend)
- Keep same code quality (Ruff, pre-commit hooks)
- Follow LangChain v1.0 patterns from Phase 3

---

## Tasks

### 1.0 Backend: Billing Support Worker
- [ ] 1.1 Create `backend/agents/workers/billing_support.py` with billing agent (branch: feat/phase4-1.1-create-billing-worker)
  - Create `create_billing_support_agent()` function
  - Use gpt-4o-mini model
  - System prompt: billing/payment expertise
  - Use InMemorySaver checkpointer
  - Name: "billing_support_agent"
  - Include module-level singleton pattern
  - Include `get_billing_agent()` getter function
  - Comprehensive logging

- [ ] 1.2 Wrap billing worker as tool for supervisor (branch: feat/phase4-1.2-wrap-billing-tool)
  - Add `@tool` decorator for `billing_support_tool`
  - Clear tool description for supervisor routing
  - Invoke billing agent with query
  - Extract and return response content
  - Logging for tool calls

- [ ] 1.3 Update `backend/agents/workers/__init__.py` to export billing worker (branch: feat/phase4-1.3-export-billing-worker)
  - Import billing agent and tool
  - Add to `__all__` exports
  - Update docstring

### 2.0 Backend: Compliance Worker
- [ ] 2.1 Create `backend/agents/workers/compliance.py` with compliance agent (branch: feat/phase4-2.1-create-compliance-worker)
  - Create `create_compliance_agent()` function
  - Use gpt-4o-mini model
  - System prompt: policy/regulatory expertise
  - Use InMemorySaver checkpointer
  - Name: "compliance_agent"
  - Include module-level singleton pattern
  - Include `get_compliance_agent()` getter function
  - Comprehensive logging

- [ ] 2.2 Wrap compliance worker as tool for supervisor (branch: feat/phase4-2.2-wrap-compliance-tool)
  - Add `@tool` decorator for `compliance_tool`
  - Clear tool description for supervisor routing
  - Invoke compliance agent with query
  - Extract and return response content
  - Logging for tool calls

- [ ] 2.3 Update `backend/agents/workers/__init__.py` to export compliance worker (branch: feat/phase4-2.3-export-compliance-worker)
  - Import compliance agent and tool
  - Add to `__all__` exports
  - Update docstring

### 3.0 Backend: General Information Worker
- [ ] 3.1 Create `backend/agents/workers/general_info.py` with general info agent (branch: feat/phase4-3.1-create-general-info-worker)
  - Create `create_general_info_agent()` function
  - Use gpt-4o-mini model
  - System prompt: company info/FAQ expertise
  - Use InMemorySaver checkpointer
  - Name: "general_info_agent"
  - Include module-level singleton pattern
  - Include `get_general_info_agent()` getter function
  - Comprehensive logging

- [ ] 3.2 Wrap general info worker as tool for supervisor (branch: feat/phase4-3.2-wrap-general-info-tool)
  - Add `@tool` decorator for `general_info_tool`
  - Clear tool description for supervisor routing
  - Invoke general info agent with query
  - Extract and return response content
  - Logging for tool calls

- [ ] 3.3 Update `backend/agents/workers/__init__.py` to export general info worker (branch: feat/phase4-3.3-export-general-info-worker)
  - Import general info agent and tool
  - Add to `__all__` exports
  - Update docstring

### 4.0 Backend: Supervisor Integration
- [ ] 4.1 Update `backend/agents/supervisor_agent.py` to integrate all 4 workers (branch: feat/phase4-4.1-integrate-all-workers)
  - Import billing_support_tool
  - Import compliance_tool
  - Import general_info_tool
  - Update tools list to include all 4 tools
  - Update system prompt with routing logic for 4 workers
  - Define clear domains for each worker
  - Maintain direct handling for simple queries
  - Update logging messages

### 5.0 Backend: Unit Tests for New Workers
- [ ] 5.1 Create `backend/tests/test_billing_worker.py` (branch: feat/phase4-5.1-billing-worker-tests)
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

- [ ] 5.2 Create `backend/tests/test_compliance_worker.py` (branch: feat/phase4-5.2-compliance-worker-tests)
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

- [ ] 5.3 Create `backend/tests/test_general_info_worker.py` (branch: feat/phase4-5.3-general-info-worker-tests)
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

### 6.0 Backend: Integration Tests for Routing
- [ ] 6.1 Update `backend/tests/test_main.py` with routing tests for all workers (branch: feat/phase4-6.1-routing-integration-tests)
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

### 7.0 Backend: Supervisor Unit Tests Update
- [ ] 7.1 Update `backend/tests/test_supervisor.py` for 4 workers (branch: feat/phase4-7.1-update-supervisor-tests)
  - Test supervisor has 4 tools registered
  - Test supervisor system prompt mentions all workers
  - Test supervisor configuration with all tools
  - Update existing tests if needed
  - Add 3-5 new tests for Phase 4 changes
  - All tests must pass

### 8.0 Documentation: Backend README
- [ ] 8.1 Update `backend/README.md` with Phase 4 workers (branch: feat/phase4-8.1-update-backend-readme)
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

### 9.0 Documentation: Root README
- [ ] 9.1 Update root `README.md` with Phase 4 status (branch: feat/phase4-9.1-update-root-readme)
  - Update "Current Status" to Phase 4 Complete
  - Update features list with all 4 workers
  - Update test count (80+ tests)
  - Update architecture diagram with all workers
  - Update "Try It Out" section with examples for all workers
  - Update "Next Phases" section
  - Update monorepo structure with Phase 4 files
  - Update completion status

### 10.0 Documentation: Manual Testing Guide
- [ ] 10.1 Update `MANUAL_TESTING.md` with Phase 4 scenarios (branch: feat/phase4-10.1-update-manual-testing)
  - Add "Phase 4: All Worker Routing Tests" section
  - Add 5 billing support test scenarios
  - Add 5 compliance test scenarios
  - Add 5 general information test scenarios
  - Add 5 mixed routing test scenarios (all 4 workers)
  - Add Phase 4 troubleshooting section
  - Update test results summary
  - Update next steps

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
- `feat/phase4-1.1-create-billing-worker`
- `feat/phase4-1.2-wrap-billing-tool`
- `feat/phase4-4.1-integrate-all-workers`
- `feat/phase4-6.1-routing-integration-tests`

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

## Estimated Timeline

### With AI Assistance (Optimistic):
- Tasks 1.0: Billing worker (2 hours)
- Tasks 2.0: Compliance worker (2 hours)
- Tasks 3.0: General info worker (2 hours)
- Tasks 4.0: Supervisor integration (1 hour)
- Tasks 5.0: Worker unit tests (2 hours)
- Tasks 6.0: Routing integration tests (1 hour)
- Tasks 7.0: Supervisor tests update (0.5 hour)
- Tasks 8.0-10.0: Documentation (1.5 hours)

**Total: 12 hours**

### With Buffer (Realistic):
- Add 2-3 hours for debugging and iteration
- **Total: 14-15 hours (1.5-2 days)**

---

## Phase 4 Completion Checklist

Before marking Phase 4 complete:

- [ ] All 23 sub-tasks completed
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

1. **Worker Creation** (same as Phase 3):
```python
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
    
    return agent
```

2. **Tool Wrapping** (same as Phase 3):
```python
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

### New Files (7):
1. `backend/agents/workers/billing_support.py`
2. `backend/agents/workers/compliance.py`
3. `backend/agents/workers/general_info.py`
4. `backend/tests/test_billing_worker.py`
5. `backend/tests/test_compliance_worker.py`
6. `backend/tests/test_general_info_worker.py`
7. `tasks/0004-prd-additional-workers.md`

### Modified Files (6):
1. `backend/agents/workers/__init__.py` (3 updates)
2. `backend/agents/supervisor_agent.py` (tools + prompt)
3. `backend/tests/test_supervisor.py` (4 tools)
4. `backend/tests/test_main.py` (routing tests)
5. `backend/README.md` (all workers)
6. `README.md` (Phase 4 status)
7. `MANUAL_TESTING.md` (new scenarios)

---

**Version**: 1.0.0 (Phase 4)  
**Created**: November 4, 2025  
**Status**: Ready for Implementation  
**Total Tasks**: 23 sub-tasks across 10 categories  
**Dependencies**: Phase 3 Complete ✅

