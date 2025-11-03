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
- `backend/tests/test_agent.py` - **CREATED**: Comprehensive unit tests for agent creation, configuration, and error handling (10 tests)
- `backend/tests/test_main.py` - **UPDATED**: Added 13 new tests for /chat endpoint (27 total tests, 87% coverage)
- `backend/conftest.py` - **CREATED**: Pytest configuration with --run-integration flag for integration tests
- `MANUAL_TESTING.md` - **CREATED**: Comprehensive manual testing guide with 10 test cases, setup instructions, and troubleshooting

### Frontend Files
- `frontend/lib/sessionManager.ts` - **CREATED**: Session ID generation and management utilities with UUID v4 and localStorage
- `frontend/lib/api.ts` - **CREATED**: Backend API client with TypeScript types, error handling, and health checks
- `frontend/app/page.tsx` - **UPDATED**: Integrated ChatInterface component with full session management and SSR-safe loading state
- `frontend/components/ChatInterface.tsx` - **CREATED**: Main container orchestrating MessageList/MessageInput, API calls, state management, and clear conversation
- `frontend/components/MessageList.tsx` - **CREATED**: Displays conversation history with user/AI distinction, auto-scroll, and loading states
- `frontend/components/MessageInput.tsx` - **CREATED**: User input field with submit button, character limit, keyboard shortcuts, and validation
- `frontend/components/LoadingIndicator.tsx` - **INTEGRATED**: Loading indicator implemented inline in MessageList.tsx

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

- [x] 1.0 Backend: LangChain Agent Setup and Integration
  - [x] 1.1 Verify and update LangChain packages in requirements.txt to ensure v1.0+ compatibility
  - [x] 1.2 Create `backend/agents/simple_agent.py` with agent initialization using `create_agent()`
  - [x] 1.3 Update `backend/agents/__init__.py` to export `create_customer_service_agent` function
  - [x] 1.4 Update `backend/.env.example` with OpenAI and LangSmith configuration variables

- [x] 2.0 Backend: API Endpoint Updates and Error Handling
  - [x] 2.1 Create Pydantic models for ChatRequest and ChatResponse with session_id validation
  - [x] 2.2 Add POST `/chat` endpoint to `backend/main.py` that invokes the LangChain agent
  - [x] 2.3 Implement error handling for OpenAI API errors, invalid session IDs, and missing credentials
  - [x] 2.4 Add startup validation to check for OPENAI_API_KEY and initialize agent at startup

- [x] 3.0 Frontend: Session Management Implementation
  - [x] 3.1 Create `frontend/lib/sessionManager.ts` with UUID generation and localStorage utilities (branch: feat/phase2-3.1-create-session-manager)
  - [x] 3.2 Create `frontend/lib/api.ts` for backend API client with session ID support (branch: feat/phase2-3.2-create-api-client)
  - [x] 3.3 Add session initialization logic to generate/retrieve UUID on first load (branch: feat/phase2-3.3-session-initialization)

- [x] 4.0 Frontend: Chat Interface and User Experience
  - [x] 4.1 Create `frontend/components/MessageList.tsx` to display conversation history with user/AI distinction (branch: feat/phase2-4.1-create-message-list)
  - [x] 4.2 Create `frontend/components/MessageInput.tsx` with input field, submit button, and disabled state (branch: feat/phase2-4.2-create-message-input)
  - [x] 4.3 Create `frontend/components/LoadingIndicator.tsx` for "Agent is thinking..." display (implemented inline in MessageList.tsx)
  - [x] 4.4 Create `frontend/components/ChatInterface.tsx` as main container orchestrating all chat components (branch: feat/phase2-4.4-create-chat-interface)
  - [x] 4.5 Update `frontend/app/page.tsx` to use ChatInterface component with session management (branch: feat/phase2-4.5-integrate-chat-interface)
  - [x] 4.6 Add "Clear Conversation" button functionality to generate new session ID (implemented in ChatInterface.tsx)

- [ ] 5.0 Testing and Documentation
  - [x] 5.1 Create `backend/tests/test_agent.py` with unit tests for agent creation and basic invocation (branch: feat/phase2-5.1-create-agent-tests)
  - [x] 5.2 Update `backend/tests/test_main.py` to test `/chat` endpoint with agent integration (branch: feat/phase2-5.2-update-main-tests)
  - [x] 5.3 Create comprehensive manual testing guide with step-by-step checklist (MANUAL_TESTING.md)
  - [ ] 5.4 Update `backend/README.md` with Phase 2 setup instructions and LangSmith configuration
  - [ ] 5.5 Update root `README.md` with Phase 2 status, usage instructions, and conversation testing guide


