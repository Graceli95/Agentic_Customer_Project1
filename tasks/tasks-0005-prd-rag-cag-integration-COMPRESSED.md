# Phase 5 Task List - RAG/CAG Integration (COMPRESSED - SPEC COMPLIANT)

**PRD**: `tasks/0005-prd-rag-cag-integration.md`  
**Phase**: 5  
**Goal**: Add document retrieval with proper RAG/CAG strategies per spec  
**Estimated Time**: 4.5 hours

---

## 🎯 Key Difference from Original Plan

**CRITICAL**: This implements **different retrieval strategies** per the original project spec:
- ✅ **Technical Support**: Pure RAG (dynamic retrieval)
- ✅ **Billing Support**: Hybrid RAG/CAG (cache after first query)
- ✅ **Compliance**: Pure CAG (static context, no retrieval)
- ✅ **General Info**: Pure RAG (dynamic retrieval)

---

## 📋 Compressed Task List (10 Tasks)

### [ ] 1. Infrastructure + Sample Documents (45 min)
**Branch**: `feat/phase5-1-infrastructure-and-docs`

**Create**:
```
backend/data/__init__.py
backend/data/vectorstore.py
backend/data/document_loader.py
backend/scripts/index_documents.py
backend/data/docs/technical/troubleshooting.md
backend/data/docs/technical/error-codes.md
backend/data/docs/billing/pricing-plans.md
backend/data/docs/billing/refund-policy.md
backend/data/docs/compliance/privacy-policy.md
backend/data/docs/compliance/terms-of-service.md
backend/data/docs/general/about-company.md
backend/data/docs/general/service-overview.md
```

**Requirements**:
- ChromaDB vector store module (persistent storage)
- Document loader (TextLoader, RecursiveCharacterTextSplitter)
- Indexing script (CLI to index documents)
- 2 sample documents per domain (8 total, 300-500 words each)
- Index all documents after creation

**Success**: Run `python scripts/index_documents.py --domain technical` successfully

---

### [ ] 2. RAG/CAG Tools - All Strategies (80 min)
**Branch**: `feat/phase5-2-rag-cag-tools`

**Create**:
```
backend/agents/tools/__init__.py
backend/agents/tools/rag_tools.py
backend/data/compliance_context.py
```

**Requirements**:

**2.1: Technical Support - Pure RAG** (15 min)
```python
@tool
def technical_docs_search(query: str) -> str:
    """Pure RAG: Dynamic retrieval every query"""
    docs = technical_vectorstore.similarity_search(query, k=3)
    return format_docs_with_metadata(docs)
```

**2.2: Billing Support - Hybrid RAG/CAG** (25 min)
```python
@tool
def billing_docs_search(query: str, runtime: ToolRuntime) -> Command:
    """Hybrid: RAG first time, CAG from cache after"""
    # Check cache
    cached = runtime.state.get("billing_policies")
    if cached:
        return Command(result=cached)  # CAG
    
    # RAG: First retrieval
    docs = billing_vectorstore.similarity_search(query, k=3)
    policies = format_docs_with_metadata(docs)
    
    # Cache for session
    return Command(
        update={"billing_policies": policies},
        result=policies
    )
```

**2.3: Compliance - Pure CAG Setup** (25 min)
```python
# Load compliance docs ONCE at module level
def load_compliance_context():
    """Load all compliance docs at startup (Pure CAG)"""
    privacy = load_document("compliance/privacy-policy.md")
    terms = load_document("compliance/terms-of-service.md")
    return f"PRIVACY POLICY:\n{privacy}\n\nTERMS OF SERVICE:\n{terms}"

# Module-level load (happens once)
COMPLIANCE_CONTEXT = load_compliance_context()
```

**2.4: General Info - Pure RAG** (15 min)
```python
@tool
def general_docs_search(query: str) -> str:
    """Pure RAG: Dynamic retrieval"""
    docs = general_vectorstore.similarity_search(query, k=3)
    return format_docs_with_metadata(docs)
```

**Success**: All tools importable and callable

---

### [ ] 3. Technical Worker - Pure RAG Integration (15 min)
**Branch**: `feat/phase5-3-technical-worker-rag`

**Update**: `backend/agents/workers/technical_support.py`

**Requirements**:
- Import `technical_docs_search` tool
- Add to `tools=[technical_docs_search]`
- Update system prompt: "Use technical_docs_search to find relevant documentation"

---

### [ ] 4. Billing Worker - Hybrid RAG/CAG Integration (15 min)
**Branch**: `feat/phase5-4-billing-worker-hybrid`

**Update**: `backend/agents/workers/billing_support.py`

**Requirements**:
- Import `billing_docs_search` tool
- Add to `tools=[billing_docs_search]`
- Update system prompt: "Use billing_docs_search for policy questions. It caches policies after first retrieval."

---

### [ ] 5. Compliance Worker - Pure CAG Integration (15 min)
**Branch**: `feat/phase5-5-compliance-worker-cag`

**Update**: `backend/agents/workers/compliance.py`

**Requirements**:
- Import `COMPLIANCE_CONTEXT` from tools module
- **NO tools** - `tools=[]`
- Update system prompt to include full static context:
```python
system_prompt = f"""You are a Policy & Compliance specialist.

COMPLIANCE DOCUMENTATION (pre-loaded):
{COMPLIANCE_CONTEXT}

Use this pre-loaded context to answer all queries. Cite specific sections when relevant.
NO additional retrieval is needed - all information is above.
"""
```

---

### [ ] 6. General Info Worker - Pure RAG Integration (15 min)
**Branch**: `feat/phase5-6-general-worker-rag`

**Update**: `backend/agents/workers/general_info.py`

**Requirements**:
- Import `general_docs_search` tool
- Add to `tools=[general_docs_search]`
- Update system prompt: "Use general_docs_search to find company information"

---

### [ ] 7. Unit Tests - Strategy-Specific (35 min)
**Branch**: `feat/phase5-7-unit-tests`

**Create**:
```
backend/tests/test_rag_tools.py
backend/tests/test_compliance_cag.py
```

**Requirements** (16 tests total):

**Pure RAG Tests (6 tests)**:
- Technical: returns results, formats metadata, handles no results
- General: returns results, formats metadata, handles no results

**Hybrid RAG/CAG Tests (6 tests)**:
- First query performs RAG
- First query caches results
- Second query uses cache (CAG)
- Cache persists in session
- New session clears cache
- Returns Command with state update

**Pure CAG Tests (4 tests)**:
- Loads docs at startup
- No tools (no retrieval)
- Static context in system prompt
- No vector store calls during queries

**Success**: 16 tests passing

---

### [ ] 8. Integration Tests - All Strategies (20 min)
**Branch**: `feat/phase5-8-integration-tests`

**Update**: `backend/tests/test_main.py`

**Requirements** (4 tests):
- Test technical query with Pure RAG
- Test billing query with Hybrid RAG→CAG transition
- Test compliance query with Pure CAG (no retrieval)
- Test general info query with Pure RAG

**Success**: 4 integration tests passing

---

### [ ] 9. Documentation Updates (40 min)
**Branch**: `feat/phase5-9-documentation`

**Update**:
```
backend/README.md
README.md
```

**Requirements**:
- Phase 5 status and features
- RAG/CAG architecture section
- Explain all 3 strategies (Pure RAG, Hybrid, Pure CAG)
- Update test statistics
- Add retrieval examples for each strategy

---

### [ ] 10. RAG Setup Guide (25 min)
**Branch**: `feat/phase5-10-rag-setup-guide`

**Create**: `RAG_SETUP.md`

**Requirements**:
- Quick start (how to index documents)
- Adding new documents guide
- Strategy explanations (RAG vs CAG vs Hybrid)
- Testing RAG/CAG functionality
- Troubleshooting section
- Example queries per strategy

---

## ✅ Success Checklist

### Infrastructure
- [ ] ChromaDB vector stores created for Technical, Billing, General domains
- [ ] Compliance docs loaded at module level (CAG)
- [ ] 8 sample documents created and indexed
- [ ] Persistent storage working

### RAG/CAG Tools
- [ ] Technical: Pure RAG tool ✅
- [ ] Billing: Hybrid RAG/CAG tool with caching ✅
- [ ] Compliance: Pure CAG (no tool, static context) ✅
- [ ] General: Pure RAG tool ✅

### Worker Integration
- [ ] Technical worker uses Pure RAG
- [ ] Billing worker uses Hybrid RAG/CAG
- [ ] Compliance worker uses Pure CAG
- [ ] General worker uses Pure RAG

### Testing
- [ ] 16 unit tests passing (strategy-specific)
- [ ] 4 integration tests passing (all strategies)
- [ ] Total: ~165 tests passing (145 + 20 new)

### Documentation
- [ ] backend/README.md updated with RAG/CAG
- [ ] root README.md updated with Phase 5
- [ ] RAG_SETUP.md created

---

## 🔑 Key Differences: RAG vs CAG vs Hybrid

### Pure RAG (Technical, General)
```
Query → Vector Store Search → Retrieve Docs → Generate Response
↓
Every query retrieves fresh documents
```

### Hybrid RAG/CAG (Billing)
```
First Query:  Query → Vector Store → Retrieve → Cache → Response
Second Query: Query → Check Cache → Return Cached → Response
↓
RAG first time, CAG from cache after
```

### Pure CAG (Compliance)
```
Module Load: Load All Docs → Store in Memory
Any Query:   Query → Use Static Context → Response
↓
No runtime retrieval, all context pre-loaded
```

---

## ⏱️ Timeline

| Task | Time | Cumulative |
|------|------|------------|
| 1. Infrastructure + Docs | 45 min | 45 min |
| 2. RAG/CAG Tools (all strategies) | 80 min | 2h 05m |
| 3-6. Worker Integration (×4) | 60 min | 3h 05m |
| 7. Unit Tests (16 tests) | 35 min | 3h 40m |
| 8. Integration Tests (4 tests) | 20 min | 4h 00m |
| 9. Documentation | 40 min | 4h 40m |
| 10. RAG Setup Guide | 25 min | **5h 05m** |

**With buffer**: 5-5.5 hours total

---

## 📝 Dependencies to Add

Add to `backend/requirements.txt`:
```txt
chromadb==0.4.22
langchain-community==0.3.7
pypdf==4.0.0
unstructured==0.12.0
```

---

## 🎯 Strategy Implementation Notes

### Why Different Strategies?

**Pure RAG** (Technical, General):
- Dynamic knowledge that changes
- Need fresh, up-to-date information
- Examples: Bug fixes, new features, updated guides

**Hybrid RAG/CAG** (Billing):
- Static policies that rarely change
- High query volume for same policies
- Performance: Cache after first retrieval

**Pure CAG** (Compliance):
- Fixed legal documents (ToS, Privacy)
- Must be consistent across all users
- Fastest: No retrieval overhead
- Compliance: Same exact wording every time

---

**Task List Version**: 2.0 (Spec Compliant)  
**Created**: November 4, 2025  
**Status**: Ready for Implementation  
**Total Tasks**: 10 (compressed from 21)

