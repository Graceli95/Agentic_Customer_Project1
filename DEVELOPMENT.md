# Development Guide

This document describes the development tools and workflows for the Agentic Customer Service project.

## 🚀 Quick Start

```bash
# Install all dependencies
make install

# Run all tests (matches CI exactly)
make test

# Run all linters
make lint

# Format code
make format
```

## 📋 Available Commands

### Testing (matches GitHub Actions CI)

```bash
make test              # Run ALL tests (backend + frontend)
make test-backend      # Run backend tests only (pytest)
make test-frontend     # Run frontend tests (Phase 3)
```

### Linting (matches GitHub Actions CI)

```bash
make lint              # Run ALL linters
make lint-backend      # Ruff linter (Python)
make lint-frontend     # ESLint + TypeScript (Frontend)
```

### Formatting

```bash
make format            # Format ALL code
make format-backend    # Ruff formatter (Python)
```

### Running Services

```bash
make run-backend       # Start FastAPI server (port 8000)
make run-frontend      # Start Next.js dev server (port 3000)
```

## 🪝 Pre-commit Hooks (Recommended)

Install pre-commit hooks to automatically run tests before each commit:

```bash
make setup-hooks
```

This will:
- ✅ Run Ruff linter and formatter on Python files
- ✅ Run ESLint on TypeScript files
- ✅ Run TypeScript compiler
- ✅ Run pytest on backend
- ✅ Check for trailing whitespace, large files, etc.

The hooks run automatically when you `git commit`. If any check fails, the commit is blocked.

## 🧪 Test Script (Alternative to Make)

You can also run the comprehensive test script directly:

```bash
./scripts/test-all.sh
```

This script:
- Runs all linters (Ruff, ESLint, TypeScript)
- Runs all tests (pytest)
- Provides colored output showing pass/fail status
- Exits with error code if any check fails

## 🎯 Best Practices

### Before Committing

**Always run tests locally before pushing:**

```bash
make test
```

This ensures your code will pass GitHub Actions CI.

### Formatting

**Run formatter to fix style issues:**

```bash
make format
```

This will automatically fix most linting issues.

### Branch Workflow

1. Create a feature branch: `git checkout -b feat/my-feature`
2. Make your changes
3. Run tests: `make test`
4. Run linter: `make lint`
5. Commit changes
6. Push and create PR

## 🔧 CI/CD Pipeline

Our GitHub Actions workflow runs:

1. **Backend (Python) - Ruff**: Linter check
2. **Backend (Python) - Ruff**: Formatter check
3. **Frontend (TypeScript) - ESLint**: Linter check
4. **Frontend (TypeScript) - TSC**: Type check
5. **Backend Tests (pytest)**: All unit tests

**Local commands match CI exactly** - if `make test` and `make lint` pass locally, CI will pass.

## 📁 Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── agents/          # LangChain agents
│   ├── tests/           # Pytest tests
│   └── requirements.txt # Python dependencies
├── frontend/            # Next.js frontend
│   ├── app/            # Next.js app directory
│   ├── components/     # React components
│   └── lib/            # Utilities
├── scripts/            # Development scripts
│   └── test-all.sh    # Comprehensive test script
├── .pre-commit-config.yaml  # Pre-commit hooks
├── Makefile            # Development commands
└── DEVELOPMENT.md      # This file
```

## 🐛 Troubleshooting

### "command not found: make"

Install make:
- **macOS**: Already installed
- **Linux**: `sudo apt-get install make`
- **Windows**: Use WSL or Git Bash

### "pytest not found"

Activate the virtual environment:

```bash
cd backend
source venv/bin/activate
```

### "ruff not found"

Install backend dependencies:

```bash
make install
```

Or manually:

```bash
cd backend
pip install -r requirements.txt
```

### Pre-commit hooks not running

Install pre-commit:

```bash
make setup-hooks
```

## 📚 Additional Resources

- [Backend README](./backend/README.md) - Backend setup and API docs
- [Frontend README](./frontend/README.md) - Frontend setup and components
- [Main README](./README.md) - Project overview
- [Task List](./tasks/tasks-0002-prd-simple-agent-foundation.md) - Phase 2 tasks

