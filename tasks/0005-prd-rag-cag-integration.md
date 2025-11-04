# PRD: Phase 5 - RAG/CAG Integration

**Status**: Planning  
**Phase**: 5  
**Created**: November 4, 2025  
**Owner**: Development Team  
**Priority**: High

---

## Executive Summary

Phase 5 adds **Retrieval-Augmented Generation (RAG)** capabilities to all four worker agents, enabling them to retrieve and reference actual documentation when answering queries. This transforms the system from relying solely on LLM training data to providing accurate, up-to-date information grounded in real documents.

**Goal**: Each worker agent can search and retrieve relevant documentation from domain-specific knowledge bases to provide more accurate, detailed, and authoritative responses.

---

## Background & Motivation

### Current State (Phase 4)
- ✅ 4 specialized worker agents (Technical, Billing, Compliance, General Info)
- ✅ Intelligent routing via supervisor
- ✅ LLM-based responses using GPT-4o-mini training data
- ⚠️ **Limitation**: No access to company-specific documentation
- ⚠️ **Limitation**: Cannot reference actual policies, technical docs, or procedures

### Why RAG/CAG?

**Problems RAG Solves**:
1. **Accuracy**: LLMs can hallucinate; RAG grounds responses in real documents
2. **Up-to-date Info**: Training data gets stale; documents can be updated anytime
3. **Source Attribution**: Can cite specific documents/sections
4. **Company-Specific**: Can reference actual policies, not generic knowledge
5. **Compliance**: Critical for regulatory/legal queries (GDPR, terms of service)

**Use Cases**:
- Technical worker references actual troubleshooting guides
- Billing worker cites current pricing from official documents
- Compliance worker quotes exact policy language from terms of service
- General info worker provides accurate company information from official sources

---

## Goals & Success Criteria

### Primary Goals
1. **Document Storage**: Create knowledge base with domain-specific documents
2. **Vector Store**: Implement semantic search with ChromaDB
3. **RAG Tools**: Add retrieval tools to all 4 workers
4. **Integration**: Workers use RAG tools to enhance responses
5. **Testing**: Verify retrieval accuracy and response quality

### Success Criteria
- ✅ ChromaDB vector store operational with persistent storage
- ✅ Each worker has access to domain-specific RAG tool
- ✅ Workers retrieve relevant documents (top 3-5 results)
- ✅ Responses include retrieved context
- ✅ Unit tests for retrieval functionality
- ✅ Integration tests for RAG-enhanced responses
- ✅ Documentation updated with RAG setup instructions

### Non-Goals (Out of Scope for Phase 5)
- ❌ Advanced retrieval strategies (hybrid search, re-ranking)
- ❌ Document upload UI/API endpoints
- ❌ Real-time document updates/webhooks
- ❌ Multi-modal retrieval (images, videos)
- ❌ Custom embedding models (using OpenAI embeddings)

---

## Technical Approach

### Architecture Overview

```
User Query
    ↓
Supervisor Agent
    ↓
Worker Agent (e.g., Technical Support)
    ↓
    ├─→ [RAG Tool] → Vector Store → Retrieved Docs
    │                                       ↓
    └───────────────────────────────────────┘
                    ↓
        Response with Retrieved Context
```

### Technology Stack

**Vector Store**: ChromaDB
- Persistent storage to disk
- Fast similarity search
- Easy to use with LangChain
- No separate server required

**Embeddings**: OpenAI `text-embedding-3-small`
- Cost-effective ($0.02 / 1M tokens)
- Good quality (1536 dimensions)
- Fast inference
- Compatible with ChromaDB

**Document Loaders**: LangChain Community
- `TextLoader` - Plain text files
- `PyPDFLoader` - PDF documents
- `UnstructuredMarkdownLoader` - Markdown files
- `DirectoryLoader` - Batch loading

**Text Splitting**: `RecursiveCharacterTextSplitter`
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Respects paragraph/sentence boundaries

### Knowledge Base Structure

```
backend/data/docs/
├── technical/           # Technical documentation
│   ├── troubleshooting.md
│   ├── error-codes.pdf
│   ├── installation-guide.md
│   └── api-reference.md
├── billing/            # Billing and pricing
│   ├── pricing-plans.md
│   ├── payment-methods.md
│   ├── refund-policy.md
│   └── subscription-terms.md
├── compliance/         # Policies and regulations
│   ├── privacy-policy.md
│   ├── terms-of-service.md
│   ├── gdpr-compliance.md
│   └── data-protection.md
└── general/            # Company information
    ├── about-company.md
    ├── service-overview.md
    ├── getting-started.md
    └── faq.md
```

### RAG Tool Pattern

Each worker gets a RAG tool that:
1. Takes a query string
2. Performs semantic search in domain-specific vector store
3. Retrieves top-k most relevant documents (k=3-5)
4. Returns formatted context with document metadata
5. Worker includes context in its reasoning

**Example Tool**:
```python
@tool
def technical_docs_search(query: str) -> str:
    """Search technical documentation for troubleshooting guides and solutions.
    
    Use this tool to find relevant technical documentation, error code references,
    installation guides, and troubleshooting procedures.
    """
    # Retrieve from technical vector store
    docs = technical_vectorstore.similarity_search(query, k=3)
    
    # Format results with metadata
    context = "\n\n".join([
        f"Source: {doc.metadata['source']}\n{doc.page_content}"
        for doc in docs
    ])
    
    return context
```

### Worker Integration

Workers updated to use RAG tools:

**Before (Phase 4)**:
```python
technical_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],  # No tools
    system_prompt="You are a technical support specialist...",
    name="technical_support_agent"
)
```

**After (Phase 5)**:
```python
technical_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[technical_docs_search],  # RAG tool added
    system_prompt="""You are a technical support specialist...
    
    IMPORTANT: When relevant, use the technical_docs_search tool to find
    official documentation, troubleshooting guides, and error references.
    Always cite the source when using retrieved information.
    """,
    name="technical_support_agent"
)
```

---

## Implementation Plan

### Phase 5.1: Infrastructure Setup
**Files**: `backend/data/vectorstore.py`, sample documents

1. Create vector store initialization module
2. Add sample documents for each domain (5-10 docs total)
3. Implement document loading and chunking
4. Create persistent ChromaDB instances
5. Verify embeddings and storage

### Phase 5.2: RAG Tools Creation
**Files**: `backend/agents/tools/rag_tools.py`

1. Create `technical_docs_search` tool
2. Create `billing_docs_search` tool
3. Create `compliance_docs_search` tool
4. Create `general_docs_search` tool
5. Export all RAG tools

### Phase 5.3: Worker Agent Updates
**Files**: Update all 4 worker files

1. Update Technical Support worker with RAG tool
2. Update Billing Support worker with RAG tool
3. Update Compliance worker with RAG tool
4. Update General Info worker with RAG tool
5. Enhance system prompts to guide RAG usage

### Phase 5.4: Testing
**Files**: `backend/tests/test_rag_tools.py`, update integration tests

1. Unit tests for vector store operations
2. Unit tests for each RAG tool
3. Integration tests for RAG-enhanced responses
4. Test retrieval accuracy and relevance
5. Test edge cases (no results, malformed queries)

### Phase 5.5: Documentation
**Files**: `backend/README.md`, `README.md`, `RAG_SETUP.md`

1. Document RAG architecture
2. Instructions for adding new documents
3. Vector store maintenance guide
4. Update worker documentation with RAG capabilities
5. Add RAG examples to manual testing guide

---

## Sample Documents

### Technical Documentation Examples
```markdown
# Troubleshooting: Error 500 - Internal Server Error

## Symptoms
- Application displays "Error 500" message
- Server logs show stack trace
- Users cannot access specific features

## Common Causes
1. Database connection failure
2. Missing environment variables
3. Unhandled exceptions in code
4. Server resource exhaustion

## Resolution Steps
1. Check server logs: `tail -f /var/log/app.log`
2. Verify database connectivity
3. Ensure all environment variables are set
4. Restart application server
5. Check server resources (CPU, memory, disk)
```

### Billing Documentation Examples
```markdown
# Refund Policy

## Eligibility
Refunds are available under the following conditions:
- Request made within 30 days of charge
- Service not used beyond trial period
- Billing error or duplicate charge

## Refund Process
1. Contact billing support with transaction ID
2. Provide reason for refund request
3. Refunds processed within 5-7 business days
4. Refund issued to original payment method

## Non-Refundable Items
- Usage beyond trial period
- Custom development work
- Third-party service fees
```

### Compliance Documentation Examples
```markdown
# GDPR Data Deletion Request Process

## User Rights Under GDPR
Users have the right to request deletion of their personal data
under Article 17 (Right to Erasure).

## How to Request Deletion
1. Submit request via email to privacy@company.com
2. Include account email and verification
3. Specify data to be deleted

## Processing Timeline
- Verification: 1-2 business days
- Deletion: 30 days maximum
- Confirmation email sent upon completion

## Data Retention Exceptions
Some data may be retained for:
- Legal compliance requirements
- Fraud prevention (anonymized)
- Financial records (7 years)
```

### General Information Examples
```markdown
# Company Services Overview

## Core Services
1. **Cloud Hosting**: Scalable infrastructure for web applications
2. **Data Storage**: Secure, reliable storage solutions
3. **Analytics Platform**: Real-time data insights and reporting

## Pricing Tiers
- **Starter**: $29/month - Up to 100GB storage
- **Professional**: $79/month - Up to 500GB storage
- **Enterprise**: Custom pricing - Unlimited storage

## Getting Started
1. Sign up for free trial
2. Choose your plan
3. Deploy your first application
4. Access 24/7 support
```

---

## Testing Strategy

### Unit Tests (40 new tests)

**Vector Store Tests** (10 tests):
- Test document loading from files
- Test text splitting configuration
- Test embedding generation
- Test document persistence
- Test retrieval accuracy

**RAG Tool Tests** (20 tests):
- Test each RAG tool (4 tools × 5 tests each)
- Test query formatting
- Test result parsing
- Test error handling (no results, bad queries)
- Test metadata inclusion

**Worker Update Tests** (10 tests):
- Test tool registration for each worker
- Test system prompt updates
- Test tool invocation
- Test response with retrieved context
- Test citation of sources

### Integration Tests (10 new tests)

**RAG Flow Tests**:
- Technical query with document retrieval
- Billing query with policy reference
- Compliance query with regulation citation
- General query with company info retrieval
- Multi-turn conversation with RAG

**Retrieval Quality Tests**:
- Verify relevant documents retrieved
- Test semantic search vs keyword search
- Test retrieval across different document types
- Test handling of queries with no matching docs

---

## Performance Considerations

### Embedding Generation
- **Cost**: ~$0.02 per 1M tokens (OpenAI embeddings)
- **Time**: One-time during document ingestion
- **Strategy**: Pre-compute all embeddings during setup

### Similarity Search
- **Latency**: ~50-100ms for search in ChromaDB
- **Optimization**: Persistent storage prevents re-embedding
- **Scaling**: For >10,000 docs, consider batch retrieval

### Response Time Impact
- **Before RAG**: ~1-2 seconds per query
- **With RAG**: ~2-3 seconds per query
- **Acceptable**: Still under 5-second target

---

## Rollout Plan

### Phase 5A: MVP (Minimum Viable Product)
**Timeline**: 2-3 hours

1. Basic vector store setup
2. 2-3 sample documents per domain
3. RAG tools for all 4 workers
4. Basic unit tests
5. Update documentation

### Phase 5B: Enhancement (Optional)
**Timeline**: 1-2 hours

1. More comprehensive documents (10-15 per domain)
2. Advanced integration tests
3. Retrieval quality metrics
4. Performance optimization
5. Document management utilities

---

## Risks & Mitigations

### Risk 1: Poor Retrieval Quality
**Impact**: Workers retrieve irrelevant documents
**Mitigation**:
- Test with realistic queries
- Tune chunk size and overlap
- Adjust k (number of results)
- Improve document quality

### Risk 2: Embedding Costs
**Impact**: High OpenAI API costs for large document sets
**Mitigation**:
- Cache embeddings in ChromaDB
- Only embed once during setup
- Use cost-effective `text-embedding-3-small`
- Monitor usage with LangSmith

### Risk 3: Increased Latency
**Impact**: RAG adds 0.5-1 second to response time
**Mitigation**:
- Use persistent ChromaDB (fast)
- Limit k to 3-5 documents
- Parallel retrieval if needed
- Cache frequent queries

### Risk 4: Document Maintenance
**Impact**: Outdated documents in knowledge base
**Mitigation**:
- Document update procedures
- Version control for documents
- Regular review schedule
- Easy re-indexing process

---

## Success Metrics

### Quantitative Metrics
- ✅ **Retrieval Accuracy**: >80% queries return relevant docs
- ✅ **Response Time**: <3 seconds with RAG
- ✅ **Test Coverage**: >85% for RAG components
- ✅ **Document Coverage**: 5-10 docs per domain (MVP)

### Qualitative Metrics
- ✅ Workers cite specific documents in responses
- ✅ Responses more accurate than Phase 4 (no RAG)
- ✅ System handles "I don't know" gracefully (no docs found)
- ✅ Retrieval quality improves with better documents

---

## Dependencies

### New Python Packages
```txt
chromadb==0.4.22          # Vector store
langchain-community==0.3.7 # Document loaders
pypdf==4.0.0              # PDF support
unstructured==0.12.0      # Advanced document parsing
```

### Environment Variables (New)
```bash
# Vector store configuration
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
EMBEDDING_MODEL=text-embedding-3-small

# RAG configuration
RAG_TOP_K=3               # Number of documents to retrieve
RAG_CHUNK_SIZE=1000       # Characters per chunk
RAG_CHUNK_OVERLAP=200     # Overlap between chunks
```

---

## Documentation Deliverables

### New Documents
1. **`RAG_SETUP.md`** - Complete RAG setup guide
2. **`backend/data/README.md`** - Document management guide
3. **`backend/tests/test_rag_tools.py`** - RAG test suite

### Updated Documents
1. **`backend/README.md`** - Add RAG architecture section
2. **`README.md`** - Update features with RAG capabilities
3. **`MANUAL_TESTING.md`** - Add RAG testing scenarios

---

## Future Enhancements (Phase 6+)

### Advanced Retrieval (Phase 6A)
- Hybrid search (semantic + keyword)
- Re-ranking for better relevance
- Query expansion and reformulation
- Multi-query retrieval

### Document Management (Phase 6B)
- API endpoints for document upload
- Document versioning
- Automatic re-indexing
- Document analytics

### Enhanced RAG Patterns (Phase 6C)
- Conversational retrieval (follow-up questions)
- Citation extraction and formatting
- Confidence scoring for retrieved docs
- Fallback to web search if no docs found

---

## Appendix: LangChain v1.0 RAG Patterns

### Pattern 1: Tool-Based RAG (Agentic RAG)
**What we're using**: Worker decides when to retrieve

```python
# Worker has RAG tool, uses it when needed
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[rag_tool],  # Agent decides when to call
    system_prompt="Use rag_tool when you need documentation",
)
```

**Benefits**:
- Agent has autonomy
- Only retrieves when relevant
- Can skip retrieval for simple queries

### Pattern 2: Always-On RAG (2-Step RAG)
**Alternative**: Always retrieve before generating

```python
# Not using this - less flexible
docs = vectorstore.similarity_search(query)
context = format_docs(docs)
response = llm.invoke(f"Context: {context}\n\nQuestion: {query}")
```

**Why we prefer Pattern 1**:
- More intelligent (agent decides)
- Better for multi-turn conversations
- Handles queries that don't need retrieval

---

## References

- LangChain RAG Tutorial: https://docs.langchain.com/oss/python/langchain/retrieval
- ChromaDB Documentation: https://docs.trychroma.com/
- OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
- LangChain v1.0 Patterns: https://docs.langchain.com/oss/python/langchain/knowledge-base

---

**PRD Version**: 1.0  
**Last Updated**: November 4, 2025  
**Status**: Ready for Implementation  
**Estimated Effort**: 4-6 hours (MVP: 2-3 hours)

