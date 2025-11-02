# Backend - Advanced Customer Service AI

FastAPI backend for the multi-agent customer service AI system powered by LangChain v1.0+ and LangGraph.

## Overview

This backend provides REST API endpoints for an intelligent customer service system that uses multiple specialized AI agents to handle:
- Technical support inquiries
- Billing and payment questions
- Compliance and policy information
- General customer service requests

**Key Technologies:**
- **FastAPI** - Modern, high-performance web framework
- **LangChain v1.0+** - LLM application framework
- **LangGraph** - Agent orchestration and workflow management
- **ChromaDB** - Vector database for document retrieval
- **Pydantic** - Data validation and settings management
- **Pytest** - Testing framework

## Project Structure

```
backend/
├── agents/                  # Agent modules
│   ├── __init__.py
│   └── workers/            # Specialized worker agents
│       └── __init__.py
├── data/                   # Data and documents
│   ├── __init__.py
│   └── docs/              # Document storage
│       ├── billing/       # Billing-related documents
│       ├── compliance/    # Compliance documents
│       └── technical/     # Technical documentation
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_main.py       # API endpoint tests
├── utils/                  # Utility functions
│   └── __init__.py
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── Dockerfile             # Container configuration
├── pytest.ini             # Pytest configuration
└── README.md              # This file
```

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

**Required Environment Variables:**
- `OPENAI_API_KEY` - OpenAI API key for LLM access
- `ENVIRONMENT` - Environment name (development/staging/production)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)

**Optional Environment Variables:**
- `AWS_ACCESS_KEY_ID` - AWS credentials for Bedrock
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_DEFAULT_REGION` - AWS region
- `LANGSMITH_API_KEY` - LangSmith tracing (recommended for debugging)
- `LANGSMITH_TRACING` - Enable LangSmith tracing (true/false)
- `LANGSMITH_PROJECT` - LangSmith project name

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
- `@pytest.mark.unit` - Fast, isolated unit tests
- `@pytest.mark.integration` - Integration tests (may require external services)
- `@pytest.mark.slow` - Slow-running tests

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
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

### Available Endpoints

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
  "message": "Welcome to Advanced Customer Service AI",
  "docs": "/docs",
  "health": "/health",
  "version": "1.0.0"
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

### Adding New Agents

1. Create agent module in `agents/workers/`
2. Use LangChain v1.0 `create_agent()` helper
3. Define tools with `@tool` decorator
4. Write unit tests for the agent
5. Document agent purpose and usage

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

### LangSmith Tracing

Enable LangSmith for detailed agent execution traces:

```bash
# Add to .env file
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=customer-service-ai

# View traces at https://smith.langchain.com/
```

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

**Version**: 1.0.0  
**Last Updated**: November 2, 2025  
**LangChain Version**: 1.0+

