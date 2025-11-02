# Backend - Advanced Customer Service AI

FastAPI-based backend for the multi-agent customer service system powered by LangChain v1.0+ and LangGraph.

## 📁 Project Structure

```
backend/
├── agents/                  # Multi-agent system
│   ├── orchestrator.py     # Supervisor agent and coordination
│   └── workers/            # Specialized worker agents
│       ├── technical_support_agent.py
│       ├── billing_support_agent.py
│       └── policy_compliance_agent.py
├── data/                   # Data and vector storage
│   ├── vector_store.py    # ChromaDB initialization
│   ├── ingest_data.py     # Document ingestion pipeline
│   └── docs/              # Source documents
│       ├── technical/     # Technical documentation
│       ├── billing/       # Billing policies
│       └── compliance/    # ToS, Privacy Policy
├── utils/                  # Utility functions
│   ├── config.py          # Configuration management
│   └── logger.py          # Logging setup
├── tests/                  # Test suite
│   └── test_main.py       # API tests
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── Dockerfile             # Container configuration
└── pytest.ini             # Test configuration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment tool (venv)

### Installation

1. **Create and activate virtual environment:**

```bash
# Create venv
python -m venv venv

# Activate venv (macOS/Linux)
source venv/bin/activate

# Activate venv (Windows)
venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
# - OPENAI_API_KEY
# - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
# - LANGSMITH_API_KEY (optional but recommended)
```

### Running the Application

**Development mode (with auto-reload):**

```bash
uvicorn main:app --reload
```

**Production mode:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Using Python directly:**

```bash
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Testing

### Run all tests:

```bash
pytest
```

### Run tests with coverage:

```bash
pytest --cov=. --cov-report=html
```

### Run specific test categories:

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Specific test file
pytest tests/test_main.py
```

## 🐳 Docker

### Build the image:

```bash
docker build -t customer-service-ai-backend .
```

### Run the container:

```bash
docker run -d -p 8000:8000 --env-file .env customer-service-ai-backend
```

### Using Docker Compose (from project root):

```bash
docker-compose up backend
```

## 📚 API Endpoints

### Health Check
- **GET** `/health` - Check service health status

### Root
- **GET** `/` - API information and links

### Documentation
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation (ReDoc)

*Note: Chat endpoints will be added in Phase 2*

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options.

**Required:**
- `OPENAI_API_KEY` - OpenAI API key for GPT models
- `AWS_ACCESS_KEY_ID` - AWS access key for Bedrock
- `AWS_SECRET_ACCESS_KEY` - AWS secret key for Bedrock
- `AWS_REGION` - AWS region (e.g., us-east-1)

**Optional:**
- `LANGSMITH_API_KEY` - LangSmith tracing (recommended for debugging)
- `LANGSMITH_TRACING` - Enable/disable tracing (true/false)
- `LANGSMITH_PROJECT` - LangSmith project name
- `ENVIRONMENT` - Environment name (development/staging/production)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `CORS_ORIGINS` - Allowed CORS origins

## 🧰 Development Tools

### Linting

```bash
# Check code style
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Code Formatting

```bash
# Check formatting (when black is added)
black --check .

# Format code
black .
```

## 📖 Technology Stack

- **Framework**: FastAPI 0.104+
- **AI/LLM**: LangChain 1.0+, LangGraph 1.0+
- **Vector DB**: ChromaDB 0.4+
- **LLM Providers**: OpenAI (GPT-5), AWS Bedrock (Nova Lite, Claude)
- **Testing**: pytest, pytest-asyncio
- **Linting**: ruff
- **Server**: Uvicorn

## 🔗 Related Documentation

- [Project Architecture](../docs/ARCHITECTURE.md)
- [Development Guide](../docs/PHASED_DEVELOPMENT_GUIDE.md)
- [API Flowcharts](../docs/FLOWCHARTS.md)
- [Project Specifications](../agentic-customer-specs.md)

## 📝 Notes

- This is Phase 1 (Project Setup). Agent implementation begins in Phase 2.
- LangSmith tracing is highly recommended for debugging agents.
- ChromaDB persistence directory is `./chroma_db` (gitignored).
- API keys should never be committed to version control.

## 🆘 Troubleshooting

### Import errors
Make sure you're in the virtual environment and all dependencies are installed.

### Port already in use
Change the port in `.env` or use: `uvicorn main:app --port 8001`

### CORS errors from frontend
Check that `CORS_ORIGINS` in `.env` includes your frontend URL.

### ChromaDB errors
Ensure the `chroma_db/` directory has proper write permissions.

---

**Version**: 1.0.0  
**Status**: Phase 1 Complete (Project Setup)  
**Next**: Phase 2 (Simple Agent Foundation)

