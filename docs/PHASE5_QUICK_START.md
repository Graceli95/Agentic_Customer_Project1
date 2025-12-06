# 🚀 Phase 5 Quick Start Guide

**Goal**: Add RAG/CAG with proper strategy differentiation per spec  
**Time**: 4.5-5 hours  
**Tasks**: 10 (compressed from 21)

---

## 🎯 Critical: Strategy Differentiation

**This is NOT "RAG for everyone"** - Each worker gets a different retrieval strategy:

| Worker | Strategy | Implementation |
|--------|----------|----------------|
| **Technical** | Pure RAG | Tool searches vector store every query |
| **Billing** | Hybrid RAG/CAG | RAG first query, cache it, CAG after |
| **Compliance** | Pure CAG | Static docs loaded at startup, no tool |
| **General Info** | Pure RAG | Tool searches vector store every query |

---

## 📋 10-Task Overview

### Infrastructure (Task 1 - 45 min)
- Create vector store module
- Create document loader
- Create indexing script
- Add 8 sample documents (2 per domain)

### Tools (Task 2 - 80 min)
- Technical: Pure RAG tool
- Billing: Hybrid RAG/CAG tool with caching
- Compliance: Pure CAG (load docs at startup)
- General: Pure RAG tool

### Integration (Tasks 3-6 - 60 min)
- Add tools to workers
- Update system prompts
- Compliance gets NO tool (CAG)

### Testing (Tasks 7-8 - 55 min)
- 16 unit tests (strategy-specific)
- 4 integration tests (one per strategy)

### Documentation (Tasks 9-10 - 65 min)
- Update READMEs
- Create RAG_SETUP.md

---

## 🔑 Key Implementation Patterns

### Pure RAG (Technical, General)
```python
@tool
def technical_docs_search(query: str) -> str:
    """Search on every query"""
    docs = vectorstore.similarity_search(query, k=3)
    return format_docs(docs)

# Worker:
agent = create_agent(
    tools=[technical_docs_search],  # Has tool
    system_prompt="Use technical_docs_search when needed"
)
```

### Hybrid RAG/CAG (Billing)
```python
@tool
def billing_docs_search(query: str, runtime: ToolRuntime) -> Command:
    """RAG first time, CAG from cache"""
    cached = runtime.state.get("billing_policies")
    if cached:
        return Command(result=cached)  # CAG!
    
    # RAG
    docs = vectorstore.similarity_search(query, k=3)
    policies = format_docs(docs)
    return Command(
        update={"billing_policies": policies},  # Cache it!
        result=policies
    )

# Worker:
agent = create_agent(
    tools=[billing_docs_search],  # Has tool with caching
    system_prompt="Use billing_docs_search. It caches policies."
)
```

### Pure CAG (Compliance)
```python
# Module level - load ONCE
COMPLIANCE_CONTEXT = load_all_compliance_docs()

# Worker:
agent = create_agent(
    tools=[],  # NO TOOL!
    system_prompt=f"""You are a compliance specialist.

COMPLIANCE DOCUMENTS (pre-loaded):
{COMPLIANCE_CONTEXT}

Answer using only this pre-loaded context."""
)
```

---

## ✅ Success Criteria

### After Task 1:
- [ ] Can run `python scripts/index_documents.py --domain technical`
- [ ] ChromaDB folder created with data

### After Task 2:
- [ ] All 4 tools/strategies implemented
- [ ] Can import and call each tool

### After Task 6:
- [ ] Technical worker has RAG tool
- [ ] Billing worker has hybrid tool
- [ ] Compliance worker has NO tool (CAG)
- [ ] General worker has RAG tool

### After Task 8:
- [ ] ~165 tests passing (145 existing + 20 new)
- [ ] All strategies tested

### After Task 10:
- [ ] RAG_SETUP.md exists
- [ ] READMEs updated with Phase 5

---

## 🚫 Common Pitfalls to Avoid

### ❌ Don't:
1. Give all workers the same RAG tool (misses spec requirement!)
2. Give Compliance worker a retrieval tool (should be CAG!)
3. Forget to cache in Billing tool (should be Hybrid!)
4. Skip testing different strategies
5. Forget to document strategy differences

### ✅ Do:
1. Implement all 3 strategies (RAG, CAG, Hybrid)
2. Test each strategy independently
3. Document why each strategy was chosen
4. Show performance difference (CAG faster than RAG)
5. Cite sources from retrieved docs

---

## 📊 Expected Test Results

After completion:
```bash
$ pytest --run-integration -v

======================== 165 passed ========================

Phase 4 tests: 145 passing ✅
Phase 5 tests: 20 new passing ✅
  - 16 unit tests (strategy-specific)
  - 4 integration tests (all strategies)
```

---

## 🎯 Strategy Testing Checklist

### Pure RAG:
- [ ] Returns documents on query
- [ ] Different results for different queries
- [ ] Handles no results gracefully

### Hybrid RAG/CAG:
- [ ] First query does RAG (slow, retrieves)
- [ ] Second query does CAG (fast, cached)
- [ ] New session clears cache
- [ ] Cache persists across queries in session

### Pure CAG:
- [ ] No vector store calls
- [ ] Same context every query
- [ ] Faster than RAG
- [ ] No tools registered

---

## 🔧 Debugging Tips

### If RAG not working:
```python
# Check vector store populated
from backend.data.vectorstore import get_vectorstore
vs = get_vectorstore("technical")
print(vs._collection.count())  # Should be > 0
```

### If caching not working:
```python
# Check state in billing tool
print(runtime.state.get("billing_policies"))  # Should cache after first call
```

### If CAG not working:
```python
# Check compliance context loaded
from backend.agents.tools.rag_tools import COMPLIANCE_CONTEXT
print(len(COMPLIANCE_CONTEXT))  # Should be > 1000 chars
```

---

## 📝 Quick Command Reference

```bash
# Install new dependencies
pip install chromadb==0.4.22 langchain-community==0.3.7 pypdf==4.0.0 unstructured==0.12.0

# Index documents
python backend/scripts/index_documents.py --domain technical
python backend/scripts/index_documents.py --domain billing
python backend/scripts/index_documents.py --domain general

# Run tests
pytest backend/tests/test_rag_tools.py -v
pytest backend/tests/test_compliance_cag.py -v
pytest --run-integration -v

# Check coverage
pytest --cov=backend --cov-report=html
```

---

## 🎬 Ready to Start?

**Current task**: Task 1 - Infrastructure + Sample Documents (45 min)

**Next steps**:
1. Create vector store module
2. Create document loader
3. Create indexing script
4. Write 8 sample documents
5. Index all documents

**Let's go!** 🚀

---

**Version**: 1.0  
**Phase**: 5  
**Status**: Ready to implement  
**Estimated completion**: ~5 hours from now

