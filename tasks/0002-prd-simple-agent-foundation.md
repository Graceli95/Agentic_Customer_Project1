# Product Requirements Document: Simple Agent Foundation

**PRD Number**: 0002  
**Feature**: LangChain/LangGraph Integration with Real LLM Agent  
**Phase**: Phase 2 - Simple Agent Foundation  
**Created**: November 3, 2025  
**Target Audience**: Junior Developer  
**Status**: Ready for Implementation

---

## Introduction/Overview

This PRD covers Phase 2 of the Advanced Customer Service AI project: integrating LangChain/LangGraph with a real LLM to replace the echo response with an intelligent, stateful conversational agent.

**Problem**: Phase 1 established basic frontend-backend communication with a simple echo response. This doesn't demonstrate AI capabilities or maintain conversation context across multiple messages.

**Solution**: Integrate LangChain v1.0 with OpenAI to create a single, stateful agent that provides intelligent responses and maintains conversation history using LangGraph's checkpointing system.

**Key Outcomes**:
- Real LLM-powered responses instead of echo
- Conversation memory across multiple messages
- Session-based conversation management
- Foundation for multi-agent system (Phase 3+)

---

## Goals

1. **Integrate LangChain v1.0**: Use modern `create_agent()` pattern with proper LangChain v1.0 best practices
2. **Enable Real LLM Responses**: Connect to OpenAI API for intelligent, context-aware responses
3. **Implement Conversation Memory**: Use `InMemorySaver` checkpointer to maintain conversation history
4. **Manage User Sessions**: Implement thread-based session management for multiple users
5. **Enhance User Experience**: Add loading states and error handling to frontend
6. **Establish Development Workflow**: Set up LangSmith tracing for debugging and monitoring

---

## User Stories

**As a user**, I want to have a natural conversation with an AI assistant, so that I can get helpful responses to my customer service questions.

**As a user**, I want the AI to remember what I said earlier in the conversation, so that I don't have to repeat context.

**As a user**, I want to see a loading indicator when the AI is thinking, so that I know my message is being processed.

**As a user**, I want clear error messages if something goes wrong, so that I understand what happened.

**As a developer**, I want to use LangSmith tracing to debug the agent's behavior, so that I can understand how the LLM is responding.

**As a developer**, I want the agent code to follow LangChain v1.0 best practices, so that the codebase is maintainable and ready for Phase 3 expansion.

---

## Functional Requirements

### 1. LangChain/LangGraph Integration

- **REQ-1.1**: Backend must install LangChain v1.0+ packages:
  - `langchain>=1.0.0`
  - `langchain-openai>=1.0.0`
  - `langgraph>=1.0.0`
  - `langchain-core>=1.0.0`

- **REQ-1.2**: Agent must be created using `create_agent()` from `langchain.agents` (not manual LangGraph StateGraph)

- **REQ-1.3**: Agent must have a descriptive name: `"customer_service_agent"`

- **REQ-1.4**: Agent must NOT use deprecated patterns:
  - ❌ No LCEL pipe operators (`|`)
  - ❌ No `initialize_agent()` or `create_react_agent()`
  - ❌ No manual LangGraph for simple agent (save for Phase 3+)

### 2. OpenAI Integration

- **REQ-2.1**: Backend must use OpenAI GPT-4o-mini as the default model:
  - Model identifier: `"openai:gpt-4o-mini"`
  - Cost-effective for development
  - Good quality for customer service responses

- **REQ-2.2**: Backend must support easy upgrade to GPT-4:
  - Document model selection in code comments
  - Make model configurable via environment variable (optional)

- **REQ-2.3**: OpenAI API key must be loaded from environment variable `OPENAI_API_KEY`

- **REQ-2.4**: Backend must handle OpenAI API errors gracefully:
  - Invalid API key
  - Rate limiting (429 errors)
  - Network timeouts
  - Invalid model name

### 3. Conversation Memory

- **REQ-3.1**: Agent must use `InMemorySaver` checkpointer from `langgraph.checkpoint.memory`

- **REQ-3.2**: Each conversation must have a unique thread ID (session ID)

- **REQ-3.3**: Agent must maintain full conversation history per thread:
  - All user messages
  - All assistant responses
  - Chronological order preserved

- **REQ-3.4**: Memory must persist for the lifetime of the backend process

- **REQ-3.5**: Code must include comments about upgrading to persistent storage (PostgreSQL, Redis) in production

### 4. Session Management

- **REQ-4.1**: Frontend must generate UUID v4 session IDs:
  - Use `crypto.randomUUID()` or equivalent
  - Generate on first user visit
  - Store in localStorage as `session_id`

- **REQ-4.2**: Frontend must persist session ID across page refreshes

- **REQ-4.3**: Frontend must send session ID with every `/chat` request

- **REQ-4.4**: Backend must accept `session_id` in request body

- **REQ-4.5**: Backend must use session ID as LangGraph `thread_id`:
  ```python
  config = {"configurable": {"thread_id": session_id}}
  ```

- **REQ-4.6**: Backend must validate session ID format (UUID v4)

### 5. Backend API Updates

- **REQ-5.1**: `/chat` endpoint must be updated to invoke the LangChain agent

- **REQ-5.2**: Endpoint must accept request body:
  ```json
  {
    "message": "string (1-2000 characters)",
    "session_id": "string (UUID v4 format)"
  }
  ```

- **REQ-5.3**: Endpoint must return response:
  ```json
  {
    "response": "string (agent's response)",
    "session_id": "string (echo back for confirmation)"
  }
  ```

- **REQ-5.4**: Endpoint must use Pydantic models for request/response validation

- **REQ-5.5**: Remove the echo logic from Phase 1

### 6. System Prompt

- **REQ-6.1**: Agent must have a professional customer service system prompt

- **REQ-6.2**: System prompt must establish agent persona and guidelines:
  ```
  You are a helpful customer service assistant for our company.
  
  Your role is to:
  - Provide accurate, helpful information to customers
  - Be professional, friendly, and empathetic
  - Ask clarifying questions when needed
  - Maintain context from the conversation history
  
  Keep responses clear and concise while being thorough.
  ```

- **REQ-6.3**: System prompt can be easily modified for future phases

### 7. Error Handling

- **REQ-7.1**: Backend must catch and handle common errors:
  - OpenAI API errors → Return user-friendly message
  - Invalid session ID → Return 400 Bad Request
  - Missing API key → Log error and return 500
  - Agent invocation errors → Log and return generic error message

- **REQ-7.2**: All errors must be logged with appropriate log levels:
  - ERROR: API failures, missing credentials
  - WARNING: Invalid input, rate limiting
  - INFO: Successful requests

- **REQ-7.3**: Error responses must follow consistent format:
  ```json
  {
    "error": "User-friendly error message",
    "detail": "Technical details (dev only)",
    "session_id": "string"
  }
  ```

- **REQ-7.4**: Frontend must display error messages to user in a non-technical way

### 8. Frontend Updates

- **REQ-8.1**: Frontend must implement session ID generation and storage:
  ```javascript
  // Generate on first load if not exists
  if (!localStorage.getItem('session_id')) {
    localStorage.setItem('session_id', crypto.randomUUID());
  }
  ```

- **REQ-8.2**: Frontend must include "Clear Conversation" button:
  - Generates new session ID
  - Clears message history display
  - Starts fresh conversation

- **REQ-8.3**: Frontend must show loading states:
  - Disable input field while waiting for response
  - Show contextual loading message: "Agent is thinking..."
  - Display loading indicator (spinner or animation)

- **REQ-8.4**: Frontend must handle errors gracefully:
  - Display error messages in message list (distinct styling)
  - Re-enable input after error
  - Don't lose user's message on error

- **REQ-8.5**: Frontend must visually distinguish user vs AI messages:
  - Different background colors
  - Different text alignment (user: right, AI: left)
  - Optional: User and AI avatars/icons

- **REQ-8.6**: Frontend must update API call to include session ID:
  ```javascript
  const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: userMessage,
      session_id: sessionId
    })
  });
  ```

### 9. Environment Variables

- **REQ-9.1**: Backend `.env.example` must be updated with:
  ```bash
  # OpenAI Configuration (REQUIRED)
  OPENAI_API_KEY=sk-proj-...
  
  # LangSmith Configuration (OPTIONAL - for debugging)
  LANGSMITH_API_KEY=lsv2_...
  LANGSMITH_TRACING=true
  LANGSMITH_PROJECT=customer-service-phase2
  
  # Application Configuration
  ENVIRONMENT=development
  LOG_LEVEL=INFO
  ```

- **REQ-9.2**: Each environment variable must have clear comments explaining:
  - Whether it's required or optional
  - Where to obtain the value
  - What it's used for

### 10. LangSmith Integration (Optional but Recommended)

- **REQ-10.1**: Documentation must explain LangSmith tracing setup

- **REQ-10.2**: If `LANGSMITH_TRACING=true`, all agent interactions must be traced

- **REQ-10.3**: LangSmith must be positioned as:
  - Optional for running the application
  - Highly recommended for development and debugging
  - Essential for understanding agent behavior

- **REQ-10.4**: README must include LangSmith dashboard URL: https://smith.langchain.com/

### 11. Testing

- **REQ-11.1**: Backend must have basic unit test for agent initialization:
  ```python
  def test_agent_creation():
      """Test that agent can be created successfully."""
      agent = create_customer_service_agent()
      assert agent is not None
      assert agent.name == "customer_service_agent"
  ```

- **REQ-11.2**: Backend must have integration test for agent invocation:
  ```python
  def test_agent_responds():
      """Test that agent can generate a response."""
      result = agent.invoke({
          "messages": [{"role": "user", "content": "Hello"}]
      })
      assert "messages" in result
      assert len(result["messages"]) > 0
  ```

- **REQ-11.3**: Manual testing checklist must be documented:
  - Start backend server
  - Start frontend
  - Send first message → Verify response
  - Send second message → Verify context maintained
  - Refresh page → Verify session persists
  - Click "Clear Conversation" → Verify new session starts

---

## Non-Goals (Out of Scope)

- ❌ **Multi-agent architecture** (covered in Phase 3)
- ❌ **RAG/CAG retrieval** (covered in Phase 5)
- ❌ **AWS Bedrock integration** (covered in Phase 6)
- ❌ **Streaming responses** (covered in Phase 6)
- ❌ **Multiple conversation sessions UI** (only single active session)
- ❌ **Persistent storage for conversations** (in-memory only, will upgrade in production)
- ❌ **Tool usage by agent** (no tools yet, Phase 3+)
- ❌ **Advanced error recovery** (basic handling only)
- ❌ **Response formatting** (plain text only, no markdown rendering yet)

---

## Design Considerations

### Agent Architecture (Simple)

```
┌─────────────────────────────────────────────┐
│           Frontend (Next.js)                │
│                                             │
│  [User Input] → [Send Message]             │
│       ↓                                     │
│  POST /chat {                               │
│    message: "Hello",                        │
│    session_id: "uuid-here"                  │
│  }                                          │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────┐
│         Backend (FastAPI)                   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │    /chat Endpoint                   │   │
│  │  • Validate request                 │   │
│  │  • Extract message & session_id     │   │
│  │  • Create config with thread_id     │   │
│  └───────────────┬─────────────────────┘   │
│                  ↓                          │
│  ┌─────────────────────────────────────┐   │
│  │   Customer Service Agent            │   │
│  │   (create_agent)                    │   │
│  │                                     │   │
│  │   Model: GPT-4o-mini                │   │
│  │   Memory: InMemorySaver             │   │
│  │   Tools: [] (none yet)              │   │
│  │   Name: "customer_service_agent"    │   │
│  └───────────────┬─────────────────────┘   │
│                  ↓                          │
│  ┌─────────────────────────────────────┐   │
│  │   Response Processing               │   │
│  │  • Extract final message            │   │
│  │  • Format response                  │   │
│  │  • Return to frontend               │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### File Structure Updates

```
backend/
├── agents/
│   ├── __init__.py
│   └── simple_agent.py           # NEW: Simple agent creation
├── main.py                        # UPDATED: Use agent instead of echo
├── requirements.txt               # UPDATED: Add LangChain packages
├── .env.example                   # UPDATED: Add OpenAI & LangSmith vars
└── tests/
    ├── test_agent.py              # NEW: Agent tests
    └── test_main.py               # UPDATED: Test new endpoint behavior

frontend/
├── src/
│   ├── app/
│   │   └── page.js                # UPDATED: Add session mgmt, loading states
│   └── lib/
│       ├── api.js                 # UPDATED: Include session_id in requests
│       └── sessionManager.js      # NEW: Session ID utilities
└── package.json                   # (no changes needed)
```

### Code Structure

**Backend Agent Module** (`backend/agents/simple_agent.py`):
```python
"""
Simple Customer Service Agent using LangChain v1.0.

This module creates a single, stateful agent for Phase 2.
In Phase 3+, this will be replaced with a multi-agent system.
"""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import os

# Initialize checkpointer for conversation memory
checkpointer = InMemorySaver()

def create_customer_service_agent():
    """
    Create a simple customer service agent.
    
    Returns:
        Agent: Configured LangChain agent with memory
    """
    agent = create_agent(
        model="openai:gpt-4o-mini",  # Cost-effective for development
        # To upgrade to GPT-4: model="openai:gpt-4"
        tools=[],  # No tools yet (Phase 3+)
        system_prompt="""You are a helpful customer service assistant.
        
Your role is to:
- Provide accurate, helpful information to customers
- Be professional, friendly, and empathetic
- Ask clarifying questions when needed
- Maintain context from the conversation history

Keep responses clear and concise while being thorough.""",
        checkpointer=checkpointer,  # Enables conversation memory
        name="customer_service_agent"  # Required in LangChain v1.0
    )
    
    return agent
```

**Backend Main Update** (`backend/main.py`):
```python
from backend.agents.simple_agent import create_customer_service_agent

# Initialize agent once at startup
agent = create_customer_service_agent()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Process user message through LangChain agent.
    """
    try:
        # Create config with thread_id for conversation memory
        config = {"configurable": {"thread_id": request.session_id}}
        
        # Invoke agent
        result = agent.invoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config
        )
        
        # Extract response from final message
        response_text = result["messages"][-1].content
        
        return {
            "response": response_text,
            "session_id": request.session_id
        }
    
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process message. Please try again."
        )
```

**Frontend Session Management** (`frontend/src/lib/sessionManager.js`):
```javascript
export function getOrCreateSessionId() {
  let sessionId = localStorage.getItem('session_id');
  
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem('session_id', sessionId);
  }
  
  return sessionId;
}

export function clearSession() {
  const newSessionId = crypto.randomUUID();
  localStorage.setItem('session_id', newSessionId);
  return newSessionId;
}
```

---

## Technical Considerations

### LangChain v1.0 Compliance

**✅ DO (Modern v1.0 Patterns)**:
- Use `create_agent()` from `langchain.agents`
- Use `InMemorySaver` for checkpointing
- Pass `thread_id` in config for conversation memory
- Always provide agent `name` parameter
- Use string model identifiers: `"openai:gpt-4o-mini"`

**❌ DON'T (Deprecated v0.x Patterns)**:
- Don't use `initialize_agent()` or `create_react_agent()`
- Don't use LCEL pipe operators (`|`)
- Don't manually build LangGraph StateGraph for simple agent
- Don't use legacy memory classes like `ConversationBufferMemory`

### Model Selection Rationale

**GPT-4o-mini (Default)**:
- Cost: ~$0.15 per 1M input tokens (13x cheaper than GPT-4)
- Quality: Sufficient for customer service responses
- Speed: Faster than GPT-4
- Perfect for development and testing

**GPT-4 (Optional Upgrade)**:
- Cost: ~$2.50 per 1M input tokens
- Quality: Higher reasoning capability
- Use when: Response quality is critical
- Easy to switch: Just change model parameter

### Memory Strategy

**Phase 2: InMemorySaver**
- ✅ Simple to implement
- ✅ No external dependencies
- ✅ Perfect for development
- ⚠️ Lost on server restart
- ⚠️ Not suitable for production

**Future: Persistent Storage**
- Phase 6+: PostgreSQL or Redis checkpointer
- Conversations survive restarts
- Support for scaling across multiple servers
- Migration path documented in code comments

### Session Management

**UUID v4 Format**: `550e8400-e29b-41d4-a716-446655440000`
- Generated by frontend using `crypto.randomUUID()`
- Stored in localStorage (persists across refreshes)
- Sent with every request
- Backend validates format using regex

**Clear Conversation Flow**:
1. User clicks "Clear Conversation"
2. Frontend generates new UUID
3. Frontend updates localStorage
4. Frontend clears message display
5. Next message uses new session ID (fresh conversation)

### Error Handling Strategy

**Backend**:
- Catch specific exceptions (OpenAI API errors, validation errors)
- Log all errors with context
- Return user-friendly messages (don't expose internals)
- Use appropriate HTTP status codes

**Frontend**:
- Display errors in message list (visually distinct)
- Keep input enabled for retry
- Don't lose user's typed message
- Provide helpful guidance ("Check your connection...")

---

## Success Metrics

1. **Functional Success**:
   - Agent responds intelligently to user queries (not just echoing)
   - Conversation context maintained across multiple messages
   - New sessions start fresh (no context bleed)

2. **Performance**:
   - Response time: < 5 seconds for typical queries
   - Agent initialization: < 2 seconds at startup
   - No memory leaks during extended conversations

3. **User Experience**:
   - Clear loading indicators during API calls
   - Error messages are understandable
   - Conversation history displays correctly
   - "Clear Conversation" button works intuitively

4. **Code Quality**:
   - All code follows LangChain v1.0 patterns
   - No linter errors
   - Basic tests pass
   - Clear code comments and documentation

5. **Developer Experience**:
   - LangSmith tracing works (if enabled)
   - Easy to test manually
   - Clear error logs
   - Environment setup is straightforward

---

## Open Questions

- ✅ **Resolved**: Model selection (GPT-4o-mini default, with upgrade path)
- ✅ **Resolved**: Memory persistence (InMemorySaver with upgrade notes)
- ✅ **Resolved**: Session management (Frontend generates UUIDs)
- ✅ **Resolved**: Error handling scope (Moderate - handling + logging + friendly messages)
- ⚠️ **Pending**: Should we add response time metrics in Phase 2? (Decision: Not yet, add in Phase 6 polish)
- ⚠️ **Pending**: Should we implement message retry on failure? (Decision: Manual retry by user, automatic retry in Phase 6)

---

## Acceptance Criteria

### Agent Functionality
- [ ] Agent created using `create_agent()` with all required parameters
- [ ] Agent uses GPT-4o-mini model
- [ ] Agent has `name="customer_service_agent"`
- [ ] Agent has professional system prompt
- [ ] Agent uses InMemorySaver checkpointer

### Conversation Memory
- [ ] First message in session gets appropriate response
- [ ] Second message maintains context from first message
- [ ] Agent can reference earlier parts of conversation
- [ ] Different session IDs create separate conversations
- [ ] Same session ID continues existing conversation

### Session Management
- [ ] Frontend generates UUID on first visit
- [ ] Session ID persists in localStorage
- [ ] Session ID survives page refresh
- [ ] "Clear Conversation" button generates new session
- [ ] Backend validates session ID format

### API Behavior
- [ ] `/chat` endpoint accepts message and session_id
- [ ] Endpoint returns response and session_id
- [ ] Invalid session ID returns 400 error
- [ ] Missing API key returns 500 error
- [ ] OpenAI errors return user-friendly messages

### Frontend Features
- [ ] Loading indicator shows while waiting for response
- [ ] Input field disabled during API call
- [ ] Error messages display in message list
- [ ] User and AI messages visually distinct
- [ ] "Clear Conversation" button works correctly
- [ ] Conversation history displays correctly

### Error Handling
- [ ] Invalid session ID handled gracefully
- [ ] OpenAI API errors don't crash application
- [ ] Network errors display helpful message
- [ ] All errors logged appropriately
- [ ] User can recover from errors

### Testing
- [ ] Agent initialization test passes
- [ ] Basic invocation test passes
- [ ] Manual testing checklist completed
- [ ] No linter errors in new code

### Documentation
- [ ] README updated with Phase 2 setup
- [ ] Environment variables documented
- [ ] LangSmith setup explained
- [ ] Code comments explain key decisions
- [ ] Upgrade paths documented (GPT-4, persistent storage)

---

## Dependencies

**Depends On**:
- ✅ Phase 1 (0001-prd-project-setup.md) - Must be complete

**Blocks**:
- Phase 3 (Supervisor + First Worker) - Cannot start until Phase 2 complete

---

## Timeline Estimate

- **Backend Agent Setup**: 1-2 hours
- **API Endpoint Updates**: 1 hour
- **Frontend Session Management**: 1-2 hours
- **Loading States & Error Handling**: 1-2 hours
- **Testing**: 1 hour
- **Documentation**: 1 hour
- **Total**: **6-9 hours**

---

## Implementation Notes

### Recommended Implementation Order

1. **Backend First** (Core Functionality):
   - Install LangChain packages
   - Create `simple_agent.py` module
   - Update `main.py` to use agent
   - Test with curl/Postman

2. **Frontend Session Management** (State):
   - Create session manager utility
   - Update API calls to include session_id
   - Add "Clear Conversation" button
   - Test session persistence

3. **User Experience** (Polish):
   - Add loading states
   - Style user vs AI messages
   - Implement error handling
   - Test complete flow

4. **Testing & Documentation** (Quality):
   - Write basic unit tests
   - Update README
   - Document environment setup
   - Complete manual testing checklist

### Testing Strategy

**Manual Testing Flow**:
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
pnpm dev

# Browser: Test conversation
1. Open http://localhost:3000
2. Send message: "Hello, I need help"
3. Verify: AI responds intelligently
4. Send message: "What did I just say?"
5. Verify: AI references previous message
6. Refresh page
7. Send message: "Do you remember our conversation?"
8. Verify: AI still has context
9. Click "Clear Conversation"
10. Send message: "What did we talk about?"
11. Verify: AI starts fresh (no context)
```

**API Testing with curl**:
```bash
# Test basic request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I need help with my account",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Test conversation continuity (same session_id)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did I just ask about?",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Test new session (different session_id)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did I just ask about?",
    "session_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

### Common Pitfalls to Avoid

1. **Forgetting to pass thread_id in config**:
   ```python
   # ❌ WRONG - no memory
   agent.invoke({"messages": [...]})
   
   # ✅ CORRECT - with memory
   config = {"configurable": {"thread_id": session_id}}
   agent.invoke({"messages": [...]}, config)
   ```

2. **Not handling missing API key**:
   - Check for `OPENAI_API_KEY` at startup
   - Provide clear error message if missing
   - Don't wait for first request to fail

3. **Frontend session ID generation**:
   - Use `crypto.randomUUID()` (built-in, secure)
   - Don't use `Math.random()` (not UUID format)
   - Store in localStorage, not sessionStorage

4. **Extracting agent response**:
   ```python
   # ❌ WRONG - might get intermediate messages
   response = result["messages"][0].content
   
   # ✅ CORRECT - get final response
   response = result["messages"][-1].content
   ```

### LangSmith Setup (Optional)

1. Create account at https://smith.langchain.com/
2. Generate API key from settings
3. Add to `.env`:
   ```bash
   LANGSMITH_API_KEY=lsv2_pt_...
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=customer-service-phase2
   ```
4. Run application
5. View traces in LangSmith dashboard
6. Use for debugging conversation flow and token usage

---

## References

### LangChain v1.0 Documentation
- **Agents**: https://docs.langchain.com/oss/python/langchain/agents
- **Memory/Checkpointing**: https://docs.langchain.com/oss/python/langchain/short-term-memory
- **Models**: https://docs.langchain.com/oss/python/langchain/models
- **Migration Guide**: https://docs.langchain.com/oss/python/migrate/langgraph-v1

### Tools & Services
- **LangSmith**: https://smith.langchain.com/
- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs

### Project Documentation
- **Phase 1 PRD**: `tasks/0001-prd-project-setup.md`
- **Architecture**: `ARCHITECTURE.md`
- **Development Guide**: `PHASED_DEVELOPMENT_GUIDE.md`

---

## Phase 2 Completion Checklist

Before moving to Phase 3:

- [ ] All acceptance criteria met
- [ ] Manual testing checklist completed
- [ ] Basic unit tests pass
- [ ] No linter errors
- [ ] Code committed to Git with message: `feat(phase2): add simple agent foundation`
- [ ] README updated with Phase 2 instructions
- [ ] Environment variables documented
- [ ] Known issues documented (if any)
- [ ] LangSmith tracing tested (optional but recommended)

---

**Status**: Ready for task breakdown and implementation  
**Next Step**: Begin implementation following recommended order  
**Next Phase**: Phase 3 - Supervisor + First Worker (PRD 0003)


