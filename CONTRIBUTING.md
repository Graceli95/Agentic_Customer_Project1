# Contributing to Advanced Multi-Agent Customer Service AI

Thank you for your interest in contributing to this project! This guide will help you understand our development workflow, coding standards, and contribution process.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Format](#commit-message-format)
- [Sub-task Workflow](#sub-task-workflow)
- [Pull Request Process](#pull-request-process)
- [Code Review Guidelines](#code-review-guidelines)
- [Testing Requirements](#testing-requirements)
- [Code Style Guidelines](#code-style-guidelines)
- [Documentation Standards](#documentation-standards)

---

## Code of Conduct

This project is part of the ASU VibeCoding curriculum. We are committed to providing a welcoming and inclusive environment for all contributors.

**Expected Behavior:**
- Be respectful and constructive in all interactions
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what is best for the project and community

---

## Getting Started

### Prerequisites

Before contributing, ensure you have completed the setup in [README.md](./README.md):

- Python 3.11+ with virtual environment
- Node.js 20+ and pnpm 9+
- OpenAI API key configured
- Backend and frontend running successfully

### Fork and Clone

If working on your own fork (for external contributors):

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/Agentic_Customer_Project1.git
cd Agentic_Customer_Project1

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/Agentic_Customer_Project1.git
```

For team members with direct access:

```bash
# Clone the repository
git clone https://github.com/ORIGINAL_OWNER/Agentic_Customer_Project1.git
cd Agentic_Customer_Project1
```

---

## Development Workflow

This project follows **GitHub Flow**, a lightweight, branch-based workflow:

### Core Principles

1. **`main` branch is always deployable** - All code in `main` should work correctly
2. **Feature branches** - Create descriptive branches from `main` for new work
3. **Commit early and often** - Small, focused commits with clear messages
4. **Merge when ready** - Once tested and reviewed, merge back to `main`
5. **Keep branches short-lived** - Avoid long-running feature branches

### Basic Workflow

```bash
# 1. Start from latest main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feat/your-feature-name

# 3. Make changes and commit
git add .
git commit -m "feat: add user authentication"

# 4. Push branch to remote
git push -u origin feat/your-feature-name

# 5. Merge to main (after testing)
git checkout main
git pull origin main
git merge --no-ff feat/your-feature-name
git push origin main
```

### Why GitHub Flow?

- **Simple** - Easy to understand and follow
- **Fast** - No complex branching or release cycles
- **Continuous Integration** - Encourages frequent integration with main
- **Flexible** - Supports both small fixes and large features

---

## Branch Naming Conventions

Branch names should be descriptive and follow this format:

```
<type>/<task-number>-<short-description>
```

### Branch Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat/` | New features or enhancements | `feat/1.2-user-login-api` |
| `fix/` | Bug fixes | `fix/3.4-cors-headers` |
| `docs/` | Documentation only changes | `docs/update-readme` |
| `style/` | Code style/formatting changes | `style/ruff-formatting` |
| `refactor/` | Code refactoring (no behavior change) | `refactor/agent-structure` |
| `test/` | Adding or updating tests | `test/add-auth-tests` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |

### Guidelines

✅ **Good branch names:**
- `feat/2.3-backend-main-fastapi`
- `fix/health-endpoint-error`
- `docs/contributing-guide`
- `test/integration-tests`

❌ **Avoid:**
- `my-changes` (too vague)
- `feat` (missing description)
- `update` (not descriptive)
- `john-dev` (use purpose, not names)

---

## Commit Message Format

This project uses **Conventional Commits**, a specification for adding human and machine-readable meaning to commit messages.

### Format

```
<type>: <short summary>

<optional body with detailed explanation>

<optional footer with issue references>
```

### Type

Must be one of:

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat: add user authentication endpoint` |
| `fix` | Bug fix | `fix: resolve CORS header issue` |
| `docs` | Documentation changes | `docs: update API documentation` |
| `style` | Code style changes (formatting) | `style: apply ruff formatting` |
| `refactor` | Code refactoring | `refactor: simplify agent creation logic` |
| `test` | Adding/updating tests | `test: add integration tests for auth` |
| `chore` | Maintenance tasks | `chore: update dependencies` |
| `perf` | Performance improvements | `perf: optimize database queries` |
| `ci` | CI/CD changes | `ci: add GitHub Actions workflow` |

### Multi-line Commits (Recommended)

Use multiple `-m` flags for detailed commits:

```bash
git commit -m "feat: implement user authentication endpoint" \
           -m "- Added POST /api/auth/login route" \
           -m "- Implemented JWT token generation" \
           -m "- Added password hashing with bcrypt" \
           -m "- Created user validation middleware" \
           -m "Related to Task 1.2 in PRD-0001-user-auth"
```

**This creates a commit with:**
- **Subject line**: `feat: implement user authentication endpoint`
- **Body**: Bullet points describing key changes
- **Footer**: Reference to related task/PRD

### Guidelines

✅ **Good commit messages:**

```
feat: add document upload functionality

- Created file upload endpoint in FastAPI
- Added validation for PDF/DOCX file types
- Implemented virus scanning integration
- Added unit tests for upload handler

Related to Task 3.4 in PRD-0002-document-management
```

```
fix: resolve memory leak in vector store

ChromaDB was not properly closing connections after queries.
Added explicit connection cleanup in finally block.

Fixes #42
```

❌ **Avoid:**
- `update` (not descriptive)
- `fix bug` (which bug?)
- `WIP` (don't commit work-in-progress to main)
- `asdfasdf` (meaningless)
- `feat: updated the files` (too vague)

### Pro Tips

- **Keep subject line under 50 characters**
- **Use imperative mood** - "add feature" not "added feature"
- **Don't end subject line with a period**
- **Separate subject from body with a blank line**
- **Wrap body at 72 characters** (automatic with `-m` flags)
- **Explain what and why, not how** - Code shows how, commit explains why

---

## Sub-task Workflow

This project uses a structured task-based workflow for organized development.

### Overview

1. **PRDs (Product Requirements Documents)** define features
2. **Task lists** break PRDs into parent tasks and sub-tasks
3. **Sub-tasks** get individual feature branches
4. **One sub-task at a time** - Complete before moving to next

### Sub-task Process

```bash
# 1. Start from latest main
git checkout main
git pull origin main

# 2. Create sub-task branch
git checkout -b feat/<task-number>-<subtask-name>
# Example: feat/2.3-backend-main-fastapi

# 3. Implement the sub-task
# ... make your changes ...

# 4. Test your changes
# Backend:
cd backend && pytest
# Frontend:
cd frontend && pnpm lint && pnpm build

# 5. Stage and commit
git add .
git commit -m "feat: <short summary>" \
           -m "- Key change 1" \
           -m "- Key change 2" \
           -m "Related to Task <task-number> in <PRD reference>"

# 6. Push feature branch (required for backup)
git push -u origin feat/<task-number>-<subtask-name>

# 7. Merge to main (no PR for sub-tasks)
git checkout main
git pull origin main
git merge --no-ff feat/<task-number>-<subtask-name>

# 8. Handle any merge conflicts if they occur
# If conflicts: resolve them, then:
git add .
git commit
# Test again after resolving conflicts

# 9. Push main
git push origin main

# 10. Keep feature branch (do NOT delete)
# Branches are kept as historical reference

# 11. STOP and wait for approval before next sub-task
```

### Important Notes

- ✅ **Always push feature branches** - Required for backup and history
- ✅ **Keep all feature branches** - Don't delete them (historical reference)
- ✅ **Use `--no-ff` when merging** - Creates merge commit for clear history
- ✅ **Test before merging** - Run tests on feature branch
- ✅ **Test after merging** - Verify main still works
- ✅ **One sub-task at a time** - Don't start next until current is merged
- ❌ **No PRs for sub-tasks** - Direct merge to main (PRs are for external contributors)

### Handling Merge Conflicts

If merge conflicts occur:

```bash
# After git merge shows conflicts
# 1. View conflicted files
git status

# 2. Edit files to resolve conflicts
# Look for <<<<<<< HEAD markers

# 3. Test the resolved code
pytest  # or pnpm test

# 4. Complete the merge
git add .
git commit  # Git will use default merge commit message

# 5. Push to main
git push origin main
```

If tests fail after merge:

```bash
# Undo the merge
git reset --hard HEAD~1

# Go back to feature branch to fix
git checkout feat/<task-number>-<subtask-name>
# Fix issues, test again, then retry merge
```

---

## Pull Request Process

While sub-tasks use direct merges, **Pull Requests (PRs)** are used for:

- External contributors
- Major features requiring team review
- Breaking changes
- Architectural changes

### Creating a Pull Request

1. **Push your branch:**
   ```bash
   git push -u origin feat/your-feature-name
   ```

2. **Open PR on GitHub:**
   - Go to repository on GitHub
   - Click "Pull requests" → "New pull request"
   - Select your branch
   - Fill out the PR template (see below)

3. **PR Title Format:**
   ```
   feat: Add user authentication system
   ```
   (Follow Conventional Commits format)

4. **PR Description Template:**
   ```markdown
   ## Description
   Brief description of what this PR does.

   ## Changes
   - Added user authentication endpoint
   - Created JWT token generation
   - Added password hashing
   - Updated API documentation

   ## Testing
   - [ ] All existing tests pass
   - [ ] Added new tests for new functionality
   - [ ] Manually tested the changes
   - [ ] Backend runs without errors
   - [ ] Frontend runs without errors

   ## Documentation
   - [ ] Updated relevant README files
   - [ ] Added code comments where needed
   - [ ] Updated API documentation

   ## Related Issues
   Closes #42
   Related to PRD-0001
   ```

5. **Request review** from team members

6. **Address feedback** - Make changes based on review comments

7. **Merge** - Once approved, merge using "Squash and merge" or "Create merge commit"

### PR Best Practices

- **Keep PRs focused** - One feature or fix per PR
- **Keep PRs small** - Easier to review (<400 lines changed)
- **Respond to feedback promptly**
- **Keep PR branch updated** with main:
  ```bash
  git checkout feat/your-feature
  git fetch origin
  git rebase origin/main
  git push --force-with-lease
  ```

---

## Code Review Guidelines

### For Authors

**Before requesting review:**
- ✅ All tests pass locally
- ✅ Code follows style guidelines (ruff, eslint)
- ✅ No commented-out code or debug statements
- ✅ Documentation is updated
- ✅ Commit messages follow conventions

**During review:**
- Respond to all comments (even if just "Done")
- Don't take feedback personally - it improves the code
- Ask questions if feedback is unclear
- Push new commits for changes (don't force-push during review)

### For Reviewers

**What to look for:**
- ✅ Code correctness - Does it do what it's supposed to?
- ✅ Test coverage - Are there tests for new functionality?
- ✅ Code clarity - Is it readable and well-structured?
- ✅ Edge cases - Are error conditions handled?
- ✅ Performance - Any obvious inefficiencies?
- ✅ Security - Any security concerns?
- ✅ Documentation - Is it documented appropriately?

**How to review:**
- Be constructive and respectful
- Explain the "why" behind suggestions
- Distinguish between "must fix" and "nice to have"
- Approve when code meets quality standards
- Use GitHub's suggestion feature for small fixes:
  ````markdown
  ```suggestion
  const result = await fetchData();
  ```
  ````

---

## Testing Requirements

All code changes must include appropriate tests.

### Backend Testing (Python + pytest)

**Location:** `backend/tests/`

**Running tests:**
```bash
cd backend
source venv/bin/activate
pytest                    # Run all tests
pytest -v                # Verbose output
pytest tests/test_main.py  # Specific file
pytest -k "auth"         # Tests matching pattern
```

**Test categories:**
```python
import pytest

@pytest.mark.unit
def test_user_creation():
    """Fast, isolated unit test"""
    pass

@pytest.mark.integration
def test_database_connection():
    """Integration test (may require external services)"""
    pass

@pytest.mark.slow
def test_full_workflow():
    """Slow end-to-end test"""
    pass
```

**Coverage requirements:**
```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# Aim for >80% coverage on new code
# View report: open htmlcov/index.html
```

### Frontend Testing (TypeScript + Jest)

**Location:** `frontend/__tests__/` or `frontend/components/*.test.tsx`

**Running tests:**
```bash
cd frontend
pnpm test                 # Run all tests
pnpm test:watch          # Watch mode
pnpm test:coverage       # With coverage
```

### What to Test

**✅ Must test:**
- Core business logic
- API endpoints
- Data validation
- Error handling
- Edge cases

**⚠️ Consider testing:**
- Complex algorithms
- Security-critical code
- Frequently changed code

**❌ Don't waste time testing:**
- Third-party libraries (already tested)
- Simple getters/setters
- Configuration files

---

## Code Style Guidelines

### Backend (Python)

**Formatter:** Ruff (replaces Black, isort, and many flake8 rules)

```bash
cd backend

# Check code quality
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .
```

**Key principles:**
- **PEP 8** compliance
- **Type hints** for function parameters and return values
- **Docstrings** for modules, classes, and functions
- **Line length**: 100 characters (configured in `pyproject.toml`)

**Example:**
```python
from typing import Optional

def create_user(name: str, email: str, age: Optional[int] = None) -> dict:
    """
    Create a new user with the given information.
    
    Args:
        name: User's full name
        email: User's email address
        age: User's age (optional)
    
    Returns:
        Dictionary containing user data with generated ID
    
    Raises:
        ValueError: If email format is invalid
    """
    if "@" not in email:
        raise ValueError("Invalid email format")
    
    return {
        "id": generate_id(),
        "name": name,
        "email": email,
        "age": age,
    }
```

### Frontend (TypeScript)

**Linter:** ESLint 9 (flat config)

```bash
cd frontend

# Check code quality
pnpm lint

# Auto-fix issues (if supported)
pnpm lint --fix
```

**Key principles:**
- **TypeScript strict mode** - Full type safety
- **React best practices** - Hooks, composition
- **Functional components** - No class components
- **Named exports** - Prefer named over default exports
- **Path aliases** - Use `@/` for imports

**Example:**
```typescript
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils/cn";

interface UserCardProps {
  name: string;
  email: string;
  isActive?: boolean;
}

export function UserCard({ name, email, isActive = true }: UserCardProps) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    // Effect logic here
  }, []);

  return (
    <div className={cn(
      "rounded-lg border p-4",
      isActive && "bg-green-50",
      !isActive && "bg-gray-50"
    )}>
      <h2 className="text-xl font-bold">{name}</h2>
      <p className="text-gray-600">{email}</p>
    </div>
  );
}
```

### General Best Practices

- **Meaningful names** - Variables, functions, classes should be descriptive
- **Single Responsibility** - Each function/class does one thing
- **DRY (Don't Repeat Yourself)** - Extract common logic
- **KISS (Keep It Simple, Stupid)** - Prefer simple solutions
- **Comments for why, not what** - Code shows what, comments explain why
- **Error handling** - Handle errors gracefully, don't ignore them

---

## Documentation Standards

### Code Documentation

**Python:**
- Module docstrings at top of files
- Class and function docstrings using Google style
- Inline comments for complex logic

**TypeScript:**
- JSDoc comments for exported functions
- Interface documentation
- Inline comments for business logic

### Project Documentation

When adding features, update:

- **README.md** - If setup process changes
- **ARCHITECTURE.md** - If architecture changes
- **API documentation** - If API changes (FastAPI auto-generates from docstrings)
- **Component READMEs** - For significant components

### Commit Documentation

- Clear commit messages (see Commit Message Format)
- Reference PRD/task numbers in commits
- Explain "why" in commit body, not just "what"

---

## Questions?

If you have questions about contributing:

1. Check this guide first
2. Review [README.md](./README.md) for setup issues
3. Check [ARCHITECTURE.md](./ARCHITECTURE.md) for design questions
4. Ask in project chat/discussions
5. Open an issue for clarification

---

## Thank You!

Thank you for contributing to the Advanced Multi-Agent Customer Service AI project! Your contributions help make this project better for everyone.

**Remember:**
- Be respectful and constructive
- Follow the guidelines (but ask if unclear)
- Test your changes thoroughly
- Write clear commit messages
- Have fun coding! 🚀

---

**Version**: 1.0.0  
**Last Updated**: November 2, 2025  
**Maintained by**: ASU VibeCoding Team

