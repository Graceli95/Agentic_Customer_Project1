# Advanced Multi-Agent Customer Service AI

An intelligent, agentic customer service system powered by LangChain v1.0+ and LangGraph.

**Current Status: Phase 2 Complete ✅** - Simple Agent Foundation with conversation memory and full-stack chat interface.

This system uses AI agents to provide natural language customer service conversations. Phase 2 implements a single conversational agent with memory management, providing a foundation for multi-agent architectures in future phases.

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

## ✨ Phase 2 Features (Current)

**What's Working Now:**

🤖 **Conversational AI Agent**
- Powered by OpenAI GPT-4o-mini
- Natural language understanding
- Context-aware responses

💾 **Session Management**
- UUID-based session IDs
- Conversation memory (InMemorySaver)
- Persistent across page refreshes
- Clear conversation to start fresh

🎨 **Modern Chat Interface**
- Real-time message display
- User/AI message distinction
- Loading indicators ("AI is thinking...")
- Error handling with user-friendly messages
- Character count and validation
- Auto-scroll to latest message

✅ **Production Quality**
- 37 automated tests passing (69% coverage)
- Comprehensive error handling
- LangSmith tracing support
- Type-safe TypeScript frontend
- RESTful API design

**Try It Out:**
1. Start the application (see Quick Start above)
2. Open http://localhost:3000
3. Start chatting with the AI!
4. Test conversation memory: "My name is Alice" → "What is my name?"
5. Clear conversation to start a new session

**Next Phases:**
- **Phase 3**: Multi-agent supervisor pattern
- **Phase 4**: Specialized worker agents (technical, billing, compliance)
- **Phase 5**: RAG with document retrieval
- **Phase 6**: AWS Bedrock integration

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

This project implements an intelligent customer service AI system powered by LangChain v1.0+ and OpenAI's GPT-4o-mini.

**Phase 2 (Current) - Simple Agent Foundation:**

A conversational AI agent with memory management that:

- 💬 **Engages in Natural Conversations**: Understands and responds to customer queries
- 🧠 **Maintains Context**: Remembers conversation history within each session
- 🔄 **Manages Sessions**: UUID-based session IDs for multiple conversations
- ⚡ **Responds in Real-Time**: Fast, context-aware responses via REST API
- 🎨 **Modern Web Interface**: Full-stack Next.js chat interface

**Future Phases (Planned):**

- **Phase 3+**: Multi-agent supervisor pattern
- **Handle Technical Support**: Specialized agent with product documentation (RAG)
- **Process Billing Inquiries**: Dedicated agent for billing and payments
- **Answer Compliance Questions**: Specialized agent for policies and regulations
- **Route Intelligently**: Supervisor agent routes to appropriate specialist

**Key Technologies:**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI + Python 3.11+ | REST API and agent orchestration |
| **AI Framework** | LangChain v1.0+ & LangGraph | Multi-agent system and workflows |
| **Vector Store** | ChromaDB | Document retrieval and semantic search |
| **Frontend** | Next.js 16 + TypeScript | Modern, responsive web interface |
| **Styling** | Tailwind CSS v4 | Beautiful, utility-first design |
| **Package Manager** | pnpm | Fast, efficient dependency management |

---

## 🏗️ Architecture

**Phase 2 Architecture (Current):**

```
┌─────────────────────────────────────────────┐
│         Frontend (Next.js)                  │
│   ┌────────────────────────────────────┐   │
│   │  Chat Interface                    │   │
│   │  • Message display                 │   │
│   │  • Input handling                  │   │
│   │  • Session management (UUID)       │   │
│   └──────────────┬─────────────────────┘   │
└──────────────────┼─────────────────────────┘
                   │ POST /chat
                   │ {message, session_id}
                   ↓
┌─────────────────────────────────────────────┐
│      Backend (FastAPI + LangChain)          │
│   ┌────────────────────────────────────┐   │
│   │  /chat Endpoint                    │   │
│   │  • Request validation              │   │
│   │  • Session ID handling             │   │
│   └──────────────┬─────────────────────┘   │
│                  ↓                          │
│   ┌────────────────────────────────────┐   │
│   │  Customer Service Agent            │   │
│   │  • Model: GPT-4o-mini              │   │
│   │  • Memory: InMemorySaver           │   │
│   │  • Session-based context           │   │
│   └──────────────┬─────────────────────┘   │
│                  ↓                          │
│   ┌────────────────────────────────────┐   │
│   │  Response                          │   │
│   │  {response, session_id}            │   │
│   └────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Key Components:**
- **Single Agent**: One conversational agent handling all queries
- **Session Memory**: InMemorySaver maintains conversation context per session_id
- **REST API**: Simple request/response pattern with FastAPI
- **Type Safety**: Pydantic models for request/response validation

**Future Architecture (Phase 3+):**

Will implement a **supervisor pattern** with specialized worker agents:
```
User Query → Supervisor Agent → [Technical | Billing | Compliance] Agent → Response
```

For detailed architecture information, see:
- 📘 [**ARCHITECTURE.md**](./ARCHITECTURE.md) - Complete system design and patterns
- 📊 [**FLOWCHARTS.md**](./FLOWCHARTS.md) - Visual process flows and diagrams
- 🗺️ [**PHASED_DEVELOPMENT_GUIDE.md**](./PHASED_DEVELOPMENT_GUIDE.md) - Development roadmap

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
│   ├── agents/                 # Agent modules
│   │   └── workers/           # Specialized worker agents
│   ├── data/                   # Data and documents
│   │   └── docs/              # Document repositories
│   │       ├── technical/     # Technical documentation
│   │       ├── billing/       # Billing documents
│   │       └── compliance/    # Compliance documents
│   ├── tests/                  # Backend tests
│   ├── utils/                  # Utility functions
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── Dockerfile            # Backend container config
│   └── README.md             # Backend documentation
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
│   ├── 0001-prd-project-setup.md        # PRD documents
│   └── tasks-0001-prd-project-setup.md  # Task lists
│
├── .github/                    # GitHub workflows and templates
│   └── workflows/             # CI/CD pipelines
│
├── docker-compose.yml         # Docker orchestration (to be created)
├── ARCHITECTURE.md            # System architecture docs
├── FLOWCHARTS.md             # Process flow diagrams
├── PHASED_DEVELOPMENT_GUIDE.md # Development roadmap
├── CONTRIBUTING.md           # Contribution guidelines
└── README.md                 # This file
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

**Backend Tests (37 passing, 69% coverage):**

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test suites
pytest tests/test_main.py -v    # API endpoint tests (27 tests)
pytest tests/test_agent.py -v   # Agent unit tests (10 tests)

# View coverage report
open htmlcov/index.html
```

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

**Conversation Testing:**

1. **Start the application:**
   ```bash
   # Terminal 1: Backend
   cd backend && source venv/bin/activate && uvicorn main:app --reload
   
   # Terminal 2: Frontend
   cd frontend && pnpm dev
   ```

2. **Test basic conversation:**
   - Open http://localhost:3000
   - Type: "Hello, how can you help me?"
   - Verify: AI responds appropriately

3. **Test conversation memory:**
   - Type: "My name is Alice"
   - Type: "What is my name?"
   - Verify: AI remembers "Alice"

4. **Test session persistence:**
   - Refresh the page (F5)
   - Type: "Do you remember my name?"
   - Verify: AI still remembers "Alice"

5. **Test clear conversation:**
   - Click "Clear Conversation" button
   - Type: "What is my name?"
   - Verify: AI doesn't remember (new session)

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

## 🎉 Phase 2 Complete!

**What We Built:**
- ✅ Simple conversational agent with GPT-4o-mini
- ✅ Session-based conversation memory (InMemorySaver)
- ✅ Full-stack chat interface (Next.js + FastAPI)
- ✅ 37 automated tests (69% coverage)
- ✅ LangSmith tracing support
- ✅ Comprehensive documentation
- ✅ CI/CD with GitHub Actions
- ✅ Pre-commit hooks and local testing

**Development Timeline:**
- Phase 1: Project Setup ✅ (Complete)
- Phase 2: Simple Agent Foundation ✅ (Complete - 20/20 tasks)
- Phase 3: Multi-Agent Architecture (Next)

**Test Coverage:**
- Backend: 69% (37 tests passing)
- Frontend: TypeScript + ESLint checks passing
- CI: All checks passing

---

**Version**: 1.0.0 (Phase 2)  
**Last Updated**: November 3, 2025  
**Status**: Phase 2 Complete ✅ - Production Ready  
**LangChain Version**: 1.0+  
**Next Phase**: Multi-Agent Supervisor Pattern (Phase 3)

---

**Built with ❤️ by the ASU VibeCoding Team**
