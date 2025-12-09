# Backend - Advanced Customer Service AI

FastAPI backend for the multi-agent customer service AI system powered by LangChain v1.0+ and LangGraph.

## Overview

This backend provides REST API endpoints for an intelligent customer service system that uses AI agents powered by LangChain v1.0+, AWS Bedrock, and OpenAI.

**Current Status: Phase 6 Complete ✅ - MVP PRODUCTION READY**

The backend implements a complete multi-agent AI system with advanced knowledge retrieval (RAG/CAG), multi-provider LLMs, and real-time streaming responses.

**Key Features:**
- 🤖 **Multi-Provider LLMs** - AWS Bedrock Nova Lite (routing) + OpenAI GPT-4o-mini (generation)
- 🔄 **Real-Time Streaming** - Server-Sent Events (SSE) for token-by-token responses
- 📚 **Advanced RAG/CAG** - Pure RAG, Hybrid RAG/CAG, and Pure CAG strategies
- 🎯 **4-Worker Multi-Agent System** - Supervisor coordinates 4 specialized domains
- 🔀 **Intelligent Routing** - Supervisor analyzes queries and delegates to appropriate workers
- 🛠️ **Technical Support Worker** (Pure RAG) - Troubleshooting, errors, bugs, and technical issues
- 💳 **Billing Support Worker** (Hybrid RAG/CAG) - Payments, invoices, subscriptions, and refunds
- 📋 **Compliance Worker** (Pure CAG) - Policies, privacy, GDPR/CCPA, and legal matters
- 📚 **General Information Worker** (Pure RAG) - Company info, services, features, and FAQs
- 💾 **Session-based Memory** - Conversation history maintained across routing
- 🔄 **RESTful API** with FastAPI - `/chat` and `/chat/stream` endpoints
- ✅ **Comprehensive Test Coverage** - 145 tests passing (91% coverage)
- 📊 **LangSmith Tracing** - Debug multi-agent interactions step-by-step
- 📝 **Routing Visibility** - Detailed logging of supervisor decisions
- 🔙 **Automatic Fallback** - Gracefully falls back to OpenAI if AWS unavailable

**Key Technologies:**
- **FastAPI** - Modern, high-performance web framework
- **LangChain v1.0+** - LLM application framework (using `create_agent`)
- **LangGraph** - Multi-agent orchestration with supervisor pattern
- **AWS Bedrock** - Nova Lite for cost-effective supervisor routing
- **OpenAI GPT-4o-mini** - Language model for worker agents
- **ChromaDB** - Vector database for RAG retrieval
- **Pydantic** - Data validation and settings management
- **Pytest** - Testing framework with comprehensive coverage

## Project Structure

```
backend/
├── agents/                           # Agent modules
│   ├── __init__.py                  # Exports get_supervisor(), get_agent()
│   ├── simple_agent.py              # Phase 2: Simple agent (reference/fallback)
│   ├── supervisor_agent.py          # Phase 6: Supervisor with 4 workers + RAG/CAG ✅
│   ├── tools/                       # Phase 5: RAG/CAG tools
│   │   ├── __init__.py              # Exports RAG tools
│   │   └── rag_tools.py            # RAG retrieval and CAG caching tools ✅
│   └── workers/                     # Phase 3-6: Specialized worker agents
│       ├── __init__.py              # Exports all workers and tools
│       ├── technical_support.py    # Technical support (Pure RAG) ✅
│       ├── billing_support.py      # Billing support (Hybrid RAG/CAG) ✅
│       ├── compliance.py           # Compliance (Pure CAG) ✅
│       └── general_info.py         # General information (Pure RAG) ✅
├── data/                            # Data and documents
│   ├── __init__.py
│   ├── document_loader.py          # Document loading utilities ✅
│   ├── vectorstore.py              # ChromaDB vector store setup ✅
│   └── docs/                       # Document storage
│       ├── billing/                # Billing documents (2 files)
│       │   ├── pricing-plans.md
│       │   └── refund-policy.md
│       ├── compliance/             # Compliance documents (2 files)
│       │   ├── privacy-policy.md
│       │   └── terms-of-service.md
│       ├── general/                # General info documents (2 files)
│       │   ├── about-company.md
│       │   └── service-overview.md
│       └── technical/              # Technical documentation (2 files)
│           ├── error-codes.md
│           └── troubleshooting.md
├── scripts/                         # Utility scripts
│   └── index_documents.py          # Document indexing pipeline ✅
├── tests/                           # Test suite (145 tests total)
│   ├── __init__.py
│   ├── test_main.py                # API endpoint tests (47 tests ✅)
│   ├── test_agent.py               # Phase 2 agent tests (10 tests)
│   ├── test_supervisor.py          # Supervisor unit tests (15 tests ✅)
│   ├── test_technical_worker.py    # Technical worker tests (19 tests ✅)
│   ├── test_billing_worker.py      # Billing worker tests (18 tests ✅)
│   ├── test_compliance_worker.py   # Compliance worker tests (18 tests ✅)
│   ├── test_general_info_worker.py # General info worker tests (18 tests ✅)
│   └── test_rag_tools.py           # RAG/CAG tools tests ✅
├── utils/                           # Utility functions
│   └── __init__.py
├── main.py                          # FastAPI app with /chat and /chat/stream ✅
├── conftest.py                      # Pytest configuration and fixtures
├── requirements.txt                 # Python dependencies
├── .env.example                    # Environment variable template
├── test_routing_logs.sh            # Script to test routing visibility ✅
├── Dockerfile                       # Container configuration
├── pytest.ini                       # Pytest configuration
└── README.md                        # This file
```

**Phase 6 Status:** ✅ Complete - MVP Production Ready
- 4-worker multi-agent supervisor architecture with intelligent routing
- **Multi-Provider LLMs**: AWS Bedrock Nova Lite (supervisor) + OpenAI GPT-4o-mini (workers)
- **Real-Time Streaming**: SSE streaming with `/chat/stream` endpoint
- **Technical Support Worker** (Pure RAG) - Errors, bugs, crashes, troubleshooting
- **Billing Support Worker** (Hybrid RAG/CAG) - Payments, invoices, subscriptions, refunds
- **Compliance Worker** (Pure CAG) - Policies, privacy, GDPR/CCPA, data protection
- **General Information Worker** (Pure RAG) - Company info, services, features, FAQs
- **8 Sample Documents** - 2 per domain indexed in ChromaDB
- Tool-calling pattern (supervisor calls workers as tools)
- Conversation memory maintained across routing
- Enhanced logging with routing visibility (🔀 ROUTING, ✋ DIRECT)
- 145 tests passing: 129 unit tests + 16 integration tests
- LangSmith tracing shows multi-agent interactions
- 91% code coverage for all worker agents
- Automatic fallback to OpenAI if AWS unavailable

## Multi-Agent Architecture (Phase 6 Complete)

### Overview

Phase 6 implements a comprehensive **multi-agent supervisor pattern** with 4 specialized worker agents, advanced RAG/CAG knowledge retrieval, multi-provider LLMs, and real-time streaming. The supervisor intelligently analyzes incoming queries and routes them to the most appropriate domain expert, with each worker using an optimized knowledge retrieval strategy.

**Architecture Diagram:**
```
User Query → FastAPI Endpoint (/chat or /chat/stream)
    ↓
Supervisor Agent (AWS Nova Lite with OpenAI fallback)
    ↓
    ├─→ [Technical Support Tool] → Technical Worker (Pure RAG) → ChromaDB Search → Response
    ├─→ [Billing Support Tool] → Billing Worker (Hybrid RAG/CAG) → Cache/Search → Response
    ├─→ [Compliance Tool] → Compliance Worker (Pure CAG) → Pre-loaded Docs → Response
    ├─→ [General Info Tool] → General Info Worker (Pure RAG) → ChromaDB Search → Response
    └─→ [Direct Handling] → Response (greetings, thanks, simple queries)
         ↓
    User receives specialized response (streamed or standard)
```

### RAG/CAG Strategies

| Worker | Strategy | Description |
|--------|----------|-------------|
| **Technical Support** | Pure RAG | Always searches ChromaDB for current technical docs |
| **Billing Support** | Hybrid RAG/CAG | First query searches, subsequent use cached policies |
| **Compliance** | Pure CAG | Pre-loaded documents at startup for instant responses |
| **General Info** | Pure RAG | Always searches ChromaDB for company information |

### How It Works

1. **User sends query** to `/chat` endpoint with session_id
2. **Supervisor agent analyzes** the query to understand intent and domain
3. **Routing decision** to appropriate specialist:
   - **Technical queries** (errors, bugs, crashes, troubleshooting) → Technical Support worker
   - **Billing queries** (payments, invoices, subscriptions, refunds) → Billing Support worker
   - **Compliance queries** (policies, privacy, GDPR/CCPA, data deletion) → Compliance worker
   - **General queries** (company info, services, features, FAQs) → General Information worker
   - **Simple queries** (greetings, thanks, clarifications) → Handles directly
4. **Response generation**:
   - Worker agents provide specialized domain expertise
   - Supervisor ensures complete, accurate response returned to user
5. **Memory maintained** across routing via checkpointer + thread_id

### Supervisor Agent

**Location:** `backend/agents/supervisor_agent.py`

**Role:** Intelligent coordinator that analyzes queries and routes to appropriate domain specialists

**Key Features:**
- Analyzes query intent and domain using GPT-4o-mini
- Routes to 4 specialized worker tools based on query content
- Handles simple conversational queries directly
- Maintains conversation memory with InMemorySaver checkpointer
- Provides comprehensive final responses to users

**System Prompt Strategy:**
```python
# Supervisor understands routing across 4 domains:
# - Technical Support: errors, bugs, crashes, troubleshooting
# - Billing Support: payments, invoices, subscriptions, refunds
# - Compliance: policies, privacy, GDPR/CCPA, data protection
# - General Information: company info, services, features, FAQs
# - Direct handling: greetings, thanks, simple questions
# - How to use worker tools with complete context
# - Importance of returning full responses to users
```

**Tool Configuration:**
- Registered with 4 worker tools:
  - `technical_support_tool` - Technical issues and troubleshooting
  - `billing_support_tool` - Payments, invoices, and subscriptions
  - `compliance_tool` - Policies, privacy, and data protection
  - `general_info_tool` - Company information and services

### Technical Support Worker

**Location:** `backend/agents/workers/technical_support.py`

**Role:** Specialized agent for troubleshooting technical issues

**Expertise:**
- Software errors and bugs
- Installation and configuration issues
- Performance problems
- Crashes and system failures
- Diagnostic guidance and step-by-step solutions

**Tool Wrapper:**
```python
@tool
def technical_support_tool(query: str) -> str:
    """Handle technical support questions including errors, bugs, crashes, and troubleshooting.
    
    Use this tool when users report:
    - Error messages or error codes
    - Application crashes or freezes  
    - Installation or setup problems
    - Configuration issues
    - Performance problems
    - "Not working" or "broken" functionality
    """
    # Invokes technical worker agent
    # Returns complete response as string
```

**Key Features:**
- Deep technical knowledge and troubleshooting methodology
- Provides step-by-step solutions
- Asks clarifying questions when needed
- Maintains technical accuracy

### Billing Support Worker

**Location:** `backend/agents/workers/billing_support.py`

**Role:** Specialized agent for payment, billing, and subscription matters

**Expertise:**
- Payment processing and methods
- Invoice and charge inquiries
- Subscription management (upgrade, downgrade, cancel)
- Refund requests and disputes
- Pricing information and plans
- Account balance issues

**Tool Wrapper:**
```python
@tool
def billing_support_tool(query: str) -> str:
    """Handle billing and payment questions including charges, refunds, and subscriptions.
    
    Use this tool when users ask about:
    - Payment methods, processing, or errors
    - Invoice details or unexpected charges
    - Subscription changes or cancellation
    - Refund requests or billing disputes
    - Pricing or plan information
    """
```

**Key Features:**
- Financial accuracy and attention to detail
- Clear explanations of charges and policies
- Empathetic handling of billing concerns
- Secure handling of payment information

### Compliance Worker

**Location:** `backend/agents/workers/compliance.py`

**Role:** Specialized agent for policy, privacy, and regulatory compliance matters

**Expertise:**
- Terms of Service and policies
- Privacy policy and data collection practices
- GDPR, CCPA, and data protection regulations
- Data deletion, export, and access requests
- Cookie policy and consent management
- Legal and regulatory questions

**Tool Wrapper:**
```python
@tool
def compliance_tool(query: str) -> str:
    """Handle compliance, policy, and privacy questions.
    
    Use this tool when users ask about:
    - Terms of Service or policies
    - Privacy policy and data collection
    - GDPR, CCPA, or data protection rights
    - Data deletion, export, or access requests
    - Legal or regulatory compliance
    """
```

**Key Features:**
- Accurate interpretation of policies and regulations
- Clear explanations of user rights
- Professional handling of legal matters
- Guidance on compliance procedures

### General Information Worker

**Location:** `backend/agents/workers/general_info.py`

**Role:** Specialized agent for company information, services, and general support

**Expertise:**
- Company background and mission
- Service offerings and features
- Getting started guides and onboarding
- Plan comparisons and recommendations
- General "how-to" for basic usage
- Best practices and tips
- Navigation and interface help

**Tool Wrapper:**
```python
@tool
def general_info_tool(query: str) -> str:
    """Handle general information questions about company, services, and features.
    
    Use this tool when users ask about:
    - Company information or background
    - Available services and features
    - How to get started or use the platform
    - Plan comparisons or recommendations
    - General guidance and best practices
    """
```

**Key Features:**
- Comprehensive knowledge of company and services
- Friendly and welcoming tone for new users
- Clear guidance for getting started
- Helpful recommendations and tips

### Routing Logic

The supervisor uses **tool descriptions** to intelligently route queries to the most appropriate worker:

**Routes to Technical Support Tool when query contains:**
- Error messages (e.g., "Error 500", "404 not found")
- Problem keywords (e.g., "not working", "broken", "fails", "crash")
- Technical terms (e.g., "install", "configure", "setup", "performance")
- Troubleshooting requests (e.g., "how do I fix", "can't access")

**Routes to Billing Support Tool when query contains:**
- Payment keywords (e.g., "payment", "charge", "charged", "invoice")
- Subscription terms (e.g., "subscription", "upgrade", "downgrade", "cancel")
- Refund requests (e.g., "refund", "money back", "charged twice")
- Pricing inquiries (e.g., "how much", "cost", "price", "plan")

**Routes to Compliance Tool when query contains:**
- Policy keywords (e.g., "privacy policy", "terms of service", "policies")
- Regulatory terms (e.g., "GDPR", "CCPA", "data protection", "compliance")
- Data rights (e.g., "delete my data", "export data", "data access")
- Legal questions (e.g., "legal", "regulations", "rights", "consent")

**Routes to General Info Tool when query contains:**
- Company inquiries (e.g., "about your company", "who are you", "what do you do")
- Service questions (e.g., "what services", "features", "offerings")
- Getting started (e.g., "how do I start", "getting started", "onboarding")
- Plan comparisons (e.g., "compare plans", "which plan", "differences")

**Handles directly when query is:**
- Greetings (e.g., "Hello", "Hi there")
- Gratitude (e.g., "Thank you", "Thanks")
- Clarifications (e.g., "What do you mean?", "Can you explain?")
- Simple acknowledgments (e.g., "That makes sense", "I understand")

**Routing Visibility:**

The system logs routing decisions for debugging:

```bash
# Technical query routed to worker
🔀 ROUTING: Query routed to worker agent (session: abc-123, time: 1.5s)

# General query handled directly
✋ DIRECT: Supervisor handled query directly (session: abc-123, time: 0.3s)
```

### Adding New Worker Agents

Follow this pattern to add new specialized workers:

**1. Create Worker Module** (`agents/workers/your_worker.py`):

```python
from langchain.agents import create_agent
from langchain.tools import tool
import logging

logger = logging.getLogger(__name__)

def create_your_worker_agent():
    """Create specialized worker agent."""
    system_prompt = """You are a specialist in [domain].
    Your role is to...
    
    CRITICAL: The supervisor only sees your final message.
    Include ALL results, findings, and details in your final response.
    """
    
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[],  # Worker-specific tools if needed
        system_prompt=system_prompt,
        name="your_worker_agent",  # Descriptive name
    )
    
    logger.info(f"Your worker agent created successfully")
    return agent

# Module-level singleton
_agent_instance = None

def get_your_worker():
    """Get singleton instance of worker agent."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_your_worker_agent()
    return _agent_instance

# Tool wrapper for supervisor
@tool
def your_worker_tool(query: str) -> str:
    """Handle [domain] questions.
    
    Use this tool when users ask about [specific topics].
    Examples: [list examples]
    """
    logger.info(f"Your worker tool called with query: {query[:50]}...")
    
    agent = get_your_worker()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    response = result["messages"][-1].content
    
    logger.info(f"Your worker tool returning response: {response[:50]}...")
    return response
```

**2. Export from Workers Package** (`agents/workers/__init__.py`):

```python
from agents.workers.your_worker import (
    create_your_worker_agent,
    get_your_worker,
    your_worker_tool,  # Primary export for supervisor
)

__all__ = [
    # ... existing exports ...
    "create_your_worker_agent",
    "get_your_worker", 
    "your_worker_tool",
]
```

**3. Register with Supervisor** (`agents/supervisor_agent.py`):

```python
from agents.workers import technical_support_tool, your_worker_tool

# In create_supervisor_agent():
tools = [
    technical_support_tool,
    your_worker_tool,  # Add your tool
]

system_prompt = """...
3. Route [domain] questions to the Your Worker specialist
...
"""
```

**4. Write Tests** (`tests/test_your_worker.py`):

```python
import pytest
from agents.workers.your_worker import (
    create_your_worker_agent,
    get_your_worker,
    your_worker_tool,
)

@pytest.mark.unit
def test_create_your_worker_agent():
    """Test your worker agent creation."""
    agent = create_your_worker_agent()
    assert agent is not None
    # ... more assertions ...
```

**5. Update Supervisor System Prompt** with routing guidelines for new worker.

### Best Practices for Multi-Agent Systems

**DO:**
- ✅ Give each worker a clear, non-overlapping domain
- ✅ Write specific tool descriptions to guide supervisor routing
- ✅ Emphasize final output in worker system prompts
- ✅ Test workers independently before integration
- ✅ Use `ToolRuntime` to pass conversation context if needed
- ✅ Monitor routing decisions with logging

**DON'T:**
- ❌ Overlap worker responsibilities (causes routing confusion)
- ❌ Forget to remind workers that supervisor only sees final output
- ❌ Skip testing individual workers (test before integration)
- ❌ Use manual LangGraph for basic multi-agent (use supervisor pattern)

## Prerequisites

Before setting up the backend, ensure you have:

- **Python 3.11+** (Python 3.13 recommended)
- **pip** (Python package manager)
- **virtualenv** or **venv** (for isolated environments)
- **Docker** (optional, for containerized deployment)
- **API Keys** (see Environment Variables section)

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**Key Dependencies Installed:**
- `fastapi>=0.104.0` - Web framework
- `uvicorn[standard]>=0.24.0` - ASGI server
- `langchain>=1.0.0` - LangChain core
- `langchain-community>=1.0.0` - Community integrations
- `langchain-openai>=1.0.0` - OpenAI integration
- `langgraph>=1.0.0` - Agent orchestration
- `chromadb>=0.4.0` - Vector database
- `pytest>=7.4.0` - Testing framework
- `ruff>=0.1.0` - Linter and formatter

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys and configuration
nano .env  # or use your preferred editor
```

**Required Environment Variables (Phase 3):**
- `OPENAI_API_KEY` - **REQUIRED** - OpenAI API key for GPT-4o-mini
  - Get your key at: https://platform.openai.com/api-keys
  - Format: `sk-proj-...`
  - Used by supervisor and all worker agents

**Optional Environment Variables:**
- `LANGSMITH_TRACING` - Enable LangSmith tracing (`true`/`false`)
  - **Highly recommended** for development and debugging
  - View traces at: https://smith.langchain.com/
- `LANGSMITH_API_KEY` - LangSmith API key (if tracing enabled)
  - Get your key at: https://smith.langchain.com/settings
  - Format: `lsv2_...`
- `LANGSMITH_PROJECT` - LangSmith project name (default: `customer-service-phase3`)
- `ENVIRONMENT` - Environment name (`development`/`staging`/`production`)
- `LOG_LEVEL` - Logging level (`DEBUG`/`INFO`/`WARNING`/`ERROR`)

**Example `.env` file for Phase 3:**
```bash
# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=sk-proj-your-actual-key-here

# LangSmith Configuration (OPTIONAL but recommended)
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_your-key-here
LANGSMITH_PROJECT=customer-service-phase3

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Future Phases (not needed for Phase 2):**
- `AWS_ACCESS_KEY_ID` - AWS credentials for Bedrock (Phase 6)
- `AWS_SECRET_ACCESS_KEY` - AWS secret key (Phase 6)
- `AWS_DEFAULT_REGION` - AWS region (Phase 6)
- `CORS_ORIGINS` - Allowed CORS origins (configured in code for Phase 2)

### 4. Verify Installation

```bash
# Check Python version
python --version

# Verify dependencies installed
pip list | grep langchain

# Test import
python -c "import fastapi, langchain, langgraph; print('✅ All imports successful')"
```

## Running the Application

### Development Mode (with auto-reload)

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Run with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Or run the main.py directly:**

```bash
python main.py
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Production Mode

```bash
# Run without auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Recommended Production Settings:**
- Use multiple workers (`--workers 4` for a 4-core CPU)
- Set `LOG_LEVEL=INFO` or `LOG_LEVEL=WARNING`
- Use a process manager like **Supervisor** or **systemd**
- Deploy behind a reverse proxy (Nginx, Caddy, etc.)

## Testing

### Run All Tests

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py -v
```

### Run Tests with Coverage Report

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# View HTML coverage report
open htmlcov/index.html  # macOS
# xdg-open htmlcov/index.html  # Linux
# start htmlcov/index.html  # Windows
```

### Test Categories

Tests are organized with markers:
- `@pytest.mark.unit` - Fast, isolated unit tests (44 tests)
- `@pytest.mark.integration` - Integration tests (10 tests, requires --run-integration flag)
- `@pytest.mark.slow` - Slow-running tests

```bash
# Run only unit tests (fast, no API calls)
pytest -m unit

# Run integration tests (with mocked supervisor)
pytest -m integration --run-integration

# Run all tests including integration
pytest --run-integration

# Skip slow tests
pytest -m "not slow"
```

**Phase 3 Test Suite:**
- **test_supervisor.py** - 15 unit tests for supervisor agent
- **test_technical_worker.py** - 19 unit tests for technical worker
- **test_main.py** - 37 total tests (27 endpoint + 10 integration routing tests)
- **Total**: 54 tests, all passing ✅

### Testing Multi-Agent Routing

**Manual Test Script:**

Use the provided script to test routing decisions with real API calls:

```bash
# Make script executable
chmod +x test_routing_logs.sh

# Run the test script (requires backend server running)
./test_routing_logs.sh
```

The script sends both technical and general queries, showing routing decisions in logs:
- Technical queries show `🔀 ROUTING` indicator (routed to worker)
- General queries show `✋ DIRECT` indicator (handled by supervisor)

**Example Manual Test (with curl):**

```bash
# Start backend server in one terminal
uvicorn main:app --reload

# In another terminal, test technical query (should route)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Getting Error 500 when trying to log in",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Check logs - should see: 🔀 ROUTING: Query routed to worker agent

# Test general query (should handle directly)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How are you?",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Check logs - should see: ✋ DIRECT: Supervisor handled query directly
```

## Docker Usage

### Build Docker Image

```bash
# From the backend directory
docker build -t customer-service-ai-backend:latest .
```

### Run Container

```bash
# Run with environment variables
docker run -d \
  --name cs-ai-backend \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=INFO \
  customer-service-ai-backend:latest

# Check logs
docker logs cs-ai-backend

# Stop container
docker stop cs-ai-backend

# Remove container
docker rm cs-ai-backend
```

### Docker Compose (from project root)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## API Documentation

### Available Endpoints (Phase 6)

#### Health Check
```
GET /health
```
Returns service status and version information.

**Response:**
```json
{
  "status": "healthy",
  "service": "customer-service-ai",
  "version": "1.0.0",
  "environment": "development"
}
```

#### Root Endpoint
```
GET /
```
Returns API information and links to documentation.

**Response:**
```json
{
  "message": "Customer Service API is running",
  "docs": "/docs",
  "health": "/health",
  "version": "1.0.0"
}
```

#### Chat Endpoint (Standard) 🚀
```
POST /chat
```
Send a message to the AI customer service system. The supervisor agent intelligently routes your query to specialized workers or handles it directly, maintaining conversation history based on the session ID.

**Request Body:**
```json
{
  "message": "Hello, how can you help me?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Parameters:**
- `message` (string, required): User's message (1-2000 characters)
- `session_id` (string, required): UUID v4 format session identifier

**Success Response (200 OK):**
```json
{
  "response": "Hello! I'm here to assist you with any questions or concerns you may have. How can I help you today?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Error Responses:**

- **400 Bad Request** - Invalid session_id format
```json
{
  "error": "Invalid session_id format",
  "detail": "session_id must be a valid UUID v4",
  "session_id": "invalid-uuid"
}
```

- **422 Unprocessable Entity** - Validation error (missing fields, message too long)
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

- **500 Internal Server Error** - OpenAI API error or agent failure
```json
{
  "error": "Failed to process your message",
  "detail": "OpenAI authentication error: Invalid API key",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

- **503 Service Unavailable** - OpenAI API connection error
```json
{
  "error": "Service temporarily unavailable",
  "detail": "Could not connect to OpenAI API",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Example Usage (curl):**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What services do you offer?",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Example Usage (Python):**
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "Hello, how are you?",
        "session_id": "550e8400-e29b-41d4-a716-446655440000"
    }
)

data = response.json()
print(f"AI: {data['response']}")
```

**Conversation Memory & Routing:**
The supervisor maintains conversation history for each session_id, even across routing to different workers. Use the same session_id for follow-up messages to maintain context.

**Example - Technical Query with Routing:**

```python
# Technical query - routed to Technical Support worker
response1 = requests.post("http://localhost:8000/chat", json={
    "message": "Getting Error 500 when logging in",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
})
# Response from Technical Support worker with troubleshooting steps
# Log shows: 🔀 ROUTING: Query routed to worker agent

# Follow-up - context maintained across routing
response2 = requests.post("http://localhost:8000/chat", json={
    "message": "I tried that but still not working",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"  # Same session
})
# Worker remembers previous steps and provides next troubleshooting options
```

**Example - General Query (Direct Handling):**
```python
# General greeting - handled directly by supervisor
response = requests.post("http://localhost:8000/chat", json={
    "message": "Hello! How are you?",
    "session_id": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
})
# Response from supervisor directly (no routing needed)
# Log shows: ✋ DIRECT: Supervisor handled query directly
```

#### Streaming Chat Endpoint (SSE) ⚡

```
POST /chat/stream
```
Send a message and receive real-time token-by-token streaming response via Server-Sent Events (SSE).

**Request Body:**
```json
{
  "message": "What are your pricing plans?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:** Server-Sent Events stream

**Event Format:**
```
data: {"type": "start", "session_id": "550e8400-..."}
data: {"type": "token", "content": "Our", "session_id": "550e8400-..."}
data: {"type": "token", "content": " pricing", "session_id": "550e8400-..."}
data: {"type": "token", "content": " plans", "session_id": "550e8400-..."}
...
data: {"type": "done", "session_id": "550e8400-...", "agent": "Billing Support", "tokens": 150, "time": 1.5}
```

**Event Types:**
- `start`: Stream started
- `token`: Content token with `content` field
- `done`: Stream complete with metadata (`agent`, `tokens`, `time`)
- `error`: Error occurred with `error` and `detail` fields

**Example Usage (JavaScript):**
```javascript
const response = await fetch('http://localhost:8000/chat/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'text/event-stream',
  },
  body: JSON.stringify({
    message: 'Tell me about your services',
    session_id: sessionId,
  }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const text = decoder.decode(value);
  // Parse SSE events and update UI
}
```

#### Interactive Documentation
- **Swagger UI**: `/docs` - Test endpoints interactively
- **ReDoc**: `/redoc` - Clean, searchable API reference
- **OpenAPI Schema**: `/openapi.json` - Machine-readable API spec

## Development Guidelines

### Code Style

This project uses **Ruff** for linting and formatting:

```bash
# Check code quality
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .
```

### Adding New Endpoints

1. Add endpoint function in `main.py` or create a new router
2. Use type hints and Pydantic models for request/response
3. Add docstrings explaining the endpoint
4. Write tests in `tests/` directory
5. Update API documentation

**Example:**
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    response: str

router = APIRouter(prefix="/api/v1")

@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """Handle customer service query."""
    # Your logic here
    return QueryResponse(response="...")
```

### Adding New Worker Agents (Phase 3+)

See the detailed "Adding New Worker Agents" section in the Multi-Agent Architecture documentation above for a complete guide. Summary:

1. Create worker module in `agents/workers/your_worker.py`
2. Use `create_agent()` with specialized system prompt
3. Create `@tool` wrapper function for supervisor integration
4. Export from `agents/workers/__init__.py`
5. Register tool with supervisor in `supervisor_agent.py`
6. Update supervisor system prompt with routing guidelines
7. Write comprehensive unit tests (`tests/test_your_worker.py`)
8. Test independently before integration

**Key Pattern:**
- Worker agents provide specialized expertise
- Tool wrappers enable supervisor integration
- Clear tool descriptions guide routing decisions
- Workers return complete responses (supervisor only sees final message)

### LangChain v1.0 Best Practices

- ✅ Use `create_agent()` for agent creation
- ✅ Use `@tool` decorator for tool definitions
- ✅ Use checkpointers for conversation memory
- ✅ Enable LangSmith tracing for debugging
- ❌ Avoid deprecated LCEL patterns
- ❌ Don't use `create_react_agent()` (removed in v1.0)

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'langchain'
# Solution: Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

#### Port Already in Use
```bash
# Error: OSError: [Errno 48] Address already in use
# Solution: Change port or kill existing process
lsof -ti:8000 | xargs kill -9
uvicorn main:app --reload --port 8001
```

#### OpenAI API Key Not Found
```bash
# Error: openai.error.AuthenticationError
# Solution: Set OPENAI_API_KEY in .env file
echo "OPENAI_API_KEY=your_key_here" >> .env
```

#### ChromaDB Permission Errors
```bash
# Error: PermissionError: [Errno 13] Permission denied: 'chroma_db'
# Solution: Create directory with proper permissions
mkdir -p chroma_db
chmod 755 chroma_db
```

#### SSL Certificate Errors (macOS)
```bash
# Error: SSLCertVerificationError
# Solution: Install Python certificates
/Applications/Python\ 3.*/Install\ Certificates.command
```

### Debug Mode

Enable detailed logging:

```bash
# Set in .env file
LOG_LEVEL=DEBUG

# Or run with debug flag
uvicorn main:app --reload --log-level debug
```

### LangSmith Tracing (Highly Recommended)

LangSmith provides detailed traces of agent execution, showing:
- Every LLM call made by the agent
- Input/output of each step
- Token usage and costs
- Latency for each operation
- Error details with full stack traces

**Setup:**

1. Create account at https://smith.langchain.com/
2. Get API key from Settings
3. Add to `.env` file:

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_your_actual_key_here
LANGSMITH_PROJECT=customer-service-phase2
```

4. Restart backend server
5. Make API calls to `/chat`
6. View traces at: https://smith.langchain.com/

**Example Trace Information:**
```
📊 Trace: POST /chat
├── Agent Invocation
│   ├── Model: gpt-4o-mini
│   ├── Input: "Hello, how are you?"
│   ├── Output: "Hello! I'm doing well..."
│   ├── Tokens: 45 (15 input, 30 output)
│   └── Latency: 1.2s
└── Checkpointer: InMemorySaver
    └── Session: 550e8400-e29b-41d4-a716-446655440000
```

**Benefits:**
- ✅ Debug agent behavior step-by-step
- ✅ Monitor token usage and costs
- ✅ Identify performance bottlenecks
- ✅ Analyze error patterns
- ✅ Compare different prompts/models

**No code changes needed** - just environment variables!

## Additional Resources

- **LangChain Documentation**: https://docs.langchain.com/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **LangGraph Guide**: https://docs.langchain.com/oss/python/langgraph
- **ChromaDB Documentation**: https://docs.trychroma.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/

## Support

For questions or issues:
1. Check this README and documentation
2. Review test files for usage examples
3. Enable debug logging and LangSmith tracing
4. Check GitHub issues for known problems

---

## Phase 6 Completion Status

**✅ Phase 6 Complete** - MVP Production Ready

**What's Included:**
- **Multi-Provider LLMs** - AWS Bedrock Nova Lite (routing) + OpenAI GPT-4o-mini (generation)
- **Real-Time Streaming** - SSE streaming with `/chat/stream` endpoint
- **Advanced RAG/CAG** - Pure RAG, Hybrid RAG/CAG, and Pure CAG strategies
- **Supervisor Agent** - Intelligent coordinator routing across 4 domains
- **Technical Support Worker** (Pure RAG) - Errors, bugs, crashes, troubleshooting
- **Billing Support Worker** (Hybrid RAG/CAG) - Payments, invoices, subscriptions, refunds
- **Compliance Worker** (Pure CAG) - Policies, privacy, GDPR/CCPA, data protection
- **General Information Worker** (Pure RAG) - Company info, services, features, FAQs
- **8 Sample Documents** - 2 per domain indexed in ChromaDB
- **Document Indexing Pipeline** - `scripts/index_documents.py`
- **Tool-Calling Pattern** - All workers wrapped as supervisor tools
- **Intelligent Routing** - Analyzes intent, routes to appropriate domain specialist
- **Conversation Memory** - Maintained across routing via checkpointer
- **Routing Visibility** - Detailed logging (🔀 ROUTING, ✋ DIRECT indicators)
- **Comprehensive Tests** - 145 tests passing (129 unit + 16 integration)
- **High Coverage** - 91% for all worker agents
- **LangSmith Support** - Multi-agent interaction tracing
- **Automatic Fallback** - Gracefully falls back to OpenAI if AWS unavailable
- **Extensible Architecture** - Easy to add new worker agents

**Architecture:**
```
User → FastAPI (/chat or /chat/stream)
        ↓
    Supervisor Agent (AWS Nova Lite + fallback)
        ↓
    ├─→ Technical Support Tool → Technical Worker (Pure RAG)
    ├─→ Billing Support Tool → Billing Worker (Hybrid RAG/CAG)
    ├─→ Compliance Tool → Compliance Worker (Pure CAG)
    ├─→ General Info Tool → General Info Worker (Pure RAG)
    └─→ Direct Handling
            ↓
    ChromaDB / Cache / Pre-loaded Docs
            ↓
    Specialized Response to User (streaming or standard)
```

**All 6 Phases Complete:**
- ✅ **Phase 1**: Project Skeleton
- ✅ **Phase 2**: Simple Agent Foundation
- ✅ **Phase 3**: Multi-Agent Supervisor
- ✅ **Phase 4**: Additional Workers (4 total)
- ✅ **Phase 5**: RAG/CAG Integration
- ✅ **Phase 6**: Multi-Provider LLMs & Streaming

---

**Version**: 1.2.0 (Phase 6 Complete)  
**Last Updated**: December 9, 2025  
**LangChain Version**: 1.0+
**Test Coverage**: 145 tests passing (91% coverage)  
**Status**: ✅ MVP Production Ready

