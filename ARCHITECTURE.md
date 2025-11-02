# Project Architecture: Advanced Customer Service AI

**Project**: Multi-Agent Customer Service Application  
**Version**: 1.0  
**Last Updated**: November 1, 2025  
**Development Methodology**: Vibe Coding Strategy

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Breakdown](#component-breakdown)
4. [Technology Stack](#technology-stack)
5. [Model Strategy](#model-strategy)
6. [Data Flow](#data-flow)
7. [Retrieval Strategies](#retrieval-strategies)
8. [File Structure](#file-structure)
9. [API Specification](#api-specification)
10. [Security & Best Practices](#security--best-practices)
11. [Phase 6 Enhancement: Dynamic Model Selection](#phase-6-enhancement-dynamic-model-selection)

---

## Overview

This project implements a sophisticated, proof-of-concept customer service application powered by a multi-agent AI system. The application demonstrates a modern, scalable architecture for handling diverse customer inquiries by routing them to specialized AI agents.

### Core Capabilities

- **Intelligent Routing**: Supervisor agent analyzes queries and routes to appropriate specialist
- **Specialized Expertise**: Three domain-specific agents (Technical, Billing, Policy)
- **Advanced Retrieval**: Multiple retrieval strategies (RAG, CAG, Hybrid) optimized per agent
- **Multi-Provider LLMs**: Strategic use of AWS Bedrock and OpenAI for cost/performance optimization
- **Stateful Conversations**: Full conversation history and session-specific context
- **Real-time Streaming**: Streaming responses for enhanced user experience

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                       (Next.js Frontend)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ Chat Input   │  │ Message List │  │ Agent Status Indicator   │ │
│  │ Component    │  │ Component    │  │ Component                │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP POST/GET
                             │ /chat, /stream (SSE)
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                       API LAYER                              │  │
│  │   POST /chat    │    GET /stream    │    GET /health        │  │
│  └───────────────────────┬──────────────────────────────────────┘  │
│                          │                                          │
│  ┌───────────────────────▼──────────────────────────────────────┐  │
│  │               LANGGRAPH ORCHESTRATOR                         │  │
│  │              (Stateful Agent System)                         │  │
│  │                                                              │  │
│  │  ┌────────────────────────────────────────────────────────┐ │  │
│  │  │              SUPERVISOR AGENT                          │ │  │
│  │  │        (AWS Bedrock Nova Lite - Baseline)              │ │  │
│  │  │   Phase 6: Dynamic Nova Lite ↔ Claude 3.5 Haiku       │ │  │
│  │  │                                                        │ │  │
│  │  │  • Analyzes user query intent                         │ │  │
│  │  │  • Routes to appropriate worker agent                 │ │  │
│  │  │  • Formats final response to user                     │ │  │
│  │  └──────────────┬──────────────┬─────────────┬──────────┘ │  │
│  │                 │              │             │            │  │
│  │        Tool Call│     Tool Call│    Tool Call│            │  │
│  │                 ▼              ▼             ▼            │  │
│  │  ┌─────────────────┐ ┌──────────────┐ ┌───────────────┐ │  │
│  │  │  Technical      │ │  Billing     │ │  Policy &     │ │  │
│  │  │  Support Agent  │ │  Support     │ │  Compliance   │ │  │
│  │  │  (GPT-5)        │ │  Agent       │ │  Agent        │ │  │
│  │  │                 │ │  (GPT-5)     │ │  (GPT-5)      │ │  │
│  │  │  Strategy:      │ │  Strategy:   │ │  Strategy:    │ │  │
│  │  │  Pure RAG       │ │  Hybrid      │ │  Pure CAG     │ │  │
│  │  │  (Always search)│ │  RAG/CAG     │ │  (Static)     │ │  │
│  │  └────────┬────────┘ └──────┬───────┘ └──────┬────────┘ │  │
│  │           │                  │                │          │  │
│  └───────────┼──────────────────┼────────────────┼──────────┘  │
│              │                  │                │              │
│       Vector │           Vector │ + Session      │ Static       │
│       Search │             Search│ Cache          │ Context      │
│              ▼                  ▼                ▼              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │             RETRIEVAL & STORAGE LAYER                    │  │
│  │                                                          │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │  │
│  │  │  ChromaDB   │  │  Session     │  │  Static        │ │  │
│  │  │ (Persistent)│  │  Cache       │  │  Documents     │ │  │
│  │  │             │  │  (In-Memory) │  │  (Pre-loaded)  │ │  │
│  │  │ • Tech docs │  │              │  │  • ToS         │ │  │
│  │  │ • Bug logs  │  │ • Billing    │  │  • Privacy     │ │  │
│  │  │ • Forums    │  │   policies   │  │  • Guidelines  │ │  │
│  │  └─────────────┘  └──────────────┘  └────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

External Services:
  • OpenAI API (GPT-5, text-embedding-3-small)
  • AWS Bedrock (Nova Lite, optional Claude 3.5 Haiku)
  • LangSmith (optional observability)
```

### Architecture Principles

1. **Separation of Concerns**: Each agent has a single, well-defined responsibility
2. **Scalability**: Modular design allows easy addition of new agents
3. **Cost Optimization**: Strategic model selection based on task requirements
4. **Stateful Design**: Conversation history and session context maintained
5. **Performance**: Fast routing with Nova Lite, quality responses with GPT-5

---

## Component Breakdown

### 1. Frontend Layer (Next.js)

**Location**: `/frontend`

#### Core Components

**ChatInterface.js** - Main Container
- Manages overall chat application state
- Coordinates message flow between components
- Handles session management (UUID generation and persistence)
- Error boundary and loading states

**MessageList.js** - Conversation Display
- Renders message history
- Differentiates user vs AI messages
- Shows agent attribution ("Answered by Technical Support")
- Auto-scrolls to latest message
- Timestamps for each message

**MessageInput.js** - User Input
- Text input field with submit button
- Enter key to send message
- Disable input during API calls
- Character count/limit (optional)

**AgentIndicator.js** - Status Display
- Shows which agent is active
- Loading indicator during processing
- Visual feedback for streaming responses
- Agent-specific icons/colors

#### State Management
```javascript
// Session state
const [sessionId, setSessionId] = useState(null);  // UUID for thread
const [messages, setMessages] = useState([]);      // Conversation history
const [isLoading, setIsLoading] = useState(false); // API call status
const [activeAgent, setActiveAgent] = useState(null); // Current agent
```

#### API Communication
```javascript
// API client (lib/api.js)
export async function sendMessage(message, sessionId) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId })
  });
  return response.json();
}
```

---

### 2. API Layer (FastAPI)

**Location**: `/backend/main.py`

#### Endpoints

**POST /chat**
```python
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint for user messages.
    
    Input: { "message": str, "session_id": str }
    Output: { "response": str, "agent_used": str, "session_id": str }
    """
    result = await orchestrator.process_message(
        message=request.message,
        session_id=request.session_id
    )
    return result
```

**GET /stream** (Phase 6)
```python
@app.get("/stream")
async def stream_endpoint(message: str, session_id: str):
    """
    Server-Sent Events endpoint for streaming responses.
    
    Yields: data: {"token": str, "agent": str, "done": bool}
    """
    async for chunk in orchestrator.stream_message(message, session_id):
        yield f"data: {json.dumps(chunk)}\n\n"
```

**GET /health**
```python
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "models": ["nova-lite", "gpt-5"],
        "vector_db": vectorstore.is_connected()
    }
```

#### Request Validation
```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(..., regex="^[a-f0-9-]{36}$")  # UUID format
```

#### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 3. Orchestration Layer (LangGraph)

**Location**: `/backend/agents/orchestrator.py`

#### Supervisor Agent (Baseline: Phases 1-5)

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Initialize checkpointer for conversation memory
checkpointer = InMemorySaver()

# Create supervisor agent with tool-calling pattern
supervisor = create_agent(
    model="bedrock:amazon.nova-lite-v1:0",
    tools=[
        technical_support_tool,
        billing_support_tool,
        policy_compliance_tool
    ],
    system_prompt="""You are a customer service supervisor agent.

Your role is to analyze user queries and route them to the appropriate 
specialist agent using the available tools:

- technical_support_tool: For bugs, errors, technical issues, crashes
- billing_support_tool: For pricing, invoices, payments, subscriptions
- policy_compliance_tool: For ToS, privacy, data policies, legal questions

Analyze the query carefully and call the most appropriate tool. If a query 
is ambiguous, ask the user for clarification.

After receiving the specialist's response, format it appropriately and 
present it to the user.""",
    checkpointer=checkpointer,
    name="supervisor"
)
```

#### Orchestrator Class

```python
class AgentOrchestrator:
    """Manages the multi-agent workflow."""
    
    def __init__(self):
        self.supervisor = supervisor
        self.checkpointer = checkpointer
    
    async def process_message(self, message: str, session_id: str) -> dict:
        """
        Process a user message through the agent system.
        
        Args:
            message: User's message text
            session_id: Unique session identifier (thread_id)
            
        Returns:
            dict: Response with answer and metadata
        """
        # Configuration with thread ID for conversation memory
        config = {"configurable": {"thread_id": session_id}}
        
        # Invoke supervisor agent
        result = self.supervisor.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config
        )
        
        # Extract final response
        response = result["messages"][-1].content
        
        # Determine which agent was used (from tool calls)
        agent_used = self._extract_agent_used(result)
        
        return {
            "response": response,
            "agent_used": agent_used,
            "session_id": session_id
        }
    
    def _extract_agent_used(self, result: dict) -> str:
        """Determine which worker agent handled the query."""
        messages = result.get("messages", [])
        for msg in reversed(messages):
            if msg.get("type") == "tool":
                tool_name = msg.get("name", "")
                if "technical" in tool_name:
                    return "Technical Support"
                elif "billing" in tool_name:
                    return "Billing Support"
                elif "policy" in tool_name:
                    return "Policy & Compliance"
        return "General Support"
```

---

### 4. Worker Agents Layer

**Location**: `/backend/agents/workers/`

#### Technical Support Agent (Pure RAG)

**File**: `technical_support_agent.py`

**Strategy**: Always searches the vector database for current, dynamic information.

```python
from langchain.tools import tool
from langchain.agents import create_agent
from backend.data.vector_store import vectorstore

@tool
def technical_support_tool(query: str) -> str:
    """
    Handle technical support questions about bugs, errors, and technical issues.
    
    Use this tool for:
    - Application crashes or errors
    - Technical troubleshooting
    - Bug reports and known issues
    - System requirements
    - Installation problems
    """
    # RAG Strategy: Always search vector database
    docs = vectorstore.similarity_search(
        query,
        k=3,
        filter={"category": "technical"}  # Filter to technical docs only
    )
    
    # Format retrieved documents as context
    context = "\n\n".join([
        f"Document {i+1}:\n{doc.page_content}"
        for i, doc in enumerate(docs)
    ])
    
    # Create specialized agent with retrieved context
    agent = create_agent(
        model="openai:gpt-5",
        tools=[],
        system_prompt=f"""You are a technical support specialist.

Use the following technical documentation to answer the user's question:

{context}

Provide clear, step-by-step solutions. If the documentation doesn't contain 
the answer, say so honestly and suggest alternative resources.

IMPORTANT: The supervisor only sees your final message. Include ALL findings,
solutions, and relevant details in your response.""",
        name="technical_support"
    )
    
    # Generate response
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    return result["messages"][-1].content
```

---

#### Billing Support Agent (Hybrid RAG/CAG)

**File**: `billing_support_agent.py`

**Strategy**: First query fetches policies via RAG, then caches for session (CAG).

```python
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.agents import create_agent
from backend.data.vector_store import vectorstore

@tool
def billing_support_tool(query: str, runtime: ToolRuntime) -> Command:
    """
    Handle billing and pricing questions.
    
    Use this tool for:
    - Pricing and plans
    - Invoice questions
    - Payment issues
    - Subscription management
    - Refunds and credits
    """
    # Hybrid Strategy: Check if billing policies are cached in session
    billing_cache = runtime.state.get("billing_cache")
    
    if not billing_cache:
        # First query: Fetch from vector database (RAG)
        docs = vectorstore.similarity_search(
            "billing policies pricing plans invoices payments",
            k=5,
            filter={"category": "billing"}
        )
        
        # Cache the policies for this session
        billing_cache = "\n\n".join([
            f"Policy {i+1}:\n{doc.page_content}"
            for i, doc in enumerate(docs)
        ])
    
    # Create agent with cached policies (CAG)
    agent = create_agent(
        model="openai:gpt-5",
        tools=[],
        system_prompt=f"""You are a billing support specialist.

Use the following billing policies to answer questions:

{billing_cache}

Provide accurate pricing information, explain billing cycles, and help 
resolve payment issues. Be clear about refund policies and subscription terms.

CRITICAL: The supervisor only sees your final message. Include ALL relevant
pricing details, policy information, and answers in your final response.""",
        name="billing_support"
    )
    
    # Generate response
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    # Return result and update session cache
    return Command(
        update={"billing_cache": billing_cache},
        result=result["messages"][-1].content
    )
```

---

#### Policy & Compliance Agent (Pure CAG)

**File**: `policy_compliance_agent.py`

**Strategy**: Static documents loaded at startup, injected into system prompt.

```python
from langchain.tools import tool
from langchain.agents import create_agent
from pathlib import Path

# Load static policy documents at module initialization
def load_policy_documents():
    """Load all policy documents at startup."""
    docs_path = Path(__file__).parent.parent.parent / "data" / "docs" / "compliance"
    
    documents = []
    for file_path in docs_path.glob("*.txt"):
        with open(file_path, 'r') as f:
            content = f.read()
            documents.append(f"Document: {file_path.name}\n{content}")
    
    return "\n\n" + "="*80 + "\n\n".join(documents)

# Load once at startup (CAG - Context Augmented Generation)
POLICY_DOCUMENTS = load_policy_documents()

@tool
def policy_compliance_tool(query: str) -> str:
    """
    Handle policy and compliance questions.
    
    Use this tool for:
    - Terms of Service questions
    - Privacy Policy
    - Data handling and GDPR
    - Compliance and legal questions
    - Account deletion requests
    """
    # CAG Strategy: All context in system prompt (no runtime retrieval)
    agent = create_agent(
        model="openai:gpt-5",
        tools=[],
        system_prompt=f"""You are a policy and compliance specialist.

Use the following official policy documents to answer questions:

{POLICY_DOCUMENTS}

Provide accurate, authoritative answers based strictly on these documents.
For legal questions, remind users to consult legal counsel for specific advice.

IMPORTANT: The supervisor only sees your final message. Include the complete
answer with all relevant policy details in your final response.""",
        name="policy_compliance"
    )
    
    # Generate response
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    return result["messages"][-1].content
```

---

### 5. Data & Retrieval Layer

**Location**: `/backend/data/`

#### Vector Store Setup

**File**: `vector_store.py`

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from pathlib import Path

# Initialize embeddings model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536
)

# Initialize persistent ChromaDB
CHROMA_PATH = Path(__file__).parent.parent / "chroma_db"

vectorstore = Chroma(
    persist_directory=str(CHROMA_PATH),
    embedding_function=embeddings,
    collection_name="customer_service_kb"
)

def get_vectorstore():
    """Get the initialized vector store instance."""
    return vectorstore
```

#### Data Ingestion Pipeline

**File**: `ingest_data.py`

```python
"""
Data ingestion pipeline for processing mock documents and loading into ChromaDB.

Usage:
    python -m backend.data.ingest_data
"""

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.data.vector_store import vectorstore
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_documents():
    """Load all documents from the docs directory."""
    docs_path = Path(__file__).parent / "docs"
    documents = []
    
    # Load technical documents
    tech_path = docs_path / "technical"
    for pdf_file in tech_path.glob("*.pdf"):
        logger.info(f"Loading {pdf_file.name}")
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()
        # Add metadata
        for doc in docs:
            doc.metadata["category"] = "technical"
            doc.metadata["source_file"] = pdf_file.name
        documents.extend(docs)
    
    for md_file in tech_path.glob("*.md"):
        logger.info(f"Loading {md_file.name}")
        loader = UnstructuredMarkdownLoader(str(md_file))
        docs = loader.load()
        for doc in docs:
            doc.metadata["category"] = "technical"
            doc.metadata["source_file"] = md_file.name
        documents.extend(docs)
    
    # Load billing documents
    billing_path = docs_path / "billing"
    for txt_file in billing_path.glob("*.txt"):
        logger.info(f"Loading {txt_file.name}")
        loader = TextLoader(str(txt_file))
        docs = loader.load()
        for doc in docs:
            doc.metadata["category"] = "billing"
            doc.metadata["source_file"] = txt_file.name
        documents.extend(docs)
    
    logger.info(f"Loaded {len(documents)} documents")
    return documents

def split_documents(documents):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split into {len(chunks)} chunks")
    return chunks

def ingest():
    """Main ingestion function."""
    logger.info("Starting data ingestion...")
    
    # Load documents
    documents = load_documents()
    
    # Split into chunks
    chunks = split_documents(documents)
    
    # Add to vector store
    logger.info("Adding chunks to ChromaDB...")
    vectorstore.add_documents(chunks)
    
    # Verify
    count = vectorstore._collection.count()
    logger.info(f"Ingestion complete. Total documents in DB: {count}")

if __name__ == "__main__":
    ingest()
```

---

## Technology Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | FastAPI | 0.104+ | High-performance async API |
| Agent Framework | LangChain | 1.0+ | Agent creation and tooling |
| Orchestration | LangGraph | 1.0+ | Multi-agent workflow |
| Vector DB | ChromaDB | 0.4+ | Embeddings storage |
| Text Splitting | LangChain Splitters | 1.0+ | Document chunking |
| Python | Python | 3.11+ | Runtime environment |

### Frontend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Next.js | 14+ | React framework |
| UI Components | shadcn/ui | Latest | Modern component library |
| Styling | Tailwind CSS | 3+ | Utility-first CSS |
| State Management | React Hooks | - | Client state |
| HTTP Client | Fetch API | - | Backend communication |

### LLM Providers
| Provider | Model | Purpose | Cost |
|----------|-------|---------|------|
| AWS Bedrock | **Nova Lite** | Supervisor routing (Baseline) | $0.00006 / 1K input |
| AWS Bedrock | Claude 3.5 Haiku | Supervisor routing (Phase 6) | $0.0008 / 1K input |
| OpenAI | **GPT-5** | Worker agent responses | Premium |
| OpenAI | text-embedding-3-small | Vector embeddings | $0.00002 / 1K tokens |

### Development Tools
| Tool | Purpose |
|------|---------|
| LangSmith | Agent tracing and debugging |
| Git | Version control |
| Docker | Containerization (optional) |
| pytest | Backend testing |
| Jest | Frontend testing |

---

## Model Strategy

### Baseline Architecture (Phases 1-5)

```
Supervisor Agent: AWS Bedrock Nova Lite
├─ Rationale: Ultra-fast routing, 13x cheaper than alternatives
├─ Cost: $0.00006 per 1K input tokens
├─ Latency: Ultra-low
└─ Sufficient for straightforward routing decisions

Worker Agents: OpenAI GPT-5
├─ Rationale: Highest quality customer-facing responses
├─ Features: Enhanced reasoning, conversation continuity
└─ Use: Where response quality directly impacts user experience
```

### Why This Strategy?

**Cost Optimization**
- Supervisor invoked on **every message** → use cheapest effective model
- Workers invoked **selectively** → justify premium model cost
- Estimated cost: ~$0.01 per customer conversation

**Performance Optimization**
- Nova Lite: Ultra-low latency routing (~100-200ms)
- GPT-5: High-quality responses worth the wait (~1-2s)
- Total response time: Competitive with single-model approaches

**Quality Where It Matters**
- Routing decisions are simple: "Which agent?"
- Customer responses are complex: Require reasoning, empathy, accuracy
- Premium model (GPT-5) allocated to high-impact component

---

## Data Flow

### Typical User Query Flow

```
1. USER ACTION
   User types: "My app keeps crashing on startup"
   └─> Frontend generates/retrieves session_id (UUID)
       └─> POST /chat { message: "...", session_id: "..." }

2. API LAYER
   FastAPI receives request
   └─> Validates input (Pydantic)
       └─> Invokes AgentOrchestrator.process_message()

3. ORCHESTRATOR
   Creates config with thread_id for memory
   └─> config = { "configurable": { "thread_id": session_id } }
       └─> Invokes supervisor.invoke(messages, config)

4. SUPERVISOR AGENT (Nova Lite)
   Analyzes query: "app crash" = technical issue
   └─> Decides to call technical_support_tool
       └─> Tool call: technical_support_tool("My app keeps crashing...")

5. TECHNICAL SUPPORT WORKER (GPT-5)
   └─> Searches ChromaDB vector store
       └─> query="app crash startup"
           └─> Retrieves top 3 relevant documents
               └─> Injects context into agent system prompt
                   └─> GPT-5 generates answer using context
                       └─> Returns: "Try these steps: 1. Clear cache..."

6. SUPERVISOR RECEIVES RESULT
   └─> Formats worker's response
       └─> Returns to user: "Technical Support says: Try these steps..."

7. RESPONSE FLOWS BACK
   Orchestrator → FastAPI → Frontend → User
   └─> Frontend displays:
       - Message from "Technical Support"
       - Agent indicator shows technical agent icon
       - Message added to conversation history

8. CONVERSATION CONTINUITY
   Next message: "That didn't work"
   └─> Same session_id used
       └─> LangGraph loads previous messages from checkpointer
           └─> Supervisor has full context
               └─> Can follow up intelligently
```

### Session State Management

```python
# State is maintained per thread_id (session_id)
{
    "thread_id": "uuid-here",
    "messages": [
        {"role": "user", "content": "My app crashes"},
        {"role": "assistant", "content": "Try clearing cache..."},
        {"role": "user", "content": "That didn't work"},
        # ... conversation continues
    ],
    "billing_cache": "Billing policies...",  # Cached by Billing agent
    # Other session-specific data
}
```

---

## Retrieval Strategies

### Strategy Comparison

| Agent | Strategy | When Retrieves | Persistence | Best For |
|-------|----------|---------------|-------------|----------|
| **Technical Support** | Pure RAG | Every query | None (always fresh) | Dynamic, frequently updated knowledge |
| **Billing Support** | Hybrid RAG/CAG | First query only | Session cache | Static within session, updated periodically |
| **Policy & Compliance** | Pure CAG | At startup | Application lifetime | Completely static documents |

### Technical Support: Pure RAG

**Why?**
- Technical knowledge changes frequently (new bugs, updates, patches)
- Users need most current information
- Queries are specific and varied

**Implementation:**
```python
def technical_support(query):
    # Always search (RAG)
    docs = vectorstore.similarity_search(query, k=3)
    context = format_docs(docs)
    return generate_with_context(context, query)
```

**Trade-offs:**
- ✅ Always current
- ✅ Handles diverse queries
- ❌ Slower (search on every query)
- ❌ Higher cost (embeddings API calls)

---

### Billing Support: Hybrid RAG/CAG

**Why?**
- Billing policies are stable within a session
- First query fetches comprehensive policies
- Subsequent queries reuse cached policies (faster, cheaper)

**Implementation:**
```python
def billing_support(query, session_cache):
    if not session_cache:
        # First query: RAG
        docs = vectorstore.similarity_search("billing policies", k=5)
        session_cache = format_docs(docs)
    
    # All queries: CAG with cache
    return generate_with_context(session_cache, query)
```

**Trade-offs:**
- ✅ Fast after first query
- ✅ Cost-effective
- ✅ Comprehensive context
- ⚠️ Cache might be stale (acceptable for policies)

---

### Policy & Compliance: Pure CAG

**Why?**
- Policy documents are completely static
- Same for all users and sessions
- Can load once at startup

**Implementation:**
```python
# Load at startup
POLICY_DOCS = load_all_policies()

def policy_compliance(query):
    # No retrieval - use pre-loaded context (CAG)
    return generate_with_context(POLICY_DOCS, query)
```

**Trade-offs:**
- ✅ Fastest (no retrieval)
- ✅ No per-query costs
- ✅ Completely consistent
- ❌ Limited context window (must fit all policies)
- ❌ Requires app restart to update

---

## File Structure

```
Agentic_Customer_Project1/
│
├── backend/
│   ├── main.py                          # FastAPI app, API endpoints
│   ├── requirements.txt                 # Python dependencies
│   ├── .env                             # Environment variables (gitignored)
│   ├── .env.example                     # Template for environment setup
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py              # AgentOrchestrator class, supervisor
│   │   │
│   │   └── workers/
│   │       ├── __init__.py
│   │       ├── technical_support_agent.py    # Technical agent + tool
│   │       ├── billing_support_agent.py      # Billing agent + tool
│   │       └── policy_compliance_agent.py    # Policy agent + tool
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── vector_store.py              # ChromaDB initialization
│   │   ├── ingest_data.py               # Data ingestion script
│   │   │
│   │   └── docs/                        # Mock documents for ingestion
│   │       ├── technical/
│   │       │   ├── user_manual.pdf
│   │       │   ├── troubleshooting_guide.md
│   │       │   ├── known_bugs.md
│   │       │   └── forum_posts.txt
│   │       │
│   │       ├── billing/
│   │       │   ├── pricing_plans.txt
│   │       │   ├── invoice_faq.txt
│   │       │   └── payment_policies.txt
│   │       │
│   │       └── compliance/
│   │           ├── terms_of_service.txt
│   │           ├── privacy_policy.txt
│   │           └── data_handling_guidelines.txt
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py                    # Configuration management
│   │   └── logger.py                    # Logging setup
│   │
│   ├── tests/
│   │   ├── test_orchestrator.py
│   │   ├── test_workers.py
│   │   └── test_api.py
│   │
│   └── chroma_db/                       # ChromaDB persistence (gitignored)
│       └── [vector database files]
│
├── frontend/
│   ├── package.json                     # NPM dependencies
│   ├── package-lock.json
│   ├── next.config.js                   # Next.js configuration
│   ├── tailwind.config.js               # Tailwind CSS configuration
│   ├── .env.local                       # Frontend env vars (gitignored)
│   ├── .env.example
│   │
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.js                  # Main chat page
│   │   │   ├── layout.js                # Root layout
│   │   │   └── globals.css              # Global styles
│   │   │
│   │   ├── components/
│   │   │   ├── ChatInterface.js         # Main chat container
│   │   │   ├── MessageList.js           # Message display component
│   │   │   ├── MessageInput.js          # Input field component
│   │   │   ├── AgentIndicator.js        # Agent status indicator
│   │   │   └── ui/                      # shadcn/ui components
│   │   │       ├── button.js
│   │   │       ├── card.js
│   │   │       └── [other ui components]
│   │   │
│   │   └── lib/
│   │       ├── api.js                   # Backend API client
│   │       └── utils.js                 # Helper functions
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── assets/
│   │       └── agent-icons/             # Icons for each agent
│   │
│   └── tests/
│       └── [frontend tests]
│
├── docs/
│   ├── ARCHITECTURE.md                  # This document
│   ├── PHASED_DEVELOPMENT_GUIDE.md      # Development roadmap
│   ├── API_DOCUMENTATION.md             # API reference
│   └── DEPLOYMENT.md                    # Deployment instructions
│
├── .gitignore                           # Git ignore rules
├── README.md                            # Project overview & setup
└── agentic-customer-specs.md            # Original specification
```

---

## API Specification

### POST /chat

**Endpoint**: `POST http://localhost:8000/chat`

**Request Body**:
```json
{
  "message": "How much does the Pro plan cost?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Request Schema**:
```python
class ChatRequest(BaseModel):
    message: str          # User message (1-2000 chars)
    session_id: str       # UUID v4 format
```

**Response**:
```json
{
  "response": "The Pro plan costs $29.99/month or $299/year...",
  "agent_used": "Billing Support",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Status Codes**:
- `200 OK`: Successful response
- `400 Bad Request`: Invalid input (malformed UUID, empty message)
- `500 Internal Server Error`: Server error

---

### GET /stream (Phase 6)

**Endpoint**: `GET http://localhost:8000/stream?message=...&session_id=...`

**Query Parameters**:
- `message`: URL-encoded user message
- `session_id`: UUID for session

**Response**: Server-Sent Events (SSE)

**Event Format**:
```
data: {"token": "The", "agent": "Technical Support", "done": false}
data: {"token": " Pro", "agent": "Technical Support", "done": false}
data: {"token": " plan", "agent": "Technical Support", "done": false}
...
data: {"token": "", "agent": "Technical Support", "done": true}
```

---

### GET /health

**Endpoint**: `GET http://localhost:8000/health`

**Response**:
```json
{
  "status": "healthy",
  "models": {
    "supervisor": "amazon.nova-lite-v1:0",
    "workers": "gpt-5"
  },
  "vector_db": {
    "connected": true,
    "document_count": 156
  },
  "timestamp": "2025-11-01T12:00:00Z"
}
```

---

## Security & Best Practices

### Environment Variables

**Backend (.env)**:
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...

# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# LangSmith (Optional)
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=customer-service-ai

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Frontend (.env.local)**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Security Considerations

**1. API Keys**
- ✅ Never commit `.env` files
- ✅ Use `.env.example` as template
- ✅ Rotate keys regularly
- ✅ Use separate keys for dev/prod

**2. Input Validation**
```python
# Pydantic validation prevents injection
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(..., regex="^[a-f0-9-]{36}$")
```

**3. Rate Limiting** (Consider adding in production)
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: ChatRequest):
    ...
```

**4. CORS Configuration**
```python
# Development: Allow localhost
allow_origins=["http://localhost:3000"]

# Production: Restrict to your domain
allow_origins=["https://yourdomain.com"]
```

---

## Phase 6 Enhancement: Dynamic Model Selection

### Overview

In **Phase 6**, we add intelligent model selection for the supervisor agent. Simple queries use Nova Lite (fast, cheap), while complex queries use Claude 3.5 Haiku (better reasoning).

### Implementation

**File**: `/backend/agents/orchestrator.py`

#### 1. Complexity Analyzer

```python
from typing import List
from langchain_core.messages import BaseMessage

def analyze_query_complexity(messages: List[BaseMessage]) -> float:
    """
    Analyze query complexity to determine which model to use.
    
    Returns:
        float: Complexity score from 0.0 (simple) to 1.0 (complex)
    """
    if not messages:
        return 0.0
    
    # Get last user message
    user_message = messages[-1].content if messages else ""
    
    complexity_score = 0.0
    
    # Factor 1: Message length (longer = potentially more complex)
    word_count = len(user_message.split())
    if word_count > 50:
        complexity_score += 0.2
    elif word_count > 100:
        complexity_score += 0.4
    
    # Factor 2: Question words (multiple questions = more complex)
    question_words = ['what', 'why', 'how', 'when', 'where', 'who']
    question_count = sum(1 for word in question_words if word in user_message.lower())
    if question_count >= 2:
        complexity_score += 0.2
    
    # Factor 3: Conditional language (if/then, either/or = more complex)
    conditionals = ['if', 'but', 'however', 'although', 'unless', 'either']
    if any(cond in user_message.lower() for cond in conditionals):
        complexity_score += 0.2
    
    # Factor 4: Ambiguous/vague language
    vague_indicators = ['maybe', 'not sure', 'kind of', 'sort of', 'unclear']
    if any(vague in user_message.lower() for vague in vague_indicators):
        complexity_score += 0.3
    
    # Factor 5: Conversation history length (long conversations = more context)
    if len(messages) > 10:
        complexity_score += 0.1
    
    return min(complexity_score, 1.0)  # Cap at 1.0
```

#### 2. Dynamic Model Selection Middleware

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
import logging

logger = logging.getLogger(__name__)

# Complexity threshold for model selection
COMPLEXITY_THRESHOLD = 0.6

@wrap_model_call
def dynamic_model_selection(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """
    Dynamically select between Nova Lite and Claude 3.5 Haiku based on query complexity.
    
    Simple queries (< threshold): Use Nova Lite (fast, cheap)
    Complex queries (>= threshold): Use Claude 3.5 Haiku (better reasoning)
    """
    # Analyze complexity
    complexity = analyze_query_complexity(request.messages)
    
    # Select model based on complexity
    if complexity < COMPLEXITY_THRESHOLD:
        model = "bedrock:amazon.nova-lite-v1:0"
        reasoning = "simple routing"
    else:
        model = "bedrock:anthropic.claude-3-5-haiku"
        reasoning = "complex query requiring advanced reasoning"
    
    # Log decision (useful for debugging and metrics)
    logger.info(
        f"Model selection: {model} "
        f"(complexity: {complexity:.2f}, reason: {reasoning})"
    )
    
    # Override model in request
    request = request.override(model=model)
    
    # Call handler with updated request
    return handler(request)
```

#### 3. Updated Supervisor Agent

```python
# Create supervisor with dynamic model selection middleware
supervisor = create_agent(
    model="bedrock:amazon.nova-lite-v1:0",  # Default model
    tools=[
        technical_support_tool,
        billing_support_tool,
        policy_compliance_tool
    ],
    middleware=[dynamic_model_selection],  # ← Add middleware here
    system_prompt="""You are a customer service supervisor agent.

Your role is to analyze user queries and route them to the appropriate 
specialist agent using the available tools:

- technical_support_tool: For bugs, errors, technical issues, crashes
- billing_support_tool: For pricing, invoices, payments, subscriptions
- policy_compliance_tool: For ToS, privacy, data policies, legal questions

Analyze the query carefully and call the most appropriate tool. If a query 
is ambiguous, ask the user for clarification.

After receiving the specialist's response, format it appropriately and 
present it to the user.""",
    checkpointer=checkpointer,
    name="supervisor"
)
```

### Complexity Score Examples

| Query | Complexity Score | Model Selected | Reasoning |
|-------|-----------------|----------------|-----------|
| "How much is Pro?" | 0.0 | Nova Lite | Short, direct question |
| "My app crashes" | 0.0 | Nova Lite | Simple technical query |
| "Can I delete my account?" | 0.0 | Nova Lite | Straightforward policy question |
| "If I upgrade mid-month, how is billing prorated?" | 0.4 | Nova Lite | Conditional but clear |
| "I'm not sure if my issue is billing or technical, kind of both" | 0.7 | Claude 3.5 Haiku | Ambiguous, needs reasoning |
| "What happens if I cancel but then want to resubscribe?" | 0.6 | Claude 3.5 Haiku | Multiple conditionals |
| "Why did my payment fail and how do I fix it?" | 0.4 | Nova Lite | Two questions but clear domain |

### Monitoring and Metrics

Add logging to track model selection patterns:

```python
class ModelSelectionMetrics:
    """Track model usage for cost and performance analysis."""
    
    def __init__(self):
        self.nova_count = 0
        self.claude_count = 0
        self.complexity_scores = []
    
    def record(self, model: str, complexity: float):
        if "nova" in model:
            self.nova_count += 1
        else:
            self.claude_count += 1
        self.complexity_scores.append(complexity)
    
    def summary(self):
        total = self.nova_count + self.claude_count
        avg_complexity = sum(self.complexity_scores) / len(self.complexity_scores)
        
        return {
            "total_queries": total,
            "nova_lite_pct": (self.nova_count / total) * 100,
            "claude_pct": (self.claude_count / total) * 100,
            "avg_complexity": avg_complexity,
            "cost_savings_vs_all_claude": self._calculate_savings()
        }
```

### Benefits of Dynamic Selection

**Cost Optimization**
- Estimated 70-80% of queries use Nova Lite (13-16x cheaper)
- Only pay premium for queries that need it
- Typical savings: 10-12x vs all-Claude approach

**Performance**
- Nova Lite: ~100-200ms routing
- Claude: ~300-500ms routing
- Most queries get ultra-fast routing

**Quality**
- Complex queries get better reasoning
- Simple queries don't need it (Nova Lite sufficient)
- Best of both worlds

**Scalability**
- Easy to adjust threshold based on metrics
- Can add more sophisticated complexity analysis
- Supports A/B testing different thresholds

---

## Development Workflow

### Phase-by-Phase Implementation

This architecture is designed to be built incrementally across 6 phases:

1. **Phase 1**: Project skeleton (backend + frontend communication)
2. **Phase 2**: Simple agent foundation (single agent with GPT-5)
3. **Phase 3**: Supervisor + first worker (multi-agent pattern)
4. **Phase 4**: Remaining workers (complete agent system)
5. **Phase 5**: RAG/CAG implementation (retrieval strategies)
6. **Phase 6**: Multi-provider LLMs + dynamic selection + polish

Refer to `PHASED_DEVELOPMENT_GUIDE.md` for detailed implementation steps.

---

## Testing Strategy

### Unit Tests

**Backend** (`backend/tests/`):
```python
# test_workers.py
def test_technical_support_tool():
    """Test technical support agent with mock vector search."""
    result = technical_support_tool("app crashes on startup")
    assert "clear cache" in result.lower()
    assert len(result) > 50  # Substantial response

# test_orchestrator.py
def test_routing_to_billing():
    """Test supervisor routes billing queries correctly."""
    orchestrator = AgentOrchestrator()
    result = orchestrator.process_message(
        "How much is Pro plan?",
        "test-session-id"
    )
    assert result["agent_used"] == "Billing Support"
```

**Frontend** (`frontend/tests/`):
```javascript
// ChatInterface.test.js
test('sends message to backend', async () => {
  const { getByPlaceholderText, getByText } = render(<ChatInterface />);
  const input = getByPlaceholderText('Type your message...');
  
  fireEvent.change(input, { target: { value: 'Hello' } });
  fireEvent.submit(input);
  
  await waitFor(() => {
    expect(getByText('Hello')).toBeInTheDocument();
  });
});
```

### Integration Tests

```python
# test_integration.py
@pytest.mark.integration
def test_end_to_end_conversation():
    """Test complete conversation flow."""
    session_id = str(uuid.uuid4())
    
    # First message
    response1 = client.post("/chat", json={
        "message": "My app crashes",
        "session_id": session_id
    })
    assert response1.status_code == 200
    assert "Technical Support" in response1.json()["agent_used"]
    
    # Follow-up message (should maintain context)
    response2 = client.post("/chat", json={
        "message": "That didn't work",
        "session_id": session_id
    })
    assert response2.status_code == 200
    # Should remember previous conversation
```

---

## Deployment Considerations

### Environment-Specific Configuration

**Development**:
- Use `InMemorySaver` for checkpointer
- Enable verbose logging
- LangSmith tracing enabled
- CORS allows `localhost:3000`

**Production**:
- Use PostgreSQL/Redis for checkpointer
- Structured logging
- Rate limiting enabled
- CORS restricted to production domain
- HTTPS only
- API key rotation
- Monitoring and alerting

### Scalability Path

**Current (MVP)**:
- Single FastAPI instance
- In-memory checkpointer
- Local ChromaDB

**Production Ready**:
- Multiple FastAPI instances (load balanced)
- Redis checkpointer (shared state)
- Managed ChromaDB or Pinecone
- CDN for frontend
- Database for user management

---

## Conclusion

This architecture provides a solid foundation for a production-quality multi-agent customer service system. The incremental approach (Phases 1-6) allows for rapid iteration while maintaining code quality. The Phase 6 enhancement (dynamic model selection) demonstrates advanced optimization strategies suitable for a portfolio project.

Key strengths:
- ✅ Clear separation of concerns
- ✅ Scalable multi-agent pattern
- ✅ Cost-optimized model selection
- ✅ Multiple retrieval strategies
- ✅ Maintainable and testable code
- ✅ Production-ready patterns

For detailed implementation guidance, refer to `PHASED_DEVELOPMENT_GUIDE.md`.

---

**Ready to build!** 🚀

