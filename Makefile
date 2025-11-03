# Makefile for Agentic Customer Service Project
# Provides convenient commands matching CI/CD pipeline

.PHONY: help test test-backend test-frontend lint lint-backend lint-frontend format format-backend install

# Default target
help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║  Agentic Customer Service - Development Commands              ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 Setup:"
	@echo "  make install           Install all dependencies (backend + frontend)"
	@echo ""
	@echo "🧪 Testing (matches GitHub Actions):"
	@echo "  make test              Run ALL tests (backend + frontend)"
	@echo "  make test-backend      Run backend tests (pytest)"
	@echo "  make test-frontend     Run frontend tests (coming in Phase 3)"
	@echo ""
	@echo "🔍 Linting (matches GitHub Actions):"
	@echo "  make lint              Run ALL linters (backend + frontend)"
	@echo "  make lint-backend      Run Ruff linter on backend"
	@echo "  make lint-frontend     Run ESLint + TypeScript on frontend"
	@echo ""
	@echo "✨ Formatting:"
	@echo "  make format            Format ALL code (backend + frontend)"
	@echo "  make format-backend    Format backend with Ruff"
	@echo ""
	@echo "🚀 Running:"
	@echo "  make run-backend       Start backend server (FastAPI)"
	@echo "  make run-frontend      Start frontend dev server (Next.js)"
	@echo ""

# ============================================================================
# Installation
# ============================================================================

install:
	@echo "📦 Installing backend dependencies..."
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ All dependencies installed!"

# ============================================================================
# Testing (matches GitHub Actions CI)
# ============================================================================

test:
	@echo "🧪 Running full test suite (matches CI)..."
	@./scripts/test-all.sh

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && source venv/bin/activate && pytest tests/ -v --tb=short

test-frontend:
	@echo "⚠️  Frontend tests coming in Phase 3"

# ============================================================================
# Linting (matches GitHub Actions CI)
# ============================================================================

lint: lint-backend lint-frontend
	@echo "✅ All linters passed!"

lint-backend:
	@echo "🔍 Running Ruff linter..."
	cd backend && source venv/bin/activate && ruff check .

lint-frontend:
	@echo "🔍 Running ESLint..."
	cd frontend && npx eslint . --ext .ts,.tsx --max-warnings=0
	@echo "🔍 Running TypeScript check..."
	cd frontend && npx tsc --noEmit

# ============================================================================
# Formatting
# ============================================================================

format: format-backend
	@echo "✨ Code formatting complete!"

format-backend:
	@echo "✨ Formatting backend with Ruff..."
	cd backend && source venv/bin/activate && ruff format .

# ============================================================================
# Running services
# ============================================================================

run-backend:
	@echo "🚀 Starting backend server..."
	cd backend && source venv/bin/activate && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	@echo "🚀 Starting frontend dev server..."
	cd frontend && npm run dev

# ============================================================================
# Pre-commit setup
# ============================================================================

setup-hooks:
	@echo "🪝 Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	@echo "✅ Pre-commit hooks installed!"
	@echo "   Hooks will run automatically on 'git commit'"
	@echo "   Run manually with: pre-commit run --all-files"

