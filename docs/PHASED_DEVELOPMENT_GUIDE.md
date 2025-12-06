# Phased Development Guide: Advanced Customer Service AI

**Project**: Multi-Agent Customer Service Application  
**Methodology**: Vibe Coding Strategy (Natural Language-Driven, Iterative)  
**Tech Stack**: FastAPI (Backend) + Next.js (Frontend) + LangGraph + ChromaDB

---

## Overview

This guide breaks down the development of the Advanced Customer Service AI into 6 manageable phases. Each phase builds incrementally on the previous one, ensuring we have a working application at every step.

**Key Principle**: Each phase should result in a **working, testable application** before moving to the next phase.

---

## Phase 1: Project Skeleton 🏗️

### Objectives
- Establish basic project structure
- Get frontend and backend communicating
- Verify environment setup

### Deliverables

**Backend (`/backend`)**
- [ ] FastAPI application with basic structure
- [ ] `/chat` endpoint that accepts POST requests with `{ "message": "..." }`
- [ ] Simple echo response (returns user message back)
- [ ] CORS configuration for frontend connection
- [ ] `requirements.txt` with initial dependencies
- [ ] `.env.example` for environment variables

**Frontend (`/frontend`)**
- [ ] Next.js application initialized
- [ ] Basic chat UI component (message list + input field)
- [ ] API call to backend `/chat` endpoint
- [ ] Display of conversation history
- [ ] `package.json` with dependencies

**Documentation**
- [ ] Root `README.md` with setup instructions
- [ ] Environment variable documentation
- [ ] How to run both applications

### Technical Decisions
- **Backend Port**: 8000 (FastAPI default)
- **Frontend Port**: 3000 (Next.js default)
- **API Base URL**: `http://localhost:8000`
- **UI Library**: shadcn/ui (per spec)

### Success Criteria
✅ User can type a message in the frontend  
✅ Message is sent to backend via HTTP POST  
✅ Backend echoes the message back  
✅ Frontend displays both user message and bot response  
✅ Both apps run simultaneously without errors

### Testing
```bash
# Backend test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Expected: {"response": "Echo: Hello"}
```

---

## Phase 2: Simple Agent Foundation 🤖

### Objectives
- Integrate LangChain/LangGraph
- Add real LLM responses (OpenAI)
- Implement conversation memory

### Deliverables

**Backend Updates**
- [ ] LangChain and LangGraph installed
- [ ] Single basic agent using `create_agent()`
- [ ] OpenAI integration (GPT-4 or GPT-4o-mini)
- [ ] Stateful conversation with `InMemorySaver` checkpointer
- [ ] Thread ID management for sessions
- [ ] Replace echo response with LLM-generated response

**Frontend Updates**
- [ ] Session ID generation and persistence
- [ ] Pass session ID to backend for conversation continuity
- [ ] Loading states during API calls
- [ ] Error handling for failed requests

**Environment Variables**
- [ ] `OPENAI_API_KEY` in backend
- [ ] `LANGSMITH_API_KEY` (optional, for debugging)
- [ ] `LANGSMITH_TRACING=true` (optional)

### Technical Decisions
- **Agent Framework**: Use `create_agent()` from `langchain.agents` (v1.0)
- **Model**: OpenAI GPT-4o-mini (cost-effective for development)
- **Memory**: `InMemorySaver` (will upgrade to persistent storage later)
- **Session Management**: UUID-based thread IDs generated on frontend

### Success Criteria
✅ Backend uses real LLM for responses  
✅ Conversation history is maintained across multiple messages  
✅ Agent remembers context from previous messages in same session  
✅ New session starts fresh conversation

### Testing
```python
# Manual test in Python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    system_prompt="You are a helpful customer service assistant.",
    name="test_agent"
)

result = agent.invoke({"messages": [{"role": "user", "content": "Hello!"}]})
print(result["messages"][-1].content)
```

---

## Phase 3: Supervisor + First Worker 👥

### Objectives
- Implement multi-agent architecture
- Add supervisor agent for routing
- Create first specialized worker agent
- Implement tool-calling pattern

### Deliverables

**Backend Updates**
- [ ] Supervisor agent created with routing logic
- [ ] First worker agent: **Technical Support Agent**
- [ ] Wrap worker agent as a tool using `@tool` decorator
- [ ] Supervisor routes queries to worker based on intent
- [ ] System prompts for both supervisor and worker

**Agent Architecture**
```
User Query → Supervisor Agent → [Technical Support Tool] → Response
```

**Technical Support Agent**
- System prompt focused on technical issues
- Simple responses (no RAG yet)
- Tool description guides supervisor when to route

### Technical Decisions
- **Pattern**: Tool-calling (Supervisor pattern) per LangChain v1.0 best practices
- **Supervisor Model**: OpenAI GPT-4o-mini (good at tool selection)
- **Worker Model**: OpenAI GPT-4o-mini (consistent for now)
- **Routing Strategy**: Based on tool descriptions and system prompt

### Success Criteria
✅ Supervisor receives user query  
✅ Supervisor decides to call Technical Support tool  
✅ Worker agent processes query and returns result  
✅ Supervisor formats final response to user  
✅ Conversation maintains context

### Testing Scenarios
1. **Technical Query**: "My app keeps crashing on startup" → Routes to Tech Support
2. **General Query**: "Hello" → Supervisor handles directly
3. **Multi-turn**: Follow-up questions maintain context

---

## Phase 4: Remaining Workers 🔧

### Objectives
- Add remaining specialized agents
- Test routing across all agents
- Ensure clear domain boundaries

### Deliverables

**New Worker Agents**
- [ ] **Billing Support Agent**
  - Handles pricing, invoices, payment questions
  - Tool: `billing_support_tool`
  
- [ ] **Policy & Compliance Agent**
  - Handles ToS, Privacy Policy, compliance questions
  - Tool: `policy_compliance_tool`

**Agent Architecture**
```
User Query → Supervisor Agent → [Technical Support Tool]
                              → [Billing Support Tool]
                              → [Policy Compliance Tool]
                              → Response
```

**Backend Updates**
- [ ] All three worker agents implemented
- [ ] Clear tool descriptions for routing
- [ ] System prompts emphasize final output (sub-agents return complete answers)
- [ ] Test each agent independently before integration

### Technical Decisions
- **Tool Descriptions**: Must be specific enough for supervisor to route correctly
- **Domain Boundaries**: Clear separation (no overlap between agents)
- **Fallback**: Supervisor handles queries that don't fit any agent

### Success Criteria
✅ Supervisor correctly routes to all three agents based on query type  
✅ Each agent provides relevant, domain-specific responses  
✅ No routing confusion or overlap  
✅ Fallback handling for ambiguous queries works

### Testing Scenarios
1. **Technical**: "Error 500 on login" → Tech Support
2. **Billing**: "What's the cost of the Pro plan?" → Billing Support
3. **Policy**: "Can I delete my account data?" → Policy & Compliance
4. **Ambiguous**: "I need help" → Supervisor asks for clarification
5. **Multi-domain**: "Billing issue after technical error" → Supervisor handles or routes to most relevant

---

## Phase 5: RAG/CAG Implementation 📚

### Objectives
- Implement vector database (ChromaDB)
- Create data ingestion pipeline
- Add different retrieval strategies per agent

### Deliverables

**Data Ingestion**
- [ ] `ingest_data.py` script
- [ ] Mock documents for each domain:
  - Technical docs (PDFs, markdown)
  - Billing policies (structured text)
  - Compliance documents (ToS, Privacy Policy)
- [ ] Text splitting and chunking
- [ ] Vector embeddings (OpenAI `text-embedding-3-small`)
- [ ] ChromaDB setup with persistence (`./chroma_db`)

**Retrieval Strategies**

**Technical Support Agent: Pure RAG**
- [ ] Vector search tool for technical knowledge base
- [ ] Agent decides when to search
- [ ] Returns top 3-5 relevant chunks

**Billing Support Agent: Hybrid RAG/CAG**
- [ ] Initial RAG query to fetch billing policies
- [ ] Cache results in session state
- [ ] Subsequent queries use cached context (CAG)

**Policy & Compliance Agent: Pure CAG**
- [ ] Load static documents at startup
- [ ] Inject full context into agent system prompt
- [ ] No runtime retrieval needed

**Backend Updates**
- [ ] ChromaDB integration
- [ ] Create retrieval tools with `@tool` decorator
- [ ] Update agent system prompts to use retrieval
- [ ] Implement caching logic for Billing agent

### Technical Decisions
- **Vector DB**: ChromaDB with local persistence
- **Embeddings**: OpenAI `text-embedding-3-small` (cost-effective)
- **Chunk Size**: 1000 characters with 200 overlap
- **Retrieval**: Top 3 results with similarity score threshold < 1.0
- **Caching**: In-memory session state for Billing agent

### Success Criteria
✅ Data ingestion runs successfully  
✅ Vector database persists across restarts  
✅ Technical agent retrieves relevant docs  
✅ Billing agent caches policy after first query  
✅ Policy agent uses static context consistently  
✅ Retrieval improves answer quality and accuracy

### Testing
```bash
# Ingest data
python ingest_data.py

# Verify ChromaDB
python -c "from langchain_community.vectorstores import Chroma; \
           from langchain_openai import OpenAIEmbeddings; \
           db = Chroma(persist_directory='./chroma_db', \
           embedding_function=OpenAIEmbeddings()); \
           print(f'Documents: {db._collection.count()}')"
```

---

## Phase 6: Multi-Provider LLMs & Polish ✨

### Objectives
- Integrate AWS Bedrock
- Implement response streaming
- Optimize cost and performance
- Final UI/UX improvements

### Deliverables

**AWS Bedrock Integration**
- [ ] AWS Bedrock credentials configured
- [ ] Claude 3 Haiku for supervisor routing (fast, cheap)
- [ ] Optional: AWS Nova Lite/Micro for specific tasks
- [ ] Fallback to OpenAI if Bedrock unavailable

**Model Strategy**
- **Supervisor**: AWS Bedrock Claude 3 Haiku (fast routing)
- **Workers**: OpenAI GPT-4o-mini (quality responses)
- **Embeddings**: OpenAI `text-embedding-3-small`

**Streaming Responses**
- [ ] Backend SSE (Server-Sent Events) endpoint
- [ ] Frontend stream handling
- [ ] Real-time token display as agent responds
- [ ] Graceful fallback if streaming fails

**Frontend Polish**
- [ ] Improved chat UI with agent indicators
- [ ] Show which agent is responding
- [ ] Loading states with agent context
- [ ] Error messages with retry
- [ ] Message timestamps
- [ ] Copy/export conversation
- [ ] Mobile responsive design

**Backend Polish**
- [ ] Logging and monitoring
- [ ] Error handling and retries
- [ ] Rate limiting
- [ ] Health check endpoint
- [ ] API documentation (auto-generated by FastAPI)

### Technical Decisions
- **Streaming Protocol**: SSE (Server-Sent Events)
- **AWS Region**: us-east-1 (or user preference)
- **Model Selection Logic**: Cost-optimize by using Bedrock for routing, OpenAI for generation
- **Error Handling**: Graceful degradation to OpenAI if Bedrock fails

### Success Criteria
✅ Multiple LLM providers working seamlessly  
✅ Streaming responses display in real-time  
✅ UI clearly indicates active agent  
✅ Error handling is robust  
✅ Application is production-ready for demo

### Testing
1. **Multi-provider**: Verify supervisor uses Bedrock, workers use OpenAI
2. **Streaming**: Response tokens appear incrementally
3. **Failover**: Disable Bedrock, verify OpenAI fallback
4. **Load**: Send multiple concurrent requests
5. **Edge cases**: Empty messages, very long messages, special characters

---

## Development Best Practices

### Throughout All Phases

**Git Workflow**
- Commit after each completed phase
- Use conventional commit messages: `feat:`, `fix:`, `docs:`
- Create branches for experimental features
- Tag releases: `v1-skeleton`, `v2-agents`, etc.

**Testing Strategy**
- Manual testing after each feature
- Test endpoints with `curl` or Postman
- Unit tests for critical functions
- Integration tests for agent routing

**Documentation**
- Update README as features are added
- Comment complex logic
- Document environment variables
- Keep `.env.example` current

**LangSmith Tracing**
- Enable for all development: `LANGSMITH_TRACING=true`
- Debug agent routing and tool calls
- Monitor token usage and costs
- View at https://smith.langchain.com/

**Cost Management**
- Start with `gpt-4o-mini` (cheaper than GPT-4)
- Use `text-embedding-3-small` for embeddings
- Monitor usage in OpenAI dashboard
- Set spending limits

---

## Phase Completion Checklist

Before moving to the next phase:

- [ ] All deliverables completed
- [ ] Success criteria met
- [ ] Manual testing passed
- [ ] Code committed to Git
- [ ] README updated
- [ ] Known issues documented
- [ ] Environment variables documented

---

## Troubleshooting Guide

### Common Issues

**Phase 1: Connection Issues**
- Check CORS configuration in FastAPI
- Verify both apps running on correct ports
- Check browser console for errors

**Phase 2: LLM Not Responding**
- Verify `OPENAI_API_KEY` is set
- Check API key permissions and quotas
- Enable LangSmith tracing to debug

**Phase 3-4: Routing Issues**
- Review tool descriptions (must be specific)
- Check supervisor system prompt
- Use LangSmith to see routing decisions
- Test each worker agent independently

**Phase 5: ChromaDB Issues**
- Verify `persist_directory` path
- Use same embedding model for indexing and retrieval
- Check if database files exist
- Re-run ingestion if needed

**Phase 6: Streaming Not Working**
- Check SSE headers are set correctly
- Verify frontend SSE client implementation
- Test with curl to isolate frontend vs backend issues

---

## Final Submission Checklist

Per project specification:

**GitHub Repository**
- [ ] Public repository on GitHub
- [ ] Clean commit history
- [ ] Comprehensive README with setup instructions
- [ ] All code well-documented
- [ ] `.env.example` with all required variables
- [ ] `requirements.txt` and `package.json` up to date

**YouTube Video (5-10 minutes, unlisted)**
- [ ] Architecture overview
- [ ] Live demo of all three agents
- [ ] Show query routing in action
- [ ] Code walkthrough:
  - LangGraph orchestrator
  - Retrieval strategies (RAG/CAG/Hybrid)
  - Frontend-backend connection
- [ ] Upload as unlisted video

**Code Quality**
- [ ] No hardcoded API keys
- [ ] Error handling throughout
- [ ] Logging for debugging
- [ ] Clean, readable code
- [ ] Comments on complex logic

---

## Estimated Timeline

| Phase | Duration | Complexity |
|-------|----------|-----------|
| Phase 1: Skeleton | 2-4 hours | Low |
| Phase 2: Simple Agent | 3-5 hours | Medium |
| Phase 3: Supervisor + Worker | 4-6 hours | Medium-High |
| Phase 4: Remaining Workers | 2-4 hours | Medium |
| Phase 5: RAG/CAG | 6-8 hours | High |
| Phase 6: Multi-Provider & Polish | 4-6 hours | Medium-High |
| **Total** | **21-33 hours** | - |

---

## Resources

### LangChain v1.0 Documentation
- **Agents**: https://docs.langchain.com/oss/python/langchain/agents
- **Multi-Agent**: https://docs.langchain.com/oss/python/langchain/multi-agent
- **Context Engineering**: https://docs.langchain.com/oss/python/langchain/context-engineering
- **RAG**: https://docs.langchain.com/oss/python/langchain/retrieval

### Tools
- **LangSmith**: https://smith.langchain.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
- **shadcn/ui**: https://ui.shadcn.com/

---

## Let's Build! 🚀

You're now ready to start Phase 1. When you're ready to begin, just say **"Go"** or **"Start Phase 1"**!

Remember: We're using **Vibe Coding Strategy** - describe what you want in natural language, and we'll iterate together to build it!

