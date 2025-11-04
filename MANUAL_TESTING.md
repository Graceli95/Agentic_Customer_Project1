# Manual Testing Guide - Phase 3: Multi-Agent Supervisor Architecture

This guide provides step-by-step instructions for manually testing the customer service AI application with multi-agent routing capabilities.

## 📋 Prerequisites

Before testing, ensure:

- ✅ Backend dependencies installed: `cd backend && pip install -r requirements.txt`
- ✅ Frontend dependencies installed: `cd frontend && npm install`
- ✅ OpenAI API key configured in `backend/.env`
- ✅ All automated tests pass: `make test`

## 🚀 Setup

### 1. Configure Environment

Create `backend/.env` file (copy from `.env.example`):

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Optional: Enable LangSmith tracing for debugging multi-agent interactions
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_your-key-here
LANGSMITH_PROJECT=customer-service-phase3
```

### 2. Start Backend Server

In **Terminal 1**:

```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify backend is running:**
- Open: http://localhost:8000
- Should see: `{"message": "Customer Service API is running", ...}`

### 3. Start Frontend Server

In **Terminal 2**:

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
```

**Verify frontend is running:**
- Open: http://localhost:3000
- Should see: Chat interface with loading spinner, then chat UI

---

## 🧪 Test Cases

### Test 1: First Message - Basic Interaction ✅

**Purpose:** Verify agent can respond to a simple message

**Steps:**
1. Open http://localhost:3000
2. Wait for chat interface to load
3. Type: `Hello, how are you?`
4. Press Enter or click Send button

**Expected Results:**
- ✅ Message appears in chat with user styling (blue bubble, right-aligned)
- ✅ Loading indicator appears ("AI is thinking...")
- ✅ AI response appears within 2-5 seconds
- ✅ AI response has different styling (gray bubble, left-aligned)
- ✅ Response is contextually appropriate (greeting back)
- ✅ Input field is disabled during loading
- ✅ Input field re-enables after response

**Example AI Response:**
```
"Hello! I'm doing well, thank you for asking. How can I assist you today?"
```

---

### Test 2: Conversation Context - Memory Test ✅

**Purpose:** Verify agent maintains conversation history

**Steps:**
1. Continue from Test 1 (same session)
2. Type: `My name is Alice`
3. Wait for response
4. Type: `What is my name?`
5. Wait for response

**Expected Results:**
- ✅ First message: AI acknowledges name
- ✅ Second message: AI correctly recalls "Alice"
- ✅ All messages appear in conversation history
- ✅ Messages are in chronological order

**Example Responses:**
```
User: My name is Alice
AI: Nice to meet you, Alice! How can I help you today?

User: What is my name?
AI: Your name is Alice.
```

---

### Test 3: Session Persistence - Page Refresh ✅

**Purpose:** Verify session ID persists across page refreshes

**Steps:**
1. Continue from Test 2 (with conversation history)
2. Note the Session ID displayed in header (first 8 characters)
3. **Refresh the page** (Cmd+R / Ctrl+R)
4. Check Session ID in header

**Expected Results:**
- ✅ Session ID remains the same after refresh
- ✅ Chat interface reloads (conversation history clears - this is expected in Phase 2)
- ✅ New messages use the same session ID
- ✅ Backend logs show same `thread_id` being used

**Note:** In Phase 2, conversation history is stored in-memory on the backend. Refreshing the frontend clears the UI but the backend maintains the session's conversation memory.

---

### Test 4: Session Context After Refresh ✅

**Purpose:** Verify backend maintains conversation memory

**Steps:**
1. After refreshing (Test 3), type: `Do you still remember my name?`
2. Wait for response

**Expected Results:**
- ✅ AI remembers "Alice" from before refresh
- ✅ Response indicates memory is maintained

**Example Response:**
```
"Yes, your name is Alice."
```

**If AI doesn't remember:**
- ❌ Check backend logs for `thread_id` consistency
- ❌ Verify `InMemorySaver` is configured correctly
- ❌ Ensure session ID in request matches previous requests

---

### Test 5: Clear Conversation - New Session ✅

**Purpose:** Verify "Clear Conversation" button starts fresh session

**Steps:**
1. Continue from Test 4 (with conversation history)
2. Note current Session ID
3. Click **"Clear Chat"** button in header
4. Check new Session ID

**Expected Results:**
- ✅ Session ID changes (new UUID generated)
- ✅ Chat interface clears (no message history)
- ✅ localStorage is updated with new session ID
- ✅ Input field is ready for new message

**Verify new session:**
5. Type: `What is my name?`
6. Wait for response

**Expected Result:**
- ✅ AI does not know the name (fresh session)

**Example Response:**
```
"I don't have that information. Could you please tell me your name?"
```

---

### Test 6: Error Handling - Invalid Input ✅

**Purpose:** Verify UI handles errors gracefully

**Steps:**
1. Start fresh session
2. Try to send empty message (should be blocked by UI)
3. Type a very long message (2000+ characters)
4. Try to send

**Expected Results:**
- ✅ Empty message: Send button is disabled
- ✅ Long message: Character counter shows limit exceeded
- ✅ Long message: Send button is disabled
- ✅ Long message: Error styling on input (red border)
- ✅ Cannot submit message over limit

---

### Test 7: Error Handling - Backend Issues 🔧

**Purpose:** Verify UI handles backend errors

**Test 7a: Backend Offline**

**Steps:**
1. Stop backend server (Ctrl+C in Terminal 1)
2. Try to send message: `Hello`

**Expected Results:**
- ✅ Error message appears in chat
- ✅ Error has distinct styling (red border/background)
- ✅ Error message is user-friendly: "Network error: Could not connect..."
- ✅ Input field re-enables
- ✅ User can try again

**Test 7b: Invalid API Key**

**Steps:**
1. Edit `backend/.env`, set `OPENAI_API_KEY=invalid-key`
2. Restart backend server
3. Send message: `Hello`

**Expected Results:**
- ✅ Error message appears in chat
- ✅ Error indicates authentication issue
- ✅ Helpful message like: "Authentication Error: Please check your API key"

---

### Test 8: Loading States ✅

**Purpose:** Verify all loading indicators work

**Steps:**
1. Start fresh session
2. Type: `Tell me a story about a robot`
3. Observe loading behavior

**Expected Results:**
- ✅ Send button changes to spinner icon while loading
- ✅ Input field is disabled during loading
- ✅ "AI is thinking..." message appears
- ✅ Three animated dots show activity
- ✅ Loading message has distinct styling
- ✅ Loading indicator removes when response arrives

---

### Test 9: UI/UX - Visual Polish ✅

**Purpose:** Verify UI meets design requirements

**Checklist:**
- ✅ User messages: Blue background, right-aligned
- ✅ AI messages: Gray background, left-aligned
- ✅ Error messages: Red styling, distinct from normal messages
- ✅ Chat icon/logo visible in header
- ✅ Session ID truncated and displayed (e.g., "550e8400...")
- ✅ Message count visible in header
- ✅ "Clear Chat" button visible and functional
- ✅ Messages have timestamps
- ✅ Auto-scroll to latest message
- ✅ Text input has placeholder text
- ✅ Keyboard shortcuts work (Enter to send, Shift+Enter for new line)
- ✅ Character limit counter appears near limit

---

## 🔀 Phase 3: Multi-Agent Routing Tests

These tests verify the supervisor agent's intelligent routing to specialized workers.

### Test 10: Technical Query Routing ✅

**Purpose:** Verify technical queries route to Technical Support worker

**Steps:**
1. Start fresh session
2. Type: `Getting Error 500 when trying to log in`
3. Wait for response
4. **Check backend logs** for routing indicator

**Expected Results:**
- ✅ AI provides technical troubleshooting response
- ✅ Response includes diagnostic steps
- ✅ Backend logs show: `🔀 ROUTING: Query routed to worker agent`
- ✅ Response is detailed and technical in nature

**Example Response:**
```
"I understand you're experiencing an Error 500 (Internal Server Error) when trying to log in. Let's troubleshoot this step by step:

1. First, try clearing your browser cache and cookies
2. Check if the issue persists in incognito/private mode
3. Verify your credentials are correct
4. Try a different browser
5. Check if the service is available at [status page]

If none of these steps resolve the issue, please provide:
- What browser are you using?
- Did this start suddenly or after a recent update?
- Do you see any error messages in the console?"
```

---

### Test 11: General Query Direct Handling ✅

**Purpose:** Verify general queries handled directly by supervisor

**Steps:**
1. Continue from Test 10 (same session)
2. Type: `Thank you for your help!`
3. Wait for response
4. **Check backend logs** for routing indicator

**Expected Results:**
- ✅ AI provides friendly acknowledgment
- ✅ Backend logs show: `✋ DIRECT: Supervisor handled query directly`
- ✅ Response is conversational, not technical
- ✅ No routing to worker occurred

**Example Response:**
```
"You're welcome! I'm glad I could help. If you continue to have issues or need any other assistance, please don't hesitate to ask!"
```

---

### Test 12: Routing with Context Maintenance ✅

**Purpose:** Verify context maintained across routing decisions

**Steps:**
1. Continue from Test 11 (same session with login error discussed)
2. Type: `I tried clearing cache but still getting the error`
3. Wait for response
4. Check logs for routing

**Expected Results:**
- ✅ AI routes to Technical Support again (technical follow-up)
- ✅ Logs show: `🔀 ROUTING`
- ✅ Worker remembers context (previous error 500, cache clearing)
- ✅ Response builds on previous troubleshooting steps

**Example Response:**
```
"I see you've already tried clearing the cache but the Error 500 persists. Let's try these additional steps:

1. Check your browser's console for more specific error details (F12 → Console tab)
2. Try accessing the login page directly via [URL]
3. Test your network connection
4. Verify the login endpoint is responding: [test URL]

Since basic troubleshooting hasn't resolved it, this may be a server-side issue. Can you tell me:
- What time did the error start occurring?
- Are other users reporting similar issues?"
```

---

### Test 13: Mixed Query Type Conversation ✅

**Purpose:** Verify supervisor handles mixed technical and general queries

**Steps:**
1. Start fresh session
2. Type: `Hello! I need some help`
3. Wait for response (should be direct)
4. Type: `My app keeps crashing on startup`
5. Wait for response (should route)
6. Type: `That's frustrating`
7. Wait for response (should be direct)
8. Type: `What logs should I check?`
9. Wait for response (should route)

**Expected Results:**
- ✅ Step 2: Direct handling (general greeting)
- ✅ Step 4: Routes to Technical Support (technical issue)
- ✅ Step 6: Direct handling (emotional response)
- ✅ Step 8: Routes to Technical Support (technical question)
- ✅ Context maintained throughout mixed conversation
- ✅ Appropriate routing decisions for each query type

**Logs should show:**
```
✋ DIRECT: Supervisor handled query directly (Hello)
🔀 ROUTING: Query routed to worker agent (crashing)
✋ DIRECT: Supervisor handled query directly (frustrating)
🔀 ROUTING: Query routed to worker agent (logs)
```

---

### Test 14: Different Technical Query Types ✅

**Purpose:** Verify routing works for various technical issues

**Test multiple technical queries (fresh session for each):**

| Query | Expected Routing | Expected Response Type |
|-------|-----------------|----------------------|
| "Error 404 not found" | 🔀 ROUTING | Troubleshooting steps |
| "Can't install the software" | 🔀 ROUTING | Installation guidance |
| "Performance is very slow" | 🔀 ROUTING | Performance diagnosis |
| "Getting timeout errors" | 🔀 ROUTING | Network troubleshooting |
| "App won't start" | 🔀 ROUTING | Startup diagnostics |

**For each query:**
1. Start fresh session
2. Send query
3. Verify logs show `🔀 ROUTING`
4. Verify response is technical and detailed

---

### Test 15: Boundary Cases - Routing Decisions ✅

**Purpose:** Test edge cases in routing logic

**Test these ambiguous queries:**

**Test 15a: Ambiguous Query**
- Query: `How do I use this?`
- Expected: Could route or handle directly (context-dependent)
- Verify: Response is helpful regardless of routing

**Test 15b: Question About Troubleshooting**
- Query: `Can you help me troubleshoot?`
- Expected: May route to Technical Support
- Verify: Appropriate routing based on context

**Test 15c: Generic Help Request**
- Query: `I need help`
- Expected: Likely direct handling (needs more info)
- Verify: AI asks clarifying questions

**Test 15d: Technical Term in General Context**
- Query: `I love how fast the installation was!`
- Expected: Direct handling (positive feedback, not a problem)
- Verify: Logs show `✋ DIRECT`

---

### Test 16: Routing Visibility in Logs ✅

**Purpose:** Verify routing indicators appear correctly in logs

**Steps:**
1. Keep backend terminal visible (Terminal 1)
2. Run test script: `cd backend && ./test_routing_logs.sh`
3. Observe log output

**Expected Log Output:**
```
# Technical queries show:
🔀 ROUTING: Query routed to worker agent (session: xxx, time: X.XXs)

# General queries show:
✋ DIRECT: Supervisor handled query directly (session: xxx, time: X.XXs)
```

**Verify:**
- ✅ Routing indicators appear for every query
- ✅ Session ID is logged
- ✅ Execution time is logged
- ✅ Indicators are clearly visible (emoji + text)

---

### Test 17: Session Persistence with Routing ✅

**Purpose:** Verify session persists across routing and page refreshes

**Steps:**
1. Start fresh session
2. Type: `Getting Error 500 on login` (technical - routes)
3. Note Session ID in header
4. **Refresh page** (Cmd+R / Ctrl+R)
5. Check Session ID matches
6. Type: `What was my error?`

**Expected Results:**
- ✅ Session ID unchanged after refresh
- ✅ AI remembers "Error 500 on login"
- ✅ May route again based on context
- ✅ Conversation history maintained on backend

---

### Test 18: Clear Session with Routing History ✅

**Purpose:** Verify clear conversation works after routing

**Steps:**
1. Have conversation with routing (technical query)
2. Note routing occurred in logs
3. Click **"Clear Chat"** button
4. Type: `What was I asking about?`

**Expected Results:**
- ✅ New Session ID generated
- ✅ AI doesn't remember previous conversation
- ✅ Routing still works for new queries
- ✅ Clean slate confirmed

**Example Response:**
```
"I don't have any previous context. How can I help you today?"
```

---

### Test 19: Multi-turn Technical Conversation ✅

**Purpose:** Verify extended technical troubleshooting maintains context

**Steps:**
1. Start fresh session
2. Have 5+ turn technical troubleshooting conversation

**Example Conversation:**
```
User: My app crashes on startup
AI: [Routes → Technical troubleshooting response]

User: I checked the logs and see "memory error"
AI: [Routes → Memory-specific guidance]

User: I increased memory allocation but still crashes
AI: [Routes → Advanced diagnostics]

User: Where can I find the crash dumps?
AI: [Routes → File location guidance]

User: Thanks, I found them!
AI: [Direct → Acknowledgment]
```

**Expected Results:**
- ✅ Appropriate routing for each technical question
- ✅ Direct handling for non-technical responses
- ✅ Full context maintained throughout
- ✅ Technical worker provides consistent, building advice

---

### Test 20: Performance - Routing Overhead ✅

**Purpose:** Verify routing doesn't significantly impact response time

**Steps:**
1. Time several queries with routing
2. Time several queries with direct handling
3. Compare response times

**Expected Results:**
- ✅ Technical queries (with routing): 1-3 seconds
- ✅ General queries (direct): 0.5-2 seconds
- ✅ Routing overhead: < 1 second difference
- ✅ No significant performance degradation
- ✅ Times are logged in routing indicators

**Note:** Response times depend on OpenAI API latency and query complexity.

---

### Test 21: Multi-turn Conversation ✅

**Purpose:** Verify extended conversations work smoothly

**Steps:**
1. Start fresh session
2. Have a 10-message conversation
3. Test various topics and follow-ups

**Example Conversation:**
```
User: What services do you offer?
AI: [Response about services]

User: Tell me more about the first one
AI: [Detailed response]

User: What are the pricing options?
AI: [Pricing information]

[Continue for 10+ exchanges]
```

**Expected Results:**
- ✅ All messages display correctly
- ✅ Conversation history maintains order
- ✅ Agent maintains context throughout
- ✅ No performance degradation
- ✅ Auto-scroll keeps latest messages visible
- ✅ No UI glitches or layout issues

---

## 📊 Test Results Summary

Use this checklist to track testing progress:

### Phase 2: Core Functionality Tests

| Test | Description | Status | Notes |
|------|-------------|--------|-------|
| 1 | Basic Interaction | ⬜ | |
| 2 | Conversation Context | ⬜ | |
| 3 | Session Persistence | ⬜ | |
| 4 | Context After Refresh | ⬜ | |
| 5 | Clear Conversation | ⬜ | |
| 6 | Invalid Input Handling | ⬜ | |
| 7a | Backend Offline Error | ⬜ | |
| 7b | Invalid API Key Error | ⬜ | |
| 8 | Loading States | ⬜ | |
| 9 | UI/UX Visual Polish | ⬜ | |

### Phase 3: Multi-Agent Routing Tests

| Test | Description | Status | Notes |
|------|-------------|--------|-------|
| 10 | Technical Query Routing | ⬜ | |
| 11 | General Query Direct Handling | ⬜ | |
| 12 | Routing with Context Maintenance | ⬜ | |
| 13 | Mixed Query Type Conversation | ⬜ | |
| 14 | Different Technical Query Types | ⬜ | |
| 15a-d | Boundary Cases - Routing Decisions | ⬜ | |
| 16 | Routing Visibility in Logs | ⬜ | |
| 17 | Session Persistence with Routing | ⬜ | |
| 18 | Clear Session with Routing History | ⬜ | |
| 19 | Multi-turn Technical Conversation | ⬜ | |
| 20 | Performance - Routing Overhead | ⬜ | |
| 21 | Multi-turn Conversation | ⬜ | |

**Legend:** ⬜ Not Tested | ✅ Passed | ❌ Failed | ⚠️ Issues Found

---

## 🐛 Troubleshooting

### Backend won't start

**Error:** `OPENAI_API_KEY must be set`

**Solution:**
1. Check `backend/.env` file exists
2. Verify API key is set: `OPENAI_API_KEY=sk-proj-...`
3. Restart backend server

---

### Frontend shows "Network error"

**Cause:** Backend not running or wrong URL

**Solution:**
1. Verify backend is running on port 8000
2. Check `frontend/.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Default should be: `http://localhost:8000`

---

### Agent doesn't remember context

**Cause:** Session ID changing or missing

**Solution:**
1. Check browser console for session ID
2. Verify localStorage has `session_id` key
3. Check backend logs show consistent `thread_id`
4. Ensure `InMemorySaver` is configured in agent

---

### Slow responses (>10 seconds)

**Cause:** Network latency or OpenAI API delays

**Solutions:**
1. Check internet connection
2. Check OpenAI API status: https://status.openai.com/
3. Consider adding timeout warnings in UI

---

### UI styling issues

**Cause:** CSS not loading or build issues

**Solution:**
1. Clear Next.js cache: `rm -rf frontend/.next`
2. Rebuild: `cd frontend && npm run build`
3. Restart dev server

---

### Routing indicators not appearing in logs (Phase 3)

**Cause:** LOG_LEVEL too high or old backend version

**Solution:**
1. Check `backend/.env` has `LOG_LEVEL=INFO` or `LOG_LEVEL=DEBUG`
2. Verify you're running Phase 3 code (check for `supervisor_agent.py`)
3. Restart backend server
4. Check logs show `🔀 ROUTING` or `✋ DIRECT` indicators

---

### All queries routing to worker (Phase 3)

**Cause:** Supervisor prompt issue or worker tool description too broad

**Solution:**
1. Verify supervisor system prompt in `backend/agents/supervisor_agent.py`
2. Check technical_support_tool description is specific
3. Restart backend to reload agent definitions
4. Test with clear general query: "Hello!"

---

### No routing occurring (Phase 3)

**Cause:** Supervisor not using tools or tool not registered

**Solution:**
1. Verify `technical_support_tool` is imported and registered with supervisor
2. Check supervisor was created with tools list
3. Enable LangSmith tracing to see tool calls
4. Check backend logs for agent initialization messages

---

### Context not maintained across routing

**Cause:** Different thread_id or checkpointer issue

**Solution:**
1. Verify same session_id used across requests
2. Check InMemorySaver is configured in supervisor
3. Verify `thread_id` in config matches `session_id`
4. Check backend logs show consistent thread_id

---

## 📝 Reporting Issues

When reporting issues, include:

1. **Test number** that failed
2. **Steps to reproduce**
3. **Expected vs Actual result**
4. **Screenshots** (if UI issue)
5. **Browser console errors** (F12 → Console)
6. **Backend logs** (from terminal)
7. **Environment details:**
   - OS
   - Browser & version
   - Node.js version
   - Python version

---

## ✅ Sign-off

**Tester Name:** _________________

**Date:** _________________

**Overall Assessment:**
- ⬜ All tests passed - Ready for production
- ⬜ Minor issues found - Document and proceed
- ⬜ Major issues found - Needs fixes before deployment

**Additional Notes:**

_________________________________________________

_________________________________________________

_________________________________________________

---

## 🎯 Next Steps After Testing

1. **Document any issues found** in GitHub Issues
2. **Update this guide** with any new edge cases discovered
3. **Mark Task 6.3 complete** in task list
4. **Proceed to Phase 4** (Additional worker agents) if all tests pass

---

**Testing Complete!** 🎉

If all Phase 3 tests pass:
- Multi-agent routing is working correctly
- Supervisor intelligently delegates to workers
- Context is maintained across routing
- System is ready for Phase 4: Additional Worker Agents (Billing, Compliance, General Info)

