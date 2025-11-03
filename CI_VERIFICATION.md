# CI Verification Guide

This document ensures local tests match GitHub Actions CI **exactly**.

## 🎯 Quick Verification

Run this command before every commit:

```bash
make lint && make test
```

Or use the comprehensive script:

```bash
./scripts/test-all.sh
```

## ✅ GitHub Actions CI Jobs → Local Commands Mapping

### Backend (Python) - Ruff

**GitHub Actions:**
```bash
cd backend
ruff check .
ruff format --check .
```

**Local Command:**
```bash
make lint-backend
```

---

### Frontend (TypeScript) - ESLint

**GitHub Actions:**
```bash
cd frontend
pnpm lint  # runs: eslint . --ext .ts,.tsx --max-warnings=0
```

**Local Command:**
```bash
cd frontend
npx eslint . --ext .ts,.tsx --max-warnings=0
```

Or:
```bash
make lint-frontend
```

---

### Backend Tests (pytest)

**GitHub Actions:**
```bash
cd backend
pytest -v
```

**Local Command:**
```bash
make test-backend
```

---

### Frontend TypeScript Check

**GitHub Actions:**
```bash
cd frontend
pnpm build  # includes tsc --noEmit
```

**Local Command:**
```bash
cd frontend
npx tsc --noEmit
```

Or:
```bash
make lint-frontend  # includes TypeScript check
```

---

## 📊 Complete CI Checklist

Before pushing code, verify all checks pass:

- [ ] **Backend Ruff Linter**: `cd backend && ruff check .`
- [ ] **Backend Ruff Formatter**: `cd backend && ruff format --check .`
- [ ] **Backend Tests**: `cd backend && pytest -v`
- [ ] **Frontend ESLint**: `cd frontend && npx eslint . --ext .ts,.tsx --max-warnings=0`
- [ ] **Frontend TypeScript**: `cd frontend && npx tsc --noEmit`

**Or simply run:**
```bash
make lint && make test
```

---

## 🛠️ Fixing Issues

### Ruff Formatter Failures

If `ruff format --check` fails:

```bash
make format
# or
cd backend && ruff format .
```

This will automatically fix all formatting issues.

### ESLint Failures

If ESLint fails:

```bash
cd frontend && npx eslint . --ext .ts,.tsx --fix
```

Some issues may need manual fixing.

### TypeScript Failures

TypeScript errors must be fixed manually. Common issues:

- Missing type annotations
- Type-only imports needed: `import type { X } from 'y'`
- Missing null checks

### Pytest Failures

Fix the failing tests. Run individual tests:

```bash
cd backend
pytest tests/test_main.py::test_name -v
```

---

## 🪝 Automated Enforcement (Recommended)

Install pre-commit hooks to automatically check on every commit:

```bash
make setup-hooks
```

This will:
1. Install pre-commit package
2. Set up git hooks
3. Run all checks automatically on `git commit`

If any check fails, the commit is blocked.

---

## 📝 CI/CD Pipeline Details

### Workflow File

`.github/workflows/lint.yml`

### Jobs Run on Every Push/PR to Main:

1. **backend-lint**: Ruff linter + formatter check
2. **frontend-lint**: ESLint
3. **backend-test**: pytest
4. **frontend-typecheck**: TypeScript compiler

All must pass for CI to succeed.

---

## 🚨 Common Issues

### Issue: "Local tests pass but CI fails"

**Cause**: Local commands don't match CI exactly

**Solution**: Use commands from this document or `make` commands

---

### Issue: "Ruff formatter check fails"

**Cause**: Code not formatted consistently

**Solution**: 
```bash
make format
git add .
git commit
```

---

### Issue: "TypeScript builds locally but fails in CI"

**Cause**: Using `npm` locally but CI uses `pnpm`

**Solution**: Use consistent package manager or test with:
```bash
cd frontend && npx tsc --noEmit
```

---

## 🔄 Updating CI Commands

If GitHub Actions workflow changes, update these locations:

1. **`scripts/test-all.sh`** - Comprehensive test script
2. **`Makefile`** - Make commands
3. **`.pre-commit-config.yaml`** - Pre-commit hooks
4. **This document** - CI verification guide

---

## 📈 Coverage Goals

- **Backend**: >70% code coverage (current: ~69%)
- **Frontend**: Tests coming in Phase 3
- **Linters**: 0 errors, 0 warnings

---

## ✨ Best Practices

1. **Always run `make lint` before committing**
2. **Run `make test` before pushing**
3. **Use `make format` to auto-fix formatting**
4. **Install pre-commit hooks** (`make setup-hooks`)
5. **Check this guide if CI fails**

---

## 🎯 Summary

| GitHub Actions Job | Local Command | Purpose |
|---|---|---|
| Backend Ruff | `make lint-backend` | Lint + format check |
| Frontend ESLint | `make lint-frontend` | Lint + type check |
| Backend Tests | `make test-backend` | Run pytest |
| All Together | `make lint && make test` | Complete verification |

**Golden Rule**: If `make lint && make test` passes locally, CI will pass! ✅

