# Phase 5 Task List - RAG/CAG Integration

**PRD**: `tasks/0005-prd-rag-cag-integration.md`  
**Phase**: 5  
**Goal**: Add document retrieval capabilities to all 4 workers  
**Estimated Time**: 4-6 hours (MVP: 2-3 hours)

---

## Task Categories

1. **Infrastructure Setup** (3 tasks)
2. **Sample Documents** (4 tasks)
3. **RAG Tools** (4 tasks)
4. **Worker Integration** (4 tasks)
5. **Testing** (3 tasks)
6. **Documentation** (3 tasks)

**Total Tasks**: 21 tasks

---

## 📋 Task List

### Category 1: Infrastructure Setup

#### [ ] 1.1 Create vector store module
**Branch**: `feat/phase5-1.1-vector-store-module`  
**Files**:
- CREATE `backend/data/__init__.py` (if not exists)
- CREATE `backend/data/vectorstore.py`

**Requirements**:
- Import ChromaDB and OpenAI embeddings
- Create `get_vectorstore(domain: str)` function
- Persistent storage: `backend/data/chroma_db/{domain}/`
- Return ChromaDB instance for given domain
- Handle initialization errors gracefully
- Add logging for vector store operations

**Tests**: Create vector store, verify persistence, test multiple domains

---

#### [ ] 1.2 Add document loading utilities
**Branch**: `feat/phase5-1.2-document-loaders`  
**Files**:
- CREATE `backend/data/document_loader.py`

**Requirements**:
- Import LangChain document loaders (TextLoader, PyPDFLoader, etc.)
- Create `load_documents(directory: str)` function
- Support .txt, .md, .pdf files
- Use `RecursiveCharacterTextSplitter` (chunk_size=1000, overlap=200)
- Return list of split documents
- Add metadata (source file, chunk index)
- Error handling for unsupported files

**Tests**: Load various file types, verify chunking, check metadata

---

#### [ ] 1.3 Create document indexing script
**Branch**: `feat/phase5-1.3-indexing-script`  
**Files**:
- CREATE `backend/scripts/index_documents.py`

**Requirements**:
- CLI script to index documents for a domain
- Usage: `python scripts/index_documents.py --domain technical`
- Load documents from `backend/data/docs/{domain}/`
- Generate embeddings using OpenAI
- Store in ChromaDB vector store
- Print progress and summary
- Handle re-indexing (clear old, add new)

**Tests**: Manual testing (run script, verify vector store populated)

---

### Category 2: Sample Documents

#### [ ] 2.1 Create technical documentation samples
**Branch**: `feat/phase5-2.1-technical-docs`  
**Files**:
- CREATE `backend/data/docs/technical/troubleshooting.md`
- CREATE `backend/data/docs/technical/error-codes.md`
- CREATE `backend/data/docs/technical/installation-guide.md`

**Requirements**:
- 3-5 sample technical documents
- Cover: troubleshooting, error codes, installation
- Realistic content (500-1000 words each)
- Markdown format
- Include headers, lists, code examples

**Tests**: Load documents, verify content readable

---

#### [ ] 2.2 Create billing documentation samples
**Branch**: `feat/phase5-2.2-billing-docs`  
**Files**:
- CREATE `backend/data/docs/billing/pricing-plans.md`
- CREATE `backend/data/docs/billing/refund-policy.md`
- CREATE `backend/data/docs/billing/payment-methods.md`

**Requirements**:
- 3-5 sample billing documents
- Cover: pricing, refunds, payment methods
- Realistic content (500-1000 words each)
- Markdown format
- Include tables, pricing tiers

**Tests**: Load documents, verify content readable

---

#### [ ] 2.3 Create compliance documentation samples
**Branch**: `feat/phase5-2.3-compliance-docs`  
**Files**:
- CREATE `backend/data/docs/compliance/privacy-policy.md`
- CREATE `backend/data/docs/compliance/terms-of-service.md`
- CREATE `backend/data/docs/compliance/gdpr-compliance.md`

**Requirements**:
- 3-5 sample compliance documents
- Cover: privacy, terms, GDPR
- Realistic content (500-1000 words each)
- Markdown format
- Include legal sections, numbered lists

**Tests**: Load documents, verify content readable

---

#### [ ] 2.4 Create general information documentation samples
**Branch**: `feat/phase5-2.4-general-docs`  
**Files**:
- CREATE `backend/data/docs/general/about-company.md`
- CREATE `backend/data/docs/general/service-overview.md`
- CREATE `backend/data/docs/general/getting-started.md`

**Requirements**:
- 3-5 sample general info documents
- Cover: company info, services, getting started
- Realistic content (500-1000 words each)
- Markdown format
- Include FAQs, feature lists

**Tests**: Load documents, verify content readable

---

### Category 3: RAG Tools

#### [ ] 3.1 Create RAG tools module and technical RAG tool
**Branch**: `feat/phase5-3.1-rag-tools-module`  
**Files**:
- CREATE `backend/agents/tools/__init__.py`
- CREATE `backend/agents/tools/rag_tools.py`

**Requirements**:
- Import necessary dependencies (tool decorator, vector store)
- Create `technical_docs_search(query: str) -> str` tool
- Retrieve from technical vector store (k=3)
- Format results with source metadata
- Handle no results gracefully
- Add detailed tool description for supervisor
- Export tool

**Tests**: Unit tests for tool invocation, retrieval, formatting

---

#### [ ] 3.2 Create billing RAG tool
**Branch**: `feat/phase5-3.2-billing-rag-tool`  
**Files**:
- UPDATE `backend/agents/tools/rag_tools.py`

**Requirements**:
- Create `billing_docs_search(query: str) -> str` tool
- Retrieve from billing vector store (k=3)
- Format results with source metadata
- Handle no results gracefully
- Add detailed tool description
- Export tool

**Tests**: Unit tests for tool invocation, retrieval, formatting

---

#### [ ] 3.3 Create compliance RAG tool
**Branch**: `feat/phase5-3.3-compliance-rag-tool`  
**Files**:
- UPDATE `backend/agents/tools/rag_tools.py`

**Requirements**:
- Create `compliance_docs_search(query: str) -> str` tool
- Retrieve from compliance vector store (k=3)
- Format results with source metadata
- Handle no results gracefully
- Add detailed tool description
- Export tool

**Tests**: Unit tests for tool invocation, retrieval, formatting

---

#### [ ] 3.4 Create general information RAG tool
**Branch**: `feat/phase5-3.4-general-rag-tool`  
**Files**:
- UPDATE `backend/agents/tools/rag_tools.py`

**Requirements**:
- Create `general_docs_search(query: str) -> str` tool
- Retrieve from general info vector store (k=3)
- Format results with source metadata
- Handle no results gracefully
- Add detailed tool description
- Export all 4 RAG tools from module

**Tests**: Unit tests for tool invocation, retrieval, formatting

---

### Category 4: Worker Integration

#### [ ] 4.1 Integrate RAG tool with Technical Support worker
**Branch**: `feat/phase5-4.1-technical-worker-rag`  
**Files**:
- UPDATE `backend/agents/workers/technical_support.py`

**Requirements**:
- Import `technical_docs_search` tool
- Add tool to worker's tools list
- Update system prompt to guide RAG usage
- Emphasize citing sources when using retrieved info
- Maintain backward compatibility

**Tests**: Unit tests for tool registration, integration tests for RAG-enhanced responses

---

#### [ ] 4.2 Integrate RAG tool with Billing Support worker
**Branch**: `feat/phase5-4.2-billing-worker-rag`  
**Files**:
- UPDATE `backend/agents/workers/billing_support.py`

**Requirements**:
- Import `billing_docs_search` tool
- Add tool to worker's tools list
- Update system prompt to guide RAG usage
- Emphasize citing sources when using retrieved info
- Maintain backward compatibility

**Tests**: Unit tests for tool registration, integration tests for RAG-enhanced responses

---

#### [ ] 4.3 Integrate RAG tool with Compliance worker
**Branch**: `feat/phase5-4.3-compliance-worker-rag`  
**Files**:
- UPDATE `backend/agents/workers/compliance.py`

**Requirements**:
- Import `compliance_docs_search` tool
- Add tool to worker's tools list
- Update system prompt to guide RAG usage
- Emphasize citing exact policy language when available
- Maintain backward compatibility

**Tests**: Unit tests for tool registration, integration tests for RAG-enhanced responses

---

#### [ ] 4.4 Integrate RAG tool with General Information worker
**Branch**: `feat/phase5-4.4-general-worker-rag`  
**Files**:
- UPDATE `backend/agents/workers/general_info.py`

**Requirements**:
- Import `general_docs_search` tool
- Add tool to worker's tools list
- Update system prompt to guide RAG usage
- Emphasize citing sources when using retrieved info
- Maintain backward compatibility

**Tests**: Unit tests for tool registration, integration tests for RAG-enhanced responses

---

### Category 5: Testing

#### [ ] 5.1 Create unit tests for RAG infrastructure
**Branch**: `feat/phase5-5.1-rag-unit-tests`  
**Files**:
- CREATE `backend/tests/test_vectorstore.py`
- CREATE `backend/tests/test_document_loader.py`

**Requirements**:
- Test vector store creation and persistence
- Test document loading from various file types
- Test text splitting and chunking
- Test embedding generation (mocked)
- Test retrieval accuracy
- 20-25 unit tests

**Tests**: Run pytest, verify all tests pass

---

#### [ ] 5.2 Create unit tests for RAG tools
**Branch**: `feat/phase5-5.2-rag-tool-tests`  
**Files**:
- CREATE `backend/tests/test_rag_tools.py`

**Requirements**:
- Test each RAG tool (4 tools × 5 tests = 20 tests)
- Test query formatting
- Test result parsing and formatting
- Test error handling (no results, bad queries)
- Test metadata inclusion
- Mock vector store calls

**Tests**: Run pytest, verify all tests pass

---

#### [ ] 5.3 Create integration tests for RAG-enhanced workers
**Branch**: `feat/phase5-5.3-rag-integration-tests`  
**Files**:
- UPDATE `backend/tests/test_main.py`

**Requirements**:
- Add 8-10 new integration tests
- Test technical query with document retrieval
- Test billing query with policy reference
- Test compliance query with regulation citation
- Test general query with company info retrieval
- Test multi-turn conversation with RAG
- Verify retrieved context in responses

**Tests**: Run pytest with --run-integration flag

---

### Category 6: Documentation

#### [ ] 6.1 Create RAG setup guide
**Branch**: `feat/phase5-6.1-rag-setup-guide`  
**Files**:
- CREATE `RAG_SETUP.md`

**Requirements**:
- Complete RAG setup instructions
- Document indexing process
- Adding new documents guide
- Vector store maintenance
- Troubleshooting section
- Example queries and responses

---

#### [ ] 6.2 Update backend README with RAG architecture
**Branch**: `feat/phase5-6.2-update-backend-readme`  
**Files**:
- UPDATE `backend/README.md`

**Requirements**:
- Add RAG Architecture section
- Update Phase 5 status and features
- Document RAG tools for each worker
- Update project structure with new files
- Update test statistics
- Add RAG environment variables

---

#### [ ] 6.3 Update root README with RAG features
**Branch**: `feat/phase5-6.3-update-root-readme`  
**Files**:
- UPDATE `README.md`

**Requirements**:
- Update Phase 5 status
- Add RAG features to feature list
- Update architecture diagram
- Update test statistics
- Add RAG to "What's Working" section

---

## 🎯 Success Checklist

### Infrastructure
- [ ] ChromaDB vector stores created for all 4 domains
- [ ] Documents loaded and chunked properly
- [ ] Embeddings generated and stored
- [ ] Persistent storage working

### RAG Tools
- [ ] 4 RAG tools created and working
- [ ] Tools return relevant documents
- [ ] Source attribution included
- [ ] Error handling for no results

### Worker Integration
- [ ] All 4 workers have RAG tools
- [ ] System prompts updated
- [ ] Workers cite sources in responses
- [ ] Backward compatibility maintained

### Testing
- [ ] 40+ new unit tests passing
- [ ] 8-10 new integration tests passing
- [ ] Total tests: ~195+ passing
- [ ] RAG retrieval accuracy verified

### Documentation
- [ ] RAG_SETUP.md complete
- [ ] Backend README updated
- [ ] Root README updated
- [ ] All architecture diagrams updated

---

## 📊 Estimated Timeline

### MVP (Minimum Viable Product) - 2-3 hours
- Tasks 1.1-1.3: Infrastructure (45 min)
- Tasks 2.1-2.4: Sample documents (30 min)
- Tasks 3.1-3.4: RAG tools (45 min)
- Tasks 4.1-4.4: Worker integration (30 min)
- Task 5.1: Basic tests (30 min)

### Complete Phase 5 - 4-6 hours
- All 21 tasks completed
- Comprehensive testing
- Complete documentation

---

## 🚀 Getting Started

1. Review PRD: `tasks/0005-prd-rag-cag-integration.md`
2. Start with Task 1.1: Vector store module
3. Follow @process-task-list.mdc workflow
4. One task at a time, commit-push-merge cycle
5. Update this checklist as you progress

---

## 📝 Notes

### Dependencies to Add
Add to `backend/requirements.txt`:
```txt
chromadb==0.4.22
langchain-community==0.3.7
pypdf==4.0.0
unstructured==0.12.0
```

### Environment Variables
Add to `backend/.env`:
```bash
# RAG Configuration
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
RAG_TOP_K=3
```

### Git Workflow
- Feature branches: `feat/phase5-X.Y-task-name`
- Commit format: `feat(phase5): Task X.Y description`
- Merge to main after each task
- Push to GitHub for backup

---

**Task List Version**: 1.0  
**Created**: November 4, 2025  
**Status**: Ready for Implementation  
**Total Tasks**: 21

