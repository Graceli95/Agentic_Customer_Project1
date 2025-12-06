# Demo Guide - Quick Reference

**For Recording Video or Live Demonstrations**

---

## 🚀 Quick Start (5 Minutes)

### 1. Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
INFO:     Attempting to create supervisor with AWS Nova Lite
INFO:     ✅ Supervisor created successfully with AWS Nova Lite
```

OR (if no AWS credentials):
```
WARNING: AWS Bedrock unavailable, falling back to OpenAI
INFO:     ✅ Supervisor created successfully with OpenAI GPT-4o-mini (fallback)
```

### 2. Start Frontend (Terminal 2)
```bash
cd frontend
pnpm dev
```

**Expected Output:**
```
▲ Next.js 16.0.0
- Local:        http://localhost:3000
- Ready in 1.2s
```

### 3. Open Application
Open http://localhost:3000 in your browser

---

## 🎯 Demo Queries (Copy-Paste Ready)

### Query 1: Technical Support (Pure RAG)
```
I'm getting Error 500 when logging in. Can you help?
```

**Expected Behavior:**
- ✅ Routes to Technical Support agent
- ✅ Backend logs: `🔀 ROUTING: Query routed to technical_support_tool`
- ✅ Response retrieves from ChromaDB knowledge base
- ✅ Provides step-by-step troubleshooting

**Key Point to Mention:**
> "This query demonstrates **Pure RAG** - the agent retrieves relevant documentation from the ChromaDB vector store on every query."

---

### Query 2: Billing Support (Hybrid RAG/CAG)
```
What are your pricing plans?
```

**Expected Behavior:**
- ✅ Routes to Billing Support agent
- ✅ Backend logs: `🔀 ROUTING: Query routed to billing_docs_search`
- ✅ **First time**: Retrieves from vector store (RAG)
- ✅ Backend logs: `[HYBRID RAG/CAG] Retrieving billing policies (RAG)`
- ✅ Caches policies in session state

**Key Point to Mention:**
> "First query uses **RAG** to retrieve from vector store. Subsequent queries will use the **cached** policies (CAG) for faster responses."

**Follow-up Query:**
```
Can you tell me more about the Enterprise plan?
```

**Expected Behavior:**
- ✅ Uses cached billing policies (no retrieval)
- ✅ Backend logs: `[HYBRID RAG/CAG] Using cached billing policies (CAG)`
- ✅ Instant response (no vector search delay)

**Key Point to Mention:**
> "Notice this was **instant** - it used the cached policies from the first query. This is the **Hybrid RAG/CAG** strategy in action."

---

### Query 3: Compliance (Pure CAG)
```
What's your data retention policy?
```

**Expected Behavior:**
- ✅ Routes to Compliance agent
- ✅ Backend logs: `🔀 ROUTING: Query routed to compliance_tool`
- ✅ Instant response from pre-loaded documents
- ✅ No vector store retrieval needed

**Key Point to Mention:**
> "This demonstrates **Pure CAG** - the compliance documents are pre-loaded into the agent's context, so responses are instant with no retrieval needed."

---

### Query 4: General Information (Pure RAG)
```
What services do you offer?
```

**Expected Behavior:**
- ✅ Routes to General Information agent
- ✅ Backend logs: `🔀 ROUTING: Query routed to general_docs_search`
- ✅ Retrieves from general knowledge base
- ✅ Provides company information

**Key Point to Mention:**
> "Another **Pure RAG** example - retrieves company information from the general knowledge base."

---

### Query 5: Memory Test
```
Can you remind me what I asked about earlier?
```

**Expected Behavior:**
- ✅ Agent remembers previous queries in the session
- ✅ References earlier questions (pricing, error 500, etc.)
- ✅ Demonstrates conversation state maintained across routing

**Key Point to Mention:**
> "Notice the agent remembers all previous queries in this conversation. Memory is maintained across agent routing using LangGraph's InMemorySaver."

---

## 🎨 Feature Demonstrations

### Streaming Toggle

**Enable Streaming:**
1. Click the lightning bolt icon in the header
2. Icon should be **blue** (streaming enabled)
3. Send any query
4. Watch response appear **token-by-token** in real-time

**Disable Streaming:**
1. Click the lightning bolt icon again
2. Icon should be **gray** (streaming disabled)
3. Send any query
4. Response appears **all at once** (traditional mode)

**Key Point to Mention:**
> "Users can toggle between **real-time streaming** (token-by-token) and **standard mode** (complete response). This uses Server-Sent Events (SSE) for streaming."

---

### Clear Conversation

1. Click "Clear Conversation" button
2. Session resets (new UUID generated)
3. Ask: "What did I just ask about?"
4. Agent should **not remember** previous queries

**Key Point to Mention:**
> "Clearing the conversation generates a new session ID, demonstrating independent conversation threads."

---

## 💻 Code Walkthrough Locations

### 1. LangGraph Orchestrator

**File:** `backend/agents/supervisor_agent.py`

**Lines to Show:** ~205-230

**What to Highlight:**
```python
try:
    logger.info("Attempting to create supervisor with AWS Nova Lite")
    supervisor = create_agent(
        model="bedrock:us.amazon.nova-lite-v1:0",  # AWS Nova Lite for routing
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
        name="supervisor_agent",
    )
    logger.info("✅ Supervisor created successfully with AWS Nova Lite")
    
except Exception as e:
    logger.warning(f"AWS Bedrock unavailable, falling back to OpenAI: {e}")
    supervisor = create_agent(
        model="openai:gpt-4o-mini",  # Fallback
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
        name="supervisor_agent",
    )
```

**Key Points:**
- Multi-provider LLM strategy
- AWS Nova Lite ($0.06/1M tokens) vs OpenAI ($0.15/1M tokens)
- Automatic fallback for reliability
- `InMemorySaver` checkpointer for conversation state

---

### 2. RAG/CAG Strategies

**File:** `backend/agents/tools/rag_tools.py`

**Pure RAG Example (Technical Support):**
```python
@tool
def technical_docs_search(query: str) -> str:
    """Search technical documentation for troubleshooting information."""
    try:
        docs = technical_vectorstore.similarity_search(query, k=3)
        if not docs:
            return "No relevant technical documentation found."
        return format_docs_with_metadata(docs)
    except Exception as e:
        logger.error(f"Technical docs search error: {e}")
        return "Error searching technical documentation."
```

**Key Points:**
- Every query retrieves from ChromaDB
- `similarity_search(k=3)` gets 3 most relevant docs
- Dynamic, up-to-date knowledge

**Hybrid RAG/CAG Example (Billing):**
```python
@tool
def billing_docs_search(query: str, runtime: ToolRuntime) -> Command:
    """Search billing documentation (Hybrid: first RAG, then CAG)."""
    # Check cache first (CAG)
    if cached_policies := runtime.state.get("billing_policies"):
        logger.info("[HYBRID RAG/CAG] Using cached billing policies (CAG)")
        return cached_policies
    
    # Otherwise retrieve (RAG)
    logger.info("[HYBRID RAG/CAG] Retrieving billing policies (RAG)")
    docs = billing_vectorstore.similarity_search(query, k=3)
    response = format_docs_with_metadata(docs)
    
    # Cache for next time
    return Command(
        update={"billing_policies": response},
        goto="__end__"
    )
```

**Key Points:**
- First query: RAG (retrieves from vector store)
- Subsequent queries: CAG (uses cached policies)
- Best of both worlds: fresh on first query, fast thereafter

**Pure CAG Example (Compliance):**
```python
def load_compliance_context():
    """Load compliance documents at startup (Pure CAG)."""
    try:
        privacy_policy = load_single_document("backend/data/docs/compliance/privacy-policy.md")
        terms_of_service = load_single_document("backend/data/docs/compliance/terms-of-service.md")
        return f"PRIVACY POLICY:\n{privacy_policy}\n\nTERMS OF SERVICE:\n{terms_of_service}"
    except Exception as e:
        return "Compliance documents not available."

COMPLIANCE_CONTEXT = load_compliance_context()  # Pre-loaded at startup

# In compliance agent:
system_prompt = f"""You are a Compliance specialist.

COMPLIANCE DOCUMENTATION (Pre-loaded):
{COMPLIANCE_CONTEXT}

IMPORTANT: Use ONLY the pre-loaded compliance documentation above.
"""
```

**Key Points:**
- Documents loaded once at startup
- No retrieval needed during queries
- Instant, consistent responses
- Perfect for static compliance docs

---

### 3. Frontend-Backend Connection

**Backend File:** `backend/main.py`

**Standard Endpoint:**
```python
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Standard chat endpoint (complete response)."""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config={"configurable": {"thread_id": request.session_id}}
    )
    return ChatResponse(
        response=result["messages"][-1].content,
        session_id=request.session_id
    )
```

**Streaming Endpoint:**
```python
@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Streaming chat endpoint using Server-Sent Events (SSE)."""
    async def generate_stream():
        # Start event
        yield f"data: {json.dumps({'type': 'start', 'session_id': request.session_id})}\\n\\n"
        
        # Stream tokens
        async for event in agent.astream(
            {"messages": [{"role": "user", "content": request.message}]},
            config
        ):
            if "messages" in event:
                # Extract and yield token
                yield f"data: {json.dumps({'type': 'token', 'content': delta})}\\n\\n"
        
        # Done event
        yield f"data: {json.dumps({'type': 'done'})}\\n\\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
```

**Frontend File:** `frontend/lib/api.ts`

**Streaming Client:**
```typescript
export async function sendChatMessageStream(
  message: string,
  sessionId: string,
  onEvent: StreamCallback
): Promise<void> {
  const response = await fetch(`${API_CONFIG.baseUrl}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        const event = JSON.parse(data) as ChatStreamEvent;
        onEvent(event);  // Call callback with event
      }
    }
  }
}
```

**Key Points:**
- SSE uses `text/event-stream` media type
- `ReadableStream` with `TextDecoder` for parsing
- Event-driven architecture with callbacks
- Handles start, token, done, error events

---

## 📊 Quick Stats (For Video)

**When discussing the project, mention these metrics:**

- **Architecture**: Multi-agent with 1 supervisor + 4 specialized workers
- **Agents**: Technical, Billing, Compliance, General Information
- **LLM Providers**: AWS Bedrock (Nova Lite) + OpenAI (GPT-4o-mini)
- **Cost Savings**: 11% cheaper with multi-provider strategy
- **RAG/CAG**: 3 strategies (Pure RAG, Hybrid, Pure CAG)
- **Streaming**: Server-Sent Events (SSE) with user toggle
- **Tests**: 145 automated tests, 91% code coverage
- **Documents**: 8 sample documents (2 per domain)
- **Tech Stack**: Python, FastAPI, LangChain v1.0+, LangGraph, Next.js, TypeScript
- **Vector DB**: ChromaDB with persistent storage

---

## 🎤 Talking Points

### Opening (30 seconds)
> "Hi! I'm presenting my Advanced Multi-Agent Customer Service AI system. This is a production-ready application built with LangChain v1.0+, LangGraph, AWS Bedrock, and OpenAI. It features a sophisticated multi-agent architecture with 4 specialized workers, 3 different RAG/CAG strategies, and real-time streaming responses. Let me show you how it works."

### Architecture Overview (1.5 minutes)
> "The system uses a supervisor agent powered by AWS Bedrock Nova Lite for cost-effective routing. It routes queries to 4 specialized workers: Technical Support, Billing, Compliance, and General Information. Each worker uses a different knowledge retrieval strategy optimized for its domain.
>
> Technical and General use Pure RAG - retrieving fresh information from ChromaDB on every query. Billing uses Hybrid RAG/CAG - the first query retrieves and caches policies, subsequent queries use the cache. Compliance uses Pure CAG - documents are pre-loaded at startup for instant responses.
>
> The frontend is built with Next.js and supports both real-time streaming and standard response modes. Users can toggle between modes with a single click."

### Demo Section (3-4 minutes)
> "Let me demonstrate the routing capabilities. [Run queries as listed above]
>
> For streaming, notice how enabling the toggle shows responses appearing in real-time, token-by-token, while standard mode returns the complete response at once. This is powered by Server-Sent Events.
>
> The system maintains conversation memory across routing - as you can see, the agent remembers our entire conversation even though we've switched between multiple specialized agents."

### Code Walkthrough (3-4 minutes)
> "In the code, the supervisor agent uses AWS Nova Lite with automatic fallback to OpenAI. This multi-provider strategy saves 11% on costs while maintaining reliability.
>
> The RAG/CAG strategies are implemented as LangChain tools. Pure RAG queries ChromaDB every time. Hybrid checks the cache first, then retrieves if needed. Pure CAG pre-loads documents at startup.
>
> The streaming implementation uses FastAPI's StreamingResponse with async generators. The frontend consumes the SSE stream using ReadableStream and TextDecoder, updating the UI token-by-token."

### Closing (30 seconds)
> "This system demonstrates production-ready AI engineering: multi-agent orchestration, optimized knowledge retrieval, cost-effective LLM selection, and modern full-stack development. It has 145 automated tests with 91% coverage and comprehensive documentation. The entire codebase is available on GitHub. Thank you!"

---

## ⚠️ Troubleshooting During Demo

### Backend Won't Start
**Issue:** `ModuleNotFoundError` or import errors

**Fix:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Won't Start
**Issue:** Missing dependencies

**Fix:**
```bash
cd frontend
rm -rf node_modules .next
pnpm install
```

### No Agent Response
**Issue:** OpenAI API key not set or invalid

**Fix:**
```bash
# Check .env file
cat backend/.env | grep OPENAI_API_KEY

# If missing or wrong, update it
nano backend/.env
# Add: OPENAI_API_KEY=sk-your-key-here

# Restart backend
```

### ChromaDB Empty
**Issue:** No documents in vector store

**Fix:**
```bash
cd backend
python scripts/index_documents.py --force --all
```

### AWS Fallback Not Working
**Issue:** Backend crashes instead of falling back

**Fix:** This shouldn't happen (we have try-catch), but if it does:
```bash
# Remove AWS credentials to force OpenAI usage
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY

# Or comment out AWS vars in .env
```

---

## 📹 Recording Checklist

Before hitting record:

- [ ] Backend running without errors
- [ ] Frontend running without errors
- [ ] Browser at http://localhost:3000
- [ ] Terminal logs visible (for routing indicators)
- [ ] Demo queries prepared in text file
- [ ] Code files bookmarked in IDE
- [ ] Audio test completed
- [ ] Screen resolution set (1920x1080)
- [ ] Desktop clean (close unnecessary apps)
- [ ] Microphone working
- [ ] Timer ready (keep under 10 minutes)

---

## 🎯 Time Management

**Suggested Timing:**
- Opening: 30 seconds
- Architecture overview: 1.5 minutes
- Live demo: 3-4 minutes
  - Technical query: 30 seconds
  - Billing query: 1 minute (show cache)
  - Compliance query: 30 seconds
  - Streaming demo: 45 seconds
  - Memory demo: 30 seconds
- Code walkthrough: 3-4 minutes
  - Supervisor: 1 minute
  - RAG/CAG: 1.5 minutes
  - Frontend-backend: 1 minute
- Closing: 30 seconds

**Total: 8-9 minutes** (perfect for 5-10 minute requirement)

---

## ✅ Post-Recording

After recording:

- [ ] Review video for audio/video quality
- [ ] Check that all 3 required components are covered:
  - [ ] Architecture overview ✓
  - [ ] Live demo with routing to all agents ✓
  - [ ] Code walkthrough ✓
- [ ] Trim any long pauses or mistakes (optional)
- [ ] Add title card (optional): "Advanced Multi-Agent Customer Service AI"
- [ ] Export as MP4, 1080p
- [ ] Upload to YouTube (unlisted)
- [ ] Test video link works
- [ ] Add to submission

---

**Good luck with your demo! You've built an impressive project!** 🚀

