# Advanced Multi-Agent Customer Service AI

An intelligent, agentic customer service system powered by LangChain v1.0+ and LangGraph.

**Current Status: Phase 6 Complete ✅** - MVP PRODUCTION READY

This is a complete, portfolio-ready multi-agent customer service system featuring:
- 🤖 **Multi-Provider LLMs**: AWS Bedrock (Nova Lite) for routing + OpenAI (GPT-4o-mini) for generation
- 🔄 **Real-Time Streaming**: Server-Sent Events (SSE) with user toggle
- 📚 **Advanced RAG/CAG**: Pure RAG, Pure CAG, and Hybrid strategies
- 🎯 **4 Specialized Agents**: Technical Support, Billing, Compliance, and General Information
- 🧪 **Production Quality**: 145 tests passing (91% coverage)

A supervisor agent intelligently routes queries to specialized workers while maintaining conversation memory across routing.

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd Agentic_Customer_Project1

# 2. Set up the backend (FastAPI + LangChain)
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
uvicorn main:app --reload

# 3. In a new terminal, set up the frontend (Next.js + TypeScript)
cd frontend
pnpm install
cp .env.example .env.local
# Edit .env.local if needed (default: http://localhost:8000)
pnpm dev
```

**Access the application:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## ✨ Features (Phase 6 Complete - MVP Ready)

### 🤖 **Multi-Provider LLM Architecture**
- **Supervisor Agent**: AWS Bedrock Nova Lite ($0.06/1M tokens) for cost-effective routing
- **Worker Agents**: OpenAI GPT-4o-mini ($0.15/1M tokens) for high-quality responses
- **Automatic Fallback**: Gracefully falls back to OpenAI if AWS unavailable
- **11% Cost Savings**: Optimized model selection for each task

### 🔄 **Real-Time Streaming Responses**
- **Server-Sent Events (SSE)**: Token-by-token streaming for immediate user feedback
- **Toggle Mode**: Switch between streaming (real-time) and standard (single response)
- **Smooth UX**: No flicker, graceful error recovery, visual indicators
- **Production Ready**: Full error handling and session continuity

### 📚 **Advanced RAG/CAG Knowledge System**
- **Pure RAG** (Technical & General): Dynamic document retrieval from ChromaDB
- **Hybrid RAG/CAG** (Billing): First query retrieves, subsequent queries use cache
- **Pure CAG** (Compliance): Pre-loaded context for instant, consistent responses
- **8 Document Repository**: 2 documents per domain (technical, billing, compliance, general)

### 🎯 **4 Specialized Worker Agents**

**🛠️ Technical Support** (Pure RAG)
- Errors, bugs, crashes, and software malfunctions
- Installation, configuration, and setup issues
- Performance problems and diagnostics
- Step-by-step troubleshooting from knowledge base

**💳 Billing Support** (Hybrid RAG/CAG)
- Payment methods and processing
- Invoice inquiries and unexpected charges
- Subscription management (upgrade, downgrade, cancel)
- Cached pricing information after first query

**📋 Compliance** (Pure CAG)
- Terms of Service and policy questions
- Privacy policy and data collection practices
- GDPR, CCPA, and data protection regulations
- Instant responses from pre-loaded documents

**📚 General Information** (Pure RAG)
- Company background and mission
- Service offerings and features
- Getting started guides and onboarding
- Dynamic retrieval from general knowledge base

### 🔀 **Intelligent Routing & Memory**
- Domain-specific query analysis and routing
- Conversation context maintained across routing
- Session persistence across page refreshes
- Clear conversation to start fresh
- Detailed logging (🔀 ROUTING, ✋ DIRECT indicators)

### 🎨 **Modern Full-Stack Interface**
- **Backend**: FastAPI with `/chat` and `/chat/stream` endpoints
- **Frontend**: Next.js 16 with TypeScript and Tailwind CSS
- **Real-time Updates**: Token-by-token streaming display
- **User Controls**: Streaming toggle, clear conversation, error handling
- **Type Safety**: Full TypeScript + Pydantic validation

### ✅ **Production Quality**
- **145 Automated Tests**: 129 unit + 16 integration tests
- **91% Code Coverage**: All worker agents thoroughly tested
- **Comprehensive Docs**: Setup guides, architecture, API docs
- **Error Handling**: Graceful fallbacks and user-friendly messages
- **LangSmith Support**: Full tracing and debugging
- **AWS Setup Guide**: Complete 409-line setup documentation

### 🚀 **Try It Out**
1. **Start the application** (see Quick Start above)
2. **Open** http://localhost:3000
3. **Test streaming**: Enable streaming toggle (lightning bolt icon)
4. **Test technical query**: "Getting Error 500 when logging in"
   - Watch response stream token-by-token
   - Check logs for `🔀 ROUTING` to Technical Support
5. **Test billing query**: "What are your pricing plans?"
   - First query retrieves from vector store (RAG)
   - Second query uses cached policies (CAG)
6. **Test compliance query**: "What's your data retention policy?"
   - Instant response from pre-loaded compliance docs
7. **Test memory**: Follow up with "Can you explain more?"
   - Context maintained across routing

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Monorepo Structure](#monorepo-structure)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup-python--fastapi)
  - [Frontend Setup](#frontend-setup-nextjs--typescript)
  - [Docker Setup (Optional)](#docker-setup-optional)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements a production-ready, intelligent customer service AI system powered by **LangChain v1.0+**, **AWS Bedrock**, and **OpenAI**.

**MVP Complete - All 6 Phases Finished:**

A sophisticated multi-agent system featuring:

- 🤖 **Multi-Provider LLMs**: AWS Bedrock Nova Lite for routing, OpenAI GPT-4o-mini for generation
- 🔄 **Real-Time Streaming**: Server-Sent Events (SSE) with user toggle between streaming/standard modes
- 📚 **Advanced RAG/CAG**: Pure RAG, Pure CAG, and Hybrid strategies for optimal knowledge retrieval
- 🎯 **4 Specialized Agents**: Technical Support, Billing, Compliance, and General Information
- 🧠 **Stateful Memory**: Conversation context maintained across routing with InMemorySaver
- 🔀 **Intelligent Routing**: Domain-specific query analysis and agent selection
- 🎨 **Modern Full-Stack**: FastAPI backend + Next.js frontend with TypeScript
- 🧪 **Production Quality**: 145 tests (91% coverage), comprehensive error handling

**Key Technologies:**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI + Python 3.11+ | REST API and agent orchestration |
| **AI Framework** | LangChain v1.0+ & LangGraph | Multi-agent system and workflows |
| **LLM Providers** | AWS Bedrock + OpenAI | Multi-provider strategy for cost optimization |
| **Vector Store** | ChromaDB | Document retrieval and semantic search |
| **Frontend** | Next.js 16 + TypeScript | Modern, responsive web interface |
| **Styling** | Tailwind CSS v4 | Beautiful, utility-first design |
| **Package Manager** | pnpm | Fast, efficient dependency management |
| **Testing** | pytest + TypeScript | 145 automated tests, 91% coverage |

---

## 🏗️ Architecture

**Phase 6 Complete - Production-Ready Multi-Agent System:**

```
┌─────────────────────────────────────────────────────────┐
│              Frontend (Next.js + TypeScript)             │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Chat Interface (with Streaming Toggle)            │ │
│  │  • Real-time SSE streaming or standard responses   │ │
│  │  • Message history with session persistence        │ │
│  │  • User controls (clear, toggle streaming)         │ │
│  └────────────────────┬───────────────────────────────┘ │
└─────────────────────────┼───────────────────────────────┘
                          │ POST /chat or /chat/stream
                          │ {message, session_id}
                          ↓
┌─────────────────────────────────────────────────────────┐
│            Backend (FastAPI + LangChain v1.0+)           │
│  ┌──────────────────┐  ┌──────────────────────────────┐ │
│  │ /chat (standard) │  │ /chat/stream (SSE streaming) │ │
│  └────────┬─────────┘  └──────────┬───────────────────┘ │
│           └──────────────┬─────────┘                     │
└──────────────────────────┼───────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│             Supervisor Agent (AWS Nova Lite)             │
│  • Analyzes query domain (technical/billing/etc.)       │
│  • Routes to appropriate worker agent                    │
│  • Fallback to OpenAI GPT-4o-mini if AWS unavailable    │
│  • Memory: InMemorySaver (cross-routing context)        │
└──────┬───────────┬─────────────┬──────────────┬─────────┘
       │           │             │              │
       ↓           ↓             ↓              ↓
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│Technical │ │ Billing  │ │Compliance│ │   General    │
│ Support  │ │ Support  │ │          │ │ Information  │
│          │ │          │ │          │ │              │
│ Pure RAG │ │ Hybrid   │ │ Pure CAG │ │  Pure RAG    │
│GPT-4o-mi │ │RAG/CAG   │ │GPT-4o-mi │ │ GPT-4o-mini  │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘
     │            │            │               │
     ↓            ↓            ↓               ↓
┌────────────────────────────────────────────────────────┐
│              RAG/CAG Knowledge System                   │
│  ┌──────────────┐  ┌────────────┐  ┌────────────────┐ │
│  │  ChromaDB    │  │   Cache    │  │  Pre-loaded    │ │
│  │  Vector      │  │  Session   │  │  Compliance    │ │
│  │  Store       │  │  Billing   │  │  Documents     │ │
│  │ (Technical,  │  │  Policies  │  │  (ToS, PP)     │ │
│  │  General)    │  │            │  │                │ │
│  └──────────────┘  └────────────┘  └────────────────┘ │
└────────────────────────────────────────────────────────┘
```

**Key Components:**

- **Multi-Provider LLMs**: AWS Nova Lite ($0.06/1M) for supervisor, OpenAI GPT-4o-mini ($0.15/1M) for workers
- **Streaming Support**: SSE for real-time responses, standard mode for single-response
- **4 Worker Agents**: Technical (Pure RAG), Billing (Hybrid), Compliance (Pure CAG), General (Pure RAG)
- **Knowledge Strategies**: 
  - Pure RAG: Dynamic retrieval from ChromaDB
  - Hybrid RAG/CAG: First query retrieves, subsequent use cache
  - Pure CAG: Pre-loaded static documents
- **Session Memory**: InMemorySaver maintains context across routing
- **Automatic Fallback**: Graceful degradation to OpenAI if AWS unavailable
- **Type Safety**: Full TypeScript + Pydantic validation

**For detailed architecture documentation, see:**
- 📘 [**ARCHITECTURE.md**](./ARCHITECTURE.md) - Complete system design and patterns
- 📊 [**FLOWCHARTS.md**](./FLOWCHARTS.md) - Visual process flows and diagrams
- 🗺️ [**PHASED_DEVELOPMENT_GUIDE.md**](./PHASED_DEVELOPMENT_GUIDE.md) - Development roadmap
- 📚 [**PHASE5_RAG_CAG_GUIDE.md**](./PHASE5_RAG_CAG_GUIDE.md) - RAG/CAG implementation details
- 🚀 [**PHASE6_COMPLETION_SUMMARY.md**](./PHASE6_COMPLETION_SUMMARY.md) - Final MVP features

---

## ✅ Prerequisites

Before setting up this project, ensure you have the following installed:

### Required for Backend

- **Python 3.11 or higher** (Python 3.13 recommended)
  ```bash
  python3 --version  # Should be 3.11+
  ```
- **pip** (Python package manager, usually comes with Python)
- **virtualenv** or **venv** (for isolated Python environments)

### Required for Frontend

- **Node.js v20 or higher**
  ```bash
  node --version  # Should be v20+
  ```
- **pnpm v9 or higher** (recommended package manager)
  ```bash
  # Install pnpm if needed
  npm install -g pnpm
  pnpm --version  # Should be v9+
  ```

### Optional but Recommended

- **Docker & Docker Compose** - For containerized deployment
- **Git** - For version control (should already be installed)
- **Visual Studio Code** - Recommended IDE with extensions:
  - Python
  - ESLint
  - Tailwind CSS IntelliSense
  - Prettier

### API Keys Required

You'll need an OpenAI API key to run the agents:

1. **OpenAI API Key**: Get from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. **(Optional) LangSmith API Key**: For debugging and tracing - [https://smith.langchain.com/](https://smith.langchain.com/)
3. **(Optional) AWS Credentials**: If using AWS Bedrock models

---

## 📁 Monorepo Structure

This is a **monorepo** containing both backend and frontend in a single repository:

```
Agentic_Customer_Project1/
├── backend/                    # Python FastAPI backend
│   ├── agents/                 # Agent modules (Phase 2-3)
│   │   ├── simple_agent.py     # Phase 2: Simple agent (reference)
│   │   ├── supervisor_agent.py # Phase 3: Supervisor ✅
│   │   └── workers/            # Phase 3: Specialized workers ✅
│   │       └── technical_support.py  # Technical worker ✅
│   ├── data/                   # Data and documents
│   │   └── docs/              # Document repositories (Phase 5+)
│   │       ├── technical/     # Technical documentation
│   │       ├── billing/       # Billing documents
│   │       └── compliance/    # Compliance documents
│   ├── tests/                  # Backend tests (54 tests ✅)
│   │   ├── test_main.py        # API + routing integration tests
│   │   ├── test_agent.py       # Phase 2 agent tests
│   │   ├── test_supervisor.py  # Supervisor unit tests ✅
│   │   └── test_technical_worker.py # Worker unit tests ✅
│   ├── utils/                  # Utility functions
│   ├── main.py                # FastAPI app with supervisor routing ✅
│   ├── test_routing_logs.sh   # Routing test script ✅
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── Dockerfile            # Backend container config
│   └── README.md             # Backend documentation (Phase 3 ✅)
│
├── frontend/                   # Next.js TypeScript frontend
│   ├── app/                   # Next.js App Router pages
│   ├── components/            # React components
│   ├── lib/                   # Frontend utilities
│   ├── public/                # Static assets
│   ├── package.json          # Frontend dependencies
│   ├── tsconfig.json         # TypeScript configuration
│   ├── .env.example          # Environment variables template
│   └── README.md             # Frontend documentation
│
├── tasks/                      # Project management
│   ├── 0001-prd-project-setup.md        # Phase 1 PRD
│   ├── tasks-0001-prd-project-setup.md  # Phase 1 tasks
│   ├── 0002-prd-simple-agent.md         # Phase 2 PRD
│   ├── tasks-0002-prd-simple-agent.md   # Phase 2 tasks
│   ├── 0003-prd-multi-agent-supervisor.md     # Phase 3 PRD ✅
│   └── tasks-0003-prd-multi-agent-supervisor.md # Phase 3 tasks ✅
│
├── .github/                    # GitHub workflows and templates
│   └── workflows/             # CI/CD pipelines
│
├── PHASE3_MULTI_AGENT_DEMO_GUIDE.md  # Phase 3 demo guide ✅
├── docker-compose.yml         # Docker orchestration
├── ARCHITECTURE.md            # System architecture docs
├── FLOWCHARTS.md             # Process flow diagrams
├── PHASED_DEVELOPMENT_GUIDE.md # Development roadmap
├── CONTRIBUTING.md           # Contribution guidelines
└── README.md                 # This file (Phase 3 ✅)
```

**Key Points:**
- **Backend** and **Frontend** are completely independent and can be developed separately
- Each has its own dependencies, environment variables, and documentation
- They communicate via REST API (backend exposes endpoints, frontend consumes them)
- Both can be run independently or together using Docker Compose

---

## 🛠️ Setup Instructions

### Backend Setup (Python + FastAPI)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate it
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   nano .env  # or use your preferred editor
   ```
   
   **Required variables:**
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ENVIRONMENT=development
   LOG_LEVEL=INFO
   ```

5. **Run the backend:**
   ```bash
   uvicorn main:app --reload
   # Or simply:
   python main.py
   ```

6. **Verify it's working:**
   - Open http://localhost:8000/health
   - Open http://localhost:8000/docs (interactive API documentation)

**📚 For detailed backend documentation, see [backend/README.md](./backend/README.md)**

---

### Frontend Setup (Next.js + TypeScript)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   pnpm install
   # Or if you prefer npm:
   npm install
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit if needed (default backend URL is http://localhost:8000)
   ```

4. **Run the development server:**
   ```bash
   pnpm dev
   # Or with npm:
   npm run dev
   ```

5. **Verify it's working:**
   - Open http://localhost:3000
   - You should see the "Customer Service AI" welcome page

**📚 For detailed frontend documentation, see [frontend/README.md](./frontend/README.md)**

---

### Docker Setup (Optional)

To run both backend and frontend using Docker:

```bash
# From the project root
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Note**: Docker Compose configuration will be added in a future task.

---

## 🔄 Development Workflow

### Starting Development

1. **Start backend** (Terminal 1):
   ```bash
   cd backend
   source venv/bin/activate  # Activate venv
   uvicorn main:app --reload
   ```

2. **Start frontend** (Terminal 2):
   ```bash
   cd frontend
   pnpm dev
   ```

3. **Start coding!**
   - Backend changes auto-reload with `--reload` flag
   - Frontend changes auto-reload with Fast Refresh

### Code Quality

**Backend (Python):**
```bash
cd backend
# Lint and format
ruff check .
ruff format .

# Run tests
pytest
```

**Frontend (TypeScript):**
```bash
cd frontend
# Lint
pnpm lint

# Type check
pnpm build  # This runs TypeScript compiler
```

### Git Workflow

This project follows **GitHub Flow** with feature branches:

1. **Create feature branch** from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/your-feature-name
   ```

2. **Make changes and commit** using Conventional Commits:
   ```bash
   git add .
   git commit -m "feat: add user authentication" \
              -m "- Added login endpoint" \
              -m "- Added JWT token generation"
   ```

3. **Push and merge**:
   ```bash
   git push -u origin feat/your-feature-name
   git checkout main
   git merge --no-ff feat/your-feature-name
   git push origin main
   ```

**📚 For detailed contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md)**

### GitHub Branch Protection Rules

To maintain code quality and prevent accidental changes to the main branch, it's recommended to enable branch protection rules on GitHub.

**⚠️ Note**: Branch protection rules can only be configured through the GitHub web interface and require repository admin access.

#### Recommended Protection Rules for `main` Branch

1. **Navigate to Repository Settings:**
   - Go to your repository on GitHub
   - Click **Settings** (requires admin access)
   - Click **Branches** in the left sidebar
   - Click **Add branch protection rule**

2. **Configure Branch Name Pattern:**
   - Set **Branch name pattern** to: `main`

3. **Enable Required Status Checks:**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - Select required checks:
     - `Backend (Python) - Ruff`
     - `Frontend (TypeScript) - ESLint`
     - `Backend Tests (pytest)` (optional but recommended)
     - `Frontend TypeScript Check` (optional but recommended)

4. **Enable Pull Request Requirements (Optional but Recommended):**
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals**: Set to 1 or more reviewers
   - ✅ **Dismiss stale pull request approvals when new commits are pushed**

5. **Additional Recommended Settings:**
   - ✅ **Require conversation resolution before merging**
   - ✅ **Do not allow bypassing the above settings** (keeps even admins accountable)
   - ✅ **Restrict who can push to matching branches** (optional for team environments)

6. **Click "Create"** to save the protection rules

#### What This Protects Against

- ❌ Direct pushes to `main` without review (if PR required)
- ❌ Merging code that fails linting checks
- ❌ Merging code that fails tests
- ❌ Merging code with unresolved review comments
- ❌ Accidentally force-pushing to `main`

#### For Solo Development

If you're working alone and find PR requirements too restrictive:

- Enable **only** the required status checks (linting and tests)
- Skip the "Require pull request" option
- You can still push directly to `main`, but linting/tests must pass

#### Testing Branch Protection

After enabling, try to:
1. Push directly to `main` - Should be blocked if PR required
2. Create a PR with failing tests - Should show checks failing
3. Fix the issues and push again - Checks should pass and allow merge

#### More Information

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Status Checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)

---

## 🧪 Testing

### Automated Tests

**Backend Tests (54 passing, 64% coverage):**

```bash
cd backend
source venv/bin/activate

# Run all tests (unit only, fast)
pytest

# Run with integration tests (mocked, no tokens used)
pytest --run-integration

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test suites
pytest tests/test_main.py -v              # API + routing integration (37 tests)
pytest tests/test_supervisor.py -v        # Supervisor unit tests (15 tests)
pytest tests/test_technical_worker.py -v  # Worker unit tests (19 tests)
pytest tests/test_agent.py -v             # Phase 2 agent tests (10 tests)

# View coverage report
open htmlcov/index.html
```

**Test Breakdown:**
- **Unit Tests (44 tests)**: Fast, mocked, no API calls
  - 15 supervisor tests
  - 19 technical worker tests
  - 10 Phase 2 agent tests (reference)
- **Integration Tests (10 tests)**: Full endpoint routing tests (mocked supervisor)
  - Technical query routing
  - General query handling
  - Context maintenance across routing
  - Error handling scenarios

**Frontend Linting & Type Checks:**

```bash
cd frontend

# Run ESLint
pnpm lint

# TypeScript type checking
pnpm tsc --noEmit
```

**Run All Tests (CI-style):**

```bash
# From project root
./scripts/test-all.sh

# Or use Make commands
make test        # Run all tests
make lint        # Run all linters
```

### Manual Testing Guide

**Multi-Agent Routing Testing (Phase 3):**

1. **Start the application:**
   ```bash
   # Terminal 1: Backend
   cd backend && source venv/bin/activate && uvicorn main:app --reload
   
   # Terminal 2: Frontend
   cd frontend && pnpm dev
   ```

2. **Test technical query routing:**
   - Open http://localhost:3000
   - Type: "Getting Error 500 when logging in"
   - **Expected**: Technical troubleshooting response
   - **Check logs**: Should see `🔀 ROUTING: Query routed to worker agent`

3. **Test general query direct handling:**
   - Type: "Hello! How are you?"
   - **Expected**: Friendly greeting response
   - **Check logs**: Should see `✋ DIRECT: Supervisor handled query directly`

4. **Test conversation memory across routing:**
   - Type: "I'm having an installation problem"
   - Type: "What did I just say?"
   - **Expected**: AI remembers the installation problem
   - **Verify**: Context maintained across routing

5. **Test session persistence:**
   - Refresh the page (F5)
   - Type: "Do you remember my issue?"
   - **Verify**: AI still remembers (session persisted)

6. **Test clear conversation:**
   - Click "Clear Conversation" button
   - Type: "What was my problem?"
   - **Verify**: AI doesn't remember (new session)

**Test Routing with Script:**
```bash
cd backend
chmod +x test_routing_logs.sh
./test_routing_logs.sh
# Watch logs for 🔀 ROUTING and ✋ DIRECT indicators
```

**For comprehensive manual testing scenarios, see [MANUAL_TESTING.md](./MANUAL_TESTING.md)**

---

## 🐛 Troubleshooting

### Common Issues

#### Backend: Module Not Found
```bash
# Make sure virtual environment is activated
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

#### Backend: OpenAI API Key Error
```bash
# Check your .env file has the key set
cat backend/.env | grep OPENAI_API_KEY

# Make sure it's not quoted and has no spaces
OPENAI_API_KEY=sk-...
```

#### Backend: Port 8000 Already in Use
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --reload --port 8001
```

#### Frontend: Module Not Found
```bash
# Clear cache and reinstall
cd frontend
rm -rf .next node_modules
pnpm install
```

#### Frontend: Port 3000 Already in Use
```bash
# Use a different port
pnpm dev -- -p 3001
```

#### Python SSL Certificate Error (macOS)
```bash
# Install Python certificates
/Applications/Python\ 3.*/Install\ Certificates.command
```

### Debug Mode

**Backend:**
```bash
# Set LOG_LEVEL=DEBUG in .env
LOG_LEVEL=DEBUG

# Or run with debug logging
uvicorn main:app --reload --log-level debug
```

**Frontend:**
```bash
# Next.js shows detailed errors in development mode by default
pnpm dev
```

### Enable LangSmith Tracing (Recommended for Debugging Agents)

Add to `backend/.env`:
```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=customer-service-ai
```

View execution traces at: https://smith.langchain.com/

---

## 📚 Documentation

This project includes comprehensive documentation:

| Document | Description |
|----------|-------------|
| **[README.md](./README.md)** | This file - Project overview, quick start, and Phase 2 features |
| **[MANUAL_TESTING.md](./MANUAL_TESTING.md)** | **NEW** - Step-by-step manual testing guide with 10 test cases |
| **[backend/README.md](./backend/README.md)** | **UPDATED** - Backend setup, /chat API docs, LangSmith tracing |
| **[frontend/README.md](./frontend/README.md)** | Frontend setup, component guide, and styling documentation |
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Complete system architecture, design patterns, and technical decisions |
| **[FLOWCHARTS.md](./FLOWCHARTS.md)** | Visual process flows, sequence diagrams, and system interactions |
| **[PHASED_DEVELOPMENT_GUIDE.md](./PHASED_DEVELOPMENT_GUIDE.md)** | Development roadmap with phases, milestones, and implementation details |
| **[CONTRIBUTING.md](./CONTRIBUTING.md)** | Contribution guidelines, Git workflow, and coding standards |
| **[DEVELOPMENT.md](./DEVELOPMENT.md)** | **NEW** - Developer setup guide and best practices |
| **[CI_VERIFICATION.md](./CI_VERIFICATION.md)** | **NEW** - Local vs CI test command mapping |
| **[Makefile](./Makefile)** | **NEW** - Convenient make commands for common tasks |
| **[agentic-customer-specs.md](./agentic-customer-specs.md)** | Original project specifications and requirements |
| **[tasks/](./tasks/)** | PRDs and task lists for feature development |

---

## 🤝 Contributing

We follow a structured development process:

1. **PRDs (Product Requirements Documents)**: Define what we're building
2. **Task Lists**: Break down PRDs into actionable tasks
3. **Feature Branches**: One branch per sub-task
4. **Conventional Commits**: Clear, semantic commit messages
5. **Testing**: All features must include tests
6. **Documentation**: Update relevant docs with changes

**For complete contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md)**

---

## 🎓 Project Context

This project is part of the **ASU VibeCoding** curriculum, demonstrating:

- Modern full-stack development
- AI/ML integration with LangChain v1.0+
- Multi-agent system design
- REST API development
- TypeScript and type safety
- Responsive web design
- DevOps practices (Docker, CI/CD)

---

## 📄 License

This project is part of the ASU VibeCoding curriculum.

---

## 🔗 Quick Links

- **Backend API Docs**: http://localhost:8000/docs (when running)
- **LangChain Documentation**: https://docs.langchain.com/
- **LangGraph Guide**: https://docs.langchain.com/oss/python/langgraph
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## 📞 Support

For questions or issues:

1. Check this README and relevant documentation
2. Review the specific component README (backend or frontend)
3. Enable debug logging and LangSmith tracing
4. Check GitHub issues for known problems
5. Review test files for usage examples

---

## 🎉 MVP Complete - All 6 Phases Finished!

### **What We Built:**

**Phase 1-4: Foundation** ✅
- ✅ FastAPI backend + Next.js frontend infrastructure
- ✅ Simple agent foundation with LangChain v1.0+
- ✅ Multi-agent supervisor architecture
- ✅ 4 specialized worker agents (Technical, Billing, Compliance, General)

**Phase 5: RAG/CAG Integration** ✅
- ✅ Pure RAG for Technical & General (ChromaDB vector retrieval)
- ✅ Hybrid RAG/CAG for Billing (first query retrieves, then caches)
- ✅ Pure CAG for Compliance (pre-loaded static documents)
- ✅ 8 sample documents across 4 domains
- ✅ Document indexing pipeline (`index_documents.py`)

**Phase 6: Multi-Provider LLMs & Streaming** ✅
- ✅ AWS Bedrock Nova Lite for supervisor routing ($0.06/1M tokens)
- ✅ OpenAI GPT-4o-mini for worker generation ($0.15/1M tokens)
- ✅ Real-time SSE streaming with token-by-token display
- ✅ User toggle between streaming/standard modes
- ✅ 11% cost savings vs single-provider strategy

### **Final System Features:**

🤖 **Multi-Provider LLM Strategy**
- AWS Nova Lite for routing decisions (60% cheaper)
- OpenAI GPT-4o-mini for response generation
- Automatic fallback mechanism

🔄 **Real-Time Streaming**
- Server-Sent Events (SSE) implementation
- Token-by-token response display
- User-controlled streaming toggle

📚 **Advanced Knowledge System**
- 3 RAG/CAG strategies optimized per domain
- ChromaDB vector store with 8 documents
- Session-based caching for billing queries

🎯 **4 Specialized Agents**
- Technical Support (Pure RAG)
- Billing Support (Hybrid RAG/CAG)
- Compliance (Pure CAG)
- General Information (Pure RAG)

🧪 **Production Quality**
- 145 automated tests (91% coverage)
- Comprehensive error handling
- Full TypeScript + Pydantic validation
- LangSmith tracing support

### **Development Timeline:**
- ✅ **Phase 1**: Project Setup & Infrastructure
- ✅ **Phase 2**: Simple Agent Foundation (20/20 tasks)
- ✅ **Phase 3**: Multi-Agent Supervisor (13/13 tasks)
- ✅ **Phase 4**: Additional Workers (11/11 tasks)
- ✅ **Phase 5**: RAG/CAG Integration (10/10 tasks)
- ✅ **Phase 6**: Multi-Provider LLMs & Streaming (3/3 tasks)

### **Ready for Submission:**
- ✅ GitHub repository with complete source code
- ✅ Comprehensive README and setup instructions
- 📹 **Next**: Record 5-10 minute YouTube demo video

### **System Architecture:**
```
User → Frontend (Streaming Toggle) → Backend API (/chat or /chat/stream)
        ↓
    Supervisor (AWS Nova Lite + fallback)
        ↓
    ┌───────┬─────────┬───────────┬─────────┐
    │Technical│Billing │Compliance│ General │
    │(Pure RAG)│(Hybrid)│(Pure CAG)│(Pure RAG)│
    └───────┴─────────┴───────────┴─────────┘
        ↓
    ChromaDB / Cache / Pre-loaded Docs
```

---

**Version**: 1.0.0 (MVP Complete)  
**Last Updated**: November 4, 2025  
**Status**: Phase 6 Complete ✅ - PRODUCTION READY MVP  
**LangChain Version**: 1.0+  
**All Requirements Met**: Backend, Frontend, RAG/CAG, Multi-Provider LLMs, Streaming

---

**Built with ❤️ using Vibe Coding Strategy**  
**ASU VibeCoding Project - Advanced Customer Service AI**
