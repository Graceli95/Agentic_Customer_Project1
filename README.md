# Advanced Multi-Agent Customer Service AI

An intelligent, agentic customer service system powered by LangChain v1.0+ and LangGraph. This system uses specialized AI agents to handle technical support, billing inquiries, and compliance questions through natural language conversations.

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

This project implements a sophisticated customer service AI system using multiple specialized agents that can:

- **Handle Technical Support**: Answer technical questions using product documentation
- **Process Billing Inquiries**: Assist with billing, payments, and account questions
- **Answer Compliance Questions**: Provide information about policies, terms, and regulations
- **Route Intelligently**: Automatically route queries to the appropriate specialized agent
- **Maintain Context**: Keep conversation history for natural, contextual interactions

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

This system uses a **supervisor pattern** where a main coordinator agent routes queries to specialized worker agents:

```
User Query → Supervisor Agent → [Technical | Billing | Compliance] Agent → Response
```

Each specialized agent has:
- **Domain-specific knowledge**: Access to relevant document repositories
- **Specialized tools**: Custom functions for their domain
- **RAG capabilities**: Retrieve and use information from documents
- **Conversation memory**: Maintain context across interactions

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
├── CONTRIBUTING.md           # Contribution guidelines (to be created)
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

**📚 For detailed contribution guidelines, see CONTRIBUTING.md** (to be created)

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

### Frontend Tests

```bash
cd frontend

# Run tests (when configured)
pnpm test

# Run linting
pnpm lint
```

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
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Complete system architecture, design patterns, and technical decisions |
| **[FLOWCHARTS.md](./FLOWCHARTS.md)** | Visual process flows, sequence diagrams, and system interactions |
| **[PHASED_DEVELOPMENT_GUIDE.md](./PHASED_DEVELOPMENT_GUIDE.md)** | Development roadmap with phases, milestones, and implementation details |
| **[backend/README.md](./backend/README.md)** | Backend-specific setup, API documentation, and development guidelines |
| **[frontend/README.md](./frontend/README.md)** | Frontend-specific setup, component guide, and styling documentation |
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

**Full contribution guidelines coming soon in CONTRIBUTING.md**

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

**Version**: 1.0.0  
**Last Updated**: November 2, 2025  
**Status**: Active Development - Phase 1 Complete ✅

---

**Built with ❤️ by the ASU VibeCoding Team**
