# Task List: Simple Agent Foundation (Phase 2)

**Source PRD**: `0002-prd-simple-agent-foundation.md`  
**Phase**: Phase 2 - Simple Agent Foundation  
**Status**: Ready for Implementation

---

## Relevant Files

### Backend Files
- `backend/agents/simple_agent.py` - **NEW**: Core agent creation module with LangChain v1.0 integration
- `backend/agents/__init__.py` - **UPDATE**: Export agent creation function
- `backend/main.py` - **UPDATE**: Replace echo endpoint with LangChain agent invocation
- `backend/requirements.txt` - **UPDATE**: Add LangChain v1.0+ packages (already includes some, verify versions)
- `backend/.env.example` - **UPDATE**: Add OpenAI and LangSmith configuration variables
- `backend/tests/test_agent.py` - **NEW**: Unit tests for agent creation and invocation
- `backend/tests/test_main.py` - **UPDATE**: Integration tests for /chat endpoint with agent

### Frontend Files
- `frontend/lib/sessionManager.js` - **NEW**: Session ID generation and management utilities
- `frontend/lib/api.js` - **NEW**: Backend API client with session ID support
- `frontend/app/page.tsx` - **UPDATE**: Transform landing page into chat interface with session management
- `frontend/components/ChatInterface.tsx` - **NEW**: Main chat container component
- `frontend/components/MessageList.tsx` - **NEW**: Display conversation history
- `frontend/components/MessageInput.tsx` - **NEW**: User input field with submit
- `frontend/components/LoadingIndicator.tsx` - **NEW**: Loading state display component

### Documentation Files
- `backend/README.md` - **UPDATE**: Add Phase 2 setup instructions and LangSmith configuration
- `README.md` - **UPDATE**: Update root README with Phase 2 status and usage

### Notes
- Backend tests use `pytest` and should be run with: `pytest backend/tests/`
- Frontend is TypeScript/Next.js, so we'll create `.tsx` files (not `.js`)
- Session management uses browser's `crypto.randomUUID()` and localStorage
- LangChain packages are already in requirements.txt but versions need verification

---

## Tasks

- [ ] 1.0 Backend: LangChain Agent Setup and Integration
  - [x] 1.1 Verify and update LangChain packages in requirements.txt to ensure v1.0+ compatibility
  - [x] 1.2 Create `backend/agents/simple_agent.py` with agent initialization using `create_agent()`
  - [ ] 1.3 Update `backend/agents/__init__.py` to export `create_customer_service_agent` function
  - [ ] 1.4 Update `backend/.env.example` with OpenAI and LangSmith configuration variables

- [ ] 2.0 Backend: API Endpoint Updates and Error Handling
  - [ ] 2.1 Create Pydantic models for ChatRequest and ChatResponse with session_id validation
  - [ ] 2.2 Add POST `/chat` endpoint to `backend/main.py` that invokes the LangChain agent
  - [ ] 2.3 Implement error handling for OpenAI API errors, invalid session IDs, and missing credentials
  - [ ] 2.4 Add startup validation to check for OPENAI_API_KEY and initialize agent at startup

- [ ] 3.0 Frontend: Session Management Implementation
  - [ ] 3.1 Create `frontend/lib/sessionManager.ts` with UUID generation and localStorage utilities
  - [ ] 3.2 Create `frontend/lib/api.ts` for backend API client with session ID support
  - [ ] 3.3 Add session initialization logic to generate/retrieve UUID on first load

- [ ] 4.0 Frontend: Chat Interface and User Experience
  - [ ] 4.1 Create `frontend/components/MessageList.tsx` to display conversation history with user/AI distinction
  - [ ] 4.2 Create `frontend/components/MessageInput.tsx` with input field, submit button, and disabled state
  - [ ] 4.3 Create `frontend/components/LoadingIndicator.tsx` for "Agent is thinking..." display
  - [ ] 4.4 Create `frontend/components/ChatInterface.tsx` as main container orchestrating all chat components
  - [ ] 4.5 Update `frontend/app/page.tsx` to use ChatInterface component with session management
  - [ ] 4.6 Add "Clear Conversation" button functionality to generate new session ID

- [ ] 5.0 Testing and Documentation
  - [ ] 5.1 Create `backend/tests/test_agent.py` with unit tests for agent creation and basic invocation
  - [ ] 5.2 Update `backend/tests/test_main.py` to test `/chat` endpoint with agent integration
  - [ ] 5.3 Perform manual testing following the checklist in PRD (conversation memory, session persistence, clear conversation)
  - [ ] 5.4 Update `backend/README.md` with Phase 2 setup instructions and LangSmith configuration
  - [ ] 5.5 Update root `README.md` with Phase 2 status, usage instructions, and conversation testing guide


