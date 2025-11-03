#!/bin/bash
# Comprehensive test script that matches GitHub Actions CI
# Run this before committing to ensure all checks pass

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================================"
echo "🧪 Running Full Test Suite (matches GitHub Actions CI)"
echo "======================================================================"
echo ""

# Track overall status
FAILED=0

# ============================================================================
# Backend Tests
# ============================================================================

echo "📦 BACKEND TESTS"
echo "----------------------------------------------------------------------"

# 1. Ruff Linter
echo "1️⃣  Running Ruff linter..."
cd backend
if source venv/bin/activate && ruff check .; then
    echo -e "${GREEN}✅ Ruff: PASSED${NC}"
else
    echo -e "${RED}❌ Ruff: FAILED${NC}"
    FAILED=1
fi
echo ""

# 2. Pytest
echo "2️⃣  Running pytest..."
if source venv/bin/activate && pytest tests/ -v --tb=short --maxfail=1; then
    echo -e "${GREEN}✅ Pytest: PASSED${NC}"
else
    echo -e "${RED}❌ Pytest: FAILED${NC}"
    FAILED=1
fi
cd ..
echo ""

# ============================================================================
# Frontend Tests
# ============================================================================

echo "🎨 FRONTEND TESTS"
echo "----------------------------------------------------------------------"

# 3. ESLint
echo "3️⃣  Running ESLint..."
cd frontend
if npx eslint . --ext .ts,.tsx --max-warnings=0; then
    echo -e "${GREEN}✅ ESLint: PASSED${NC}"
else
    echo -e "${RED}❌ ESLint: FAILED${NC}"
    FAILED=1
fi
echo ""

# 4. TypeScript Check
echo "4️⃣  Running TypeScript compiler..."
if npx tsc --noEmit; then
    echo -e "${GREEN}✅ TypeScript: PASSED${NC}"
else
    echo -e "${RED}❌ TypeScript: FAILED${NC}"
    FAILED=1
fi
cd ..
echo ""

# ============================================================================
# Summary
# ============================================================================

echo "======================================================================"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED!${NC}"
    echo "======================================================================"
    echo "✨ Your code is ready to commit and push!"
    echo ""
    exit 0
else
    echo -e "${RED}❌ SOME CHECKS FAILED!${NC}"
    echo "======================================================================"
    echo "⚠️  Please fix the errors above before committing."
    echo ""
    exit 1
fi

