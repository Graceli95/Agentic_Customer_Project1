# PRD: Multi-Agent Supervisor Architecture (Phase 3)

**Phase**: 3 of 6  
**Status**: Ready for Implementation  
**Priority**: High  
**Estimated Effort**: 3-4 days (with AI assistance: 1 day)  
**Dependencies**: Phase 2 (Simple Agent Foundation) ✅

---

## 1. Overview

### 1.1 Goals

Implement a multi-agent architecture using the **supervisor pattern** where a main coordinator agent intelligently routes user queries to specialized worker agents. This phase establishes the foundation for the full multi-agent system by creating the supervisor and converting the Phase 2 simple agent into the first specialized worker.

### 1.2 Objectives

- ✅ Create a supervisor agent that analyzes queries and routes appropriately
- ✅ Convert Phase 2's simple agent into a specialized Technical Support worker
- ✅ Implement tool-calling pattern per LangChain v1.0 best practices
- ✅ Maintain conversation memory across agent routing
- ✅ Establish clear routing logic and fallback handling
- ✅ Test routing decisions with diverse query types

### 1.3 Success Metrics

- Supervisor correctly identifies technical vs general queries (>90% accuracy)
- Technical Support worker provides relevant responses when routed
- Conversation context is maintained across multiple turns
- Fallback handling works for ambiguous/general queries
- All automated tests pass (target: 45+ tests, >70% coverage)
- Manual testing scenarios all pass

---

## 2. Technical Architecture

### 2.1 System Design

**Current Architecture (Phase 2):**
```
User → Backend → Simple Agent → Response
```

**New Architecture (Phase 3):**
```
User → Backend → Supervisor Agent → [Technical Support Tool] → Response
                                  ↘ (or handle directly if general)
```

### 2.2 Components

#### 2.2.1 Supervisor Agent
- **Purpose**: Analyze queries and route to appropriate worker or handle directly
- **Model**: `openai:gpt-4o-mini`
- **Tools**: `[technical_support_tool]`
- **Memory**: Shared `InMemorySaver` checkpointer
- **System Prompt**: Guides routing decisions and fallback handling

#### 2.2.2 Technical Support Worker
- **Purpose**: Handle technical questions, errors, bugs, and troubleshooting
- **Model**: `openai:gpt-4o-mini`
- **Tools**: `[]` (RAG will be added in Phase 5)
- **Wrapped As**: `@tool` decorator for supervisor to call
- **System Prompt**: Emphasizes technical expertise and complete responses

#### 2.2.3 Tool Integration
- Technical worker wrapped as `technical_support_tool`
- Tool description guides supervisor's routing decisions
- Tool returns complete response (not partial)
- Supervisor formats final response to user

### 2.3 Conversation Flow

```
1. User sends message with session_id
2. Backend receives via /chat endpoint
3. Supervisor agent invoked with user message
4. Supervisor analyzes query intent:
   a. Technical issue? → Call technical_support_tool
   b. General/greeting? → Handle directly
5. If tool called:
   a. Technical worker receives query
   b. Worker generates response
   c. Worker returns to supervisor
6. Supervisor formats final response
7. Response sent to user
8. Conversation saved to memory
```

### 2.4 Routing Strategy

**Technical Queries (Route to Technical Support):**
- Error messages or codes
- Software bugs or crashes
- Installation or setup issues
- Feature troubleshooting
- Technical configuration
- Performance problems

**General Queries (Supervisor Handles):**
- Greetings ("Hello", "Hi")
- Gratitude ("Thank you")
- General questions about the service
- Clarification requests
- Ambiguous queries

---

## 3. Implementation Details

### 3.1 File Structure

```
backend/
├── agents/
│   ├── __init__.py              # Update: Export supervisor and workers
│   ├── supervisor_agent.py      # NEW: Supervisor with routing logic
│   ├── workers/
│   │   ├── __init__.py          # Update: Export workers
│   │   └── technical_support.py # NEW: Technical support worker
│   └── simple_agent.py          # KEEP: For reference (Phase 2)
├── main.py                       # Update: Use supervisor instead of simple agent
└── tests/
    ├── test_supervisor.py        # NEW: Supervisor tests
    └── test_technical_worker.py  # NEW: Worker tests
```

### 3.2 Key Code Patterns

#### Supervisor Agent Creation
```python
from langchain.agents import create_agent

supervisor = create_agent(
    model="openai:gpt-4o-mini",
    tools=[technical_support_tool],  # List of worker tools
    system_prompt=supervisor_system_prompt,
    checkpointer=checkpointer,
    name="supervisor_agent"
)
```

#### Technical Worker as Tool
```python
from langchain.tools import tool
from langchain.agents import create_agent

# Create the worker agent
technical_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    system_prompt=technical_system_prompt,
    name="technical_support_agent"
)

# Wrap as tool for supervisor
@tool
def technical_support_tool(query: str) -> str:
    """Handle technical support questions including errors, bugs, and troubleshooting.
    
    Use this tool for:
    - Error messages or codes
    - Software crashes or bugs
    - Installation/setup issues
    - Technical configuration
    - Performance problems
    """
    result = technical_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].content
```

### 3.3 System Prompts

#### Supervisor System Prompt
```
You are a supervisor agent that coordinates customer service inquiries.

Your role is to:
1. Analyze the user's query to understand their intent
2. Route technical questions to the Technical Support specialist
3. Handle general queries (greetings, thanks, clarifications) directly yourself
4. Provide clear, helpful responses

Available Tools:
- technical_support_tool: For technical issues, errors, bugs, troubleshooting

Guidelines:
- Use technical_support_tool for ANY technical question
- Handle greetings, thanks, and general chat yourself
- Maintain a friendly, professional tone
- When using a tool, trust its response and pass it to the user
- If unsure, ask the user for clarification

Remember: You're coordinating specialists, not doing specialized work yourself.
```

#### Technical Worker System Prompt
```
You are a technical support specialist with expertise in troubleshooting.

Your role is to:
- Diagnose technical problems
- Provide step-by-step solutions
- Explain error messages clearly
- Guide users through troubleshooting
- Suggest preventive measures

Guidelines:
- Be thorough and technical when appropriate
- Provide actionable steps
- Explain why issues occur when helpful
- If you need more information, ask specific questions
- CRITICAL: Include ALL findings and solutions in your final response
  (The supervisor only sees your final message)

Remember: Your response goes to the supervisor, who forwards it to the user.
Include everything needed in your final message.
```

### 3.4 Backend API Changes

**Minimal changes to `/chat` endpoint:**
```python
from backend.agents import get_supervisor

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # ... validation ...
    
    # Change from simple agent to supervisor
    supervisor = get_supervisor()  # Instead of get_agent()
    
    result = supervisor.invoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config
    )
    
    # ... rest stays the same ...
```

---

## 4. Testing Strategy

### 4.1 Unit Tests

#### Supervisor Tests (`test_supervisor.py`)
- ✅ Supervisor agent creation
- ✅ Tool registration and availability
- ✅ Routing decision for technical query
- ✅ Direct handling of general query
- ✅ Error handling for invalid queries
- ✅ Memory persistence across calls

#### Technical Worker Tests (`test_technical_worker.py`)
- ✅ Worker agent creation
- ✅ Response generation
- ✅ System prompt configuration
- ✅ Tool wrapper functionality
- ✅ Error handling

### 4.2 Integration Tests

#### Routing Tests (`test_main.py` updates)
- ✅ Technical query routes to worker
- ✅ General query handled by supervisor
- ✅ Multi-turn conversation maintains context
- ✅ Worker response returned correctly
- ✅ Session persistence works
- ✅ Error handling for tool failures

### 4.3 Manual Testing Scenarios

1. **Technical Routing:**
   - User: "I'm getting error 500 when logging in"
   - Expected: Routes to Technical Support
   - Verify: Response addresses the error

2. **General Handling:**
   - User: "Hello, how are you?"
   - Expected: Supervisor handles directly
   - Verify: Friendly greeting response

3. **Conversation Context:**
   - User: "I need help with an error"
   - Agent: "What error are you seeing?"
   - User: "Error 404"
   - Expected: Remembers context, routes to tech

4. **Ambiguous Query:**
   - User: "I need help"
   - Expected: Supervisor asks for clarification
   - Verify: Prompts for more details

5. **Mixed Conversation:**
   - User: "Thanks for the help!"
   - Expected: Supervisor handles thanks
   - Verify: Appropriate acknowledgment

---

## 5. Success Criteria

### 5.1 Functional Requirements
- ✅ Supervisor agent successfully created with tool integration
- ✅ Technical worker responds when called
- ✅ Routing works correctly for technical vs general queries
- ✅ Conversation memory maintained across routing
- ✅ Error handling covers edge cases
- ✅ API endpoint returns proper responses

### 5.2 Quality Requirements
- ✅ All automated tests pass (target: 45+ tests)
- ✅ Test coverage >70%
- ✅ No ESLint errors in frontend
- ✅ No Ruff errors in backend
- ✅ CI/CD pipeline passes
- ✅ Manual test scenarios all pass

### 5.3 Documentation Requirements
- ✅ Backend README updated with Phase 3 info
- ✅ Root README updated with multi-agent architecture
- ✅ Code comments explain routing logic
- ✅ System prompts documented
- ✅ Testing guide updated

---

## 6. Timeline

### 6.1 Development Phases

**Phase 3.1: Supervisor Setup (3-4 hours)**
- Create supervisor agent module
- Implement basic routing logic
- Test supervisor creation

**Phase 3.2: Technical Worker (2-3 hours)**
- Convert Phase 2 agent pattern
- Create technical worker
- Wrap as tool
- Test worker independently

**Phase 3.3: Integration (2-3 hours)**
- Integrate supervisor with backend
- Update /chat endpoint
- Test routing end-to-end

**Phase 3.4: Testing & Documentation (2-3 hours)**
- Write unit tests
- Write integration tests
- Update documentation
- Manual testing

**Total Estimated Time: 9-13 hours (1-2 days)**  
**With AI Assistance: 4-6 hours (0.5-1 day)**

---

## 7. Risk Assessment

### 7.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Routing logic doesn't work correctly | Low | High | Use clear tool descriptions, test thoroughly |
| Worker responses incomplete | Medium | Medium | Emphasize "include everything" in system prompt |
| Memory doesn't persist across routing | Low | High | Use same checkpointer for all agents |
| Performance degradation (extra LLM call) | Low | Low | GPT-4o-mini is fast, acceptable latency |

### 7.2 Mitigation Strategies

1. **Routing Issues:**
   - Write specific tool descriptions
   - Use LangSmith tracing to debug
   - Test with diverse queries
   - Iterate on supervisor prompt

2. **Incomplete Responses:**
   - Emphasize final output in worker prompts
   - Test worker independently
   - Use ToolRuntime to pass context if needed

3. **Memory Problems:**
   - Use same checkpointer instance
   - Test conversation continuity
   - Verify thread_id handling

---

## 8. Dependencies

### 8.1 Prerequisites
- ✅ Phase 2 complete (simple agent working)
- ✅ LangChain v1.0 installed
- ✅ OpenAI API key configured
- ✅ Testing infrastructure in place

### 8.2 Required Packages
No new packages needed - all dependencies from Phase 2 sufficient.

### 8.3 External Dependencies
- OpenAI API availability
- LangSmith (optional, for debugging)

---

## 9. Future Considerations

### 9.1 Phase 4 Preparation
This phase establishes the pattern for adding workers:
- Billing Support agent (Phase 4)
- Policy & Compliance agent (Phase 4)

### 9.2 Phase 5 Integration
Technical worker will be enhanced with:
- RAG tool for document retrieval
- Access to technical knowledge base
- Vector search capabilities

### 9.3 Scalability
Architecture supports easy addition of:
- More worker agents
- More tools per agent
- Different models per agent
- Persistent memory backends

---

## 10. Acceptance Criteria

### 10.1 Definition of Done

- ✅ Code implemented and committed
- ✅ All tests passing (unit + integration)
- ✅ CI/CD pipeline green
- ✅ Documentation updated
- ✅ Manual testing complete
- ✅ Code reviewed (self-review or pair)
- ✅ No linter errors
- ✅ Performance acceptable (<3s response time)

### 10.2 Demo Scenarios

1. Show technical query routing to worker
2. Show general query handled by supervisor
3. Show conversation context maintained
4. Show fallback for ambiguous queries
5. Show error handling

---

## 11. References

- [LangChain v1.0 Multi-Agent Docs](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [LangChain v1.0 Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [Tool-Calling Pattern](https://docs.langchain.com/oss/python/langchain/tools)
- Phase 2 PRD: `tasks/0002-prd-simple-agent-foundation.md`
- Project Spec: `agentic-customer-specs.md`

---

**Version**: 1.0  
**Last Updated**: November 3, 2025  
**Status**: Ready for Implementation ✅

