# Manual Testing Guide - Phase 2: Simple Agent Foundation

This guide provides step-by-step instructions for manually testing the customer service AI application.

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

# Optional: Enable LangSmith tracing for debugging
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_your-key-here
LANGSMITH_PROJECT=customer-service-phase2
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

### Test 10: Multi-turn Conversation ✅

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
| 10 | Multi-turn Conversation | ⬜ | |

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
3. **Mark Task 5.3 complete** in task list
4. **Proceed to Phase 3** (Multi-agent architecture) if all tests pass

---

**Testing Complete!** 🎉

If all tests pass, Phase 2 is ready for deployment and we can move to Phase 3: Multi-Agent Architecture.

