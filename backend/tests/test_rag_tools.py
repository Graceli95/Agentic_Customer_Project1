"""
Unit Tests for RAG/CAG Tools.

Tests all three retrieval strategies:
- Pure RAG (Technical, General)
- Hybrid RAG/CAG (Billing)
- Pure CAG (Compliance)

Phase: 5 - RAG/CAG Integration
Last Updated: November 4, 2025
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from langchain_core.documents import Document

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.tools.rag_tools import (
    technical_docs_search,
    general_docs_search,
    billing_docs_search,
    COMPLIANCE_CONTEXT,
)


# ============================================================================
# Pure RAG Tests - Technical Support
# ============================================================================


class TestTechnicalDocsSearch:
    """Test Pure RAG strategy for technical documentation."""

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_technical_search_returns_results(self, mock_get_vectorstore):
        """Test that technical search returns formatted results."""
        # Mock vector store
        mock_vectorstore = Mock()
        mock_docs = [
            Document(
                page_content="Error 500 is a server error...",
                metadata={"source": "/path/to/error-codes.md"}
            ),
            Document(
                page_content="To troubleshoot 500 errors...",
                metadata={"source": "/path/to/troubleshooting.md"}
            )
        ]
        mock_vectorstore.similarity_search.return_value = mock_docs
        mock_get_vectorstore.return_value = mock_vectorstore

        # Call tool
        result = technical_docs_search.invoke({"query": "error 500"})

        # Assertions
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Error 500" in result or "500 errors" in result
        assert "Source 1:" in result
        assert "Source 2:" in result
        mock_vectorstore.similarity_search.assert_called_once_with("error 500", k=3)

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_technical_search_formats_metadata(self, mock_get_vectorstore):
        """Test that source metadata is properly formatted."""
        mock_vectorstore = Mock()
        mock_docs = [
            Document(
                page_content="Test content",
                metadata={"source": "/backend/data/docs/technical/error-codes.md"}
            )
        ]
        mock_vectorstore.similarity_search.return_value = mock_docs
        mock_get_vectorstore.return_value = mock_vectorstore

        result = technical_docs_search.invoke({"query": "test"})

        assert "error-codes.md" in result
        assert "Source 1:" in result

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_technical_search_handles_no_results(self, mock_get_vectorstore):
        """Test graceful handling when no documents are found."""
        mock_vectorstore = Mock()
        mock_vectorstore.similarity_search.return_value = []
        mock_get_vectorstore.return_value = mock_vectorstore

        result = technical_docs_search.invoke({"query": "nonexistent"})

        assert isinstance(result, str)
        assert "couldn't find" in result.lower()

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_technical_search_handles_none_vectorstore(self, mock_get_vectorstore):
        """Test handling when vectorstore is unavailable."""
        mock_get_vectorstore.return_value = None

        result = technical_docs_search.invoke({"query": "test"})

        assert isinstance(result, str)
        assert "unavailable" in result.lower()


# ============================================================================
# Pure RAG Tests - General Info
# ============================================================================


class TestGeneralDocsSearch:
    """Test Pure RAG strategy for general information."""

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_general_search_returns_results(self, mock_get_vectorstore):
        """Test that general search returns formatted results."""
        mock_vectorstore = Mock()
        mock_docs = [
            Document(
                page_content="Our company provides cloud services...",
                metadata={"source": "/path/to/about-company.md"}
            ),
            Document(
                page_content="We offer infrastructure solutions...",
                metadata={"source": "/path/to/service-overview.md"}
            )
        ]
        mock_vectorstore.similarity_search.return_value = mock_docs
        mock_get_vectorstore.return_value = mock_vectorstore

        result = general_docs_search.invoke({"query": "what services"})

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Source 1:" in result
        assert "Source 2:" in result
        mock_vectorstore.similarity_search.assert_called_once_with("what services", k=3)

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_general_search_handles_no_results(self, mock_get_vectorstore):
        """Test graceful handling when no documents are found."""
        mock_vectorstore = Mock()
        mock_vectorstore.similarity_search.return_value = []
        mock_get_vectorstore.return_value = mock_vectorstore

        result = general_docs_search.invoke({"query": "nonexistent"})

        assert isinstance(result, str)
        assert "couldn't find" in result.lower()


# ============================================================================
# Hybrid RAG/CAG Tests - Billing Support
# ============================================================================


class TestBillingDocsSearch:
    """Test Hybrid RAG/CAG strategy for billing documentation.
    
    Note: These tests verify the caching logic by directly testing
    the function logic since ToolRuntime requires full LangGraph context.
    """

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_billing_retrieves_on_empty_state(self, mock_get_vectorstore):
        """Test that billing function performs RAG when state is empty."""
        mock_vectorstore = Mock()
        mock_docs = [
            Document(
                page_content="Our refund policy allows...",
                metadata={"source": "/path/to/refund-policy.md"}
            )
        ]
        mock_vectorstore.similarity_search.return_value = mock_docs
        mock_get_vectorstore.return_value = mock_vectorstore

        # Test the caching logic by simulating what happens with empty state
        # Mock runtime with empty state
        runtime = Mock()
        runtime.state = {}
        
        from agents.tools.rag_tools import billing_docs_search as billing_fn
        from langgraph.types import Command
        
        result = billing_fn.func("refund policy", runtime)

        # Should have called vector search (RAG)
        mock_vectorstore.similarity_search.assert_called_once()
        # Should return Command with update
        assert isinstance(result, Command)
        assert hasattr(result, 'update')
        assert "billing_policies" in result.update
        assert "refund policy" in result.update["billing_policies"].lower()

    def test_billing_returns_cache_when_available(self):
        """Test that billing function returns cached results when available."""
        # Mock runtime with cached state
        cached_policies = "**Source 1: pricing.md**\nPricing information..."
        runtime = Mock()
        runtime.state = {"billing_policies": cached_policies}

        from agents.tools.rag_tools import billing_docs_search as billing_fn
        
        result = billing_fn.func("pricing", runtime)

        # Should return cached string directly (not Command)
        assert isinstance(result, str)
        assert result == cached_policies

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_billing_cache_includes_doc_content(self, mock_get_vectorstore):
        """Test that cached billing results include actual content."""
        mock_vectorstore = Mock()
        mock_docs = [
            Document(
                page_content="Pricing: $10/month for Basic plan",
                metadata={"source": "/path/to/pricing.md"}
            )
        ]
        mock_vectorstore.similarity_search.return_value = mock_docs
        mock_get_vectorstore.return_value = mock_vectorstore

        runtime = Mock()
        runtime.state = {}
        
        from agents.tools.rag_tools import billing_docs_search as billing_fn
        from langgraph.types import Command
        
        result = billing_fn.func("pricing", runtime)

        # Check that result is Command with cached content
        assert isinstance(result, Command)
        assert "billing_policies" in result.update
        assert "Pricing" in result.update["billing_policies"]
        assert "$10/month" in result.update["billing_policies"]


# ============================================================================
# Pure CAG Tests - Compliance
# ============================================================================


class TestComplianceContext:
    """Test Pure CAG strategy for compliance documentation."""

    def test_compliance_context_loaded(self):
        """Test that compliance context is loaded at module level."""
        assert COMPLIANCE_CONTEXT is not None
        assert isinstance(COMPLIANCE_CONTEXT, str)
        assert len(COMPLIANCE_CONTEXT) > 1000  # Should have substantial content

    def test_compliance_context_has_privacy_policy(self):
        """Test that compliance context includes privacy policy."""
        assert "PRIVACY POLICY" in COMPLIANCE_CONTEXT
        assert "privacy" in COMPLIANCE_CONTEXT.lower()

    def test_compliance_context_has_terms_of_service(self):
        """Test that compliance context includes terms of service."""
        assert "TERMS OF SERVICE" in COMPLIANCE_CONTEXT
        assert "terms" in COMPLIANCE_CONTEXT.lower()

    def test_compliance_context_is_static(self):
        """Test that compliance context doesn't change (static)."""
        # Get context multiple times
        from agents.tools.rag_tools import COMPLIANCE_CONTEXT as context1
        from agents.tools.rag_tools import COMPLIANCE_CONTEXT as context2

        # Should be the exact same object (loaded once)
        assert context1 is context2
        assert context1 == context2


# ============================================================================
# Strategy Comparison Tests
# ============================================================================


class TestStrategyBehaviors:
    """Test that different strategies behave as expected."""

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_pure_rag_always_retrieves(self, mock_get_vectorstore):
        """Test that Pure RAG strategies always hit the vector store."""
        mock_vectorstore = Mock()
        mock_vectorstore.similarity_search.return_value = [
            Document(page_content="Test", metadata={"source": "test.md"})
        ]
        mock_get_vectorstore.return_value = mock_vectorstore

        # Call technical search multiple times
        technical_docs_search.invoke({"query": "test1"})
        technical_docs_search.invoke({"query": "test2"})
        technical_docs_search.invoke({"query": "test3"})

        # Should call vector store every time (no caching)
        assert mock_vectorstore.similarity_search.call_count == 3

    def test_pure_cag_no_retrieval(self):
        """Test that Pure CAG has no retrieval mechanism."""
        # Compliance uses static context, not a retrieval tool
        # Just verify the context is available
        assert COMPLIANCE_CONTEXT is not None
        assert len(COMPLIANCE_CONTEXT) > 0

    @patch('agents.tools.rag_tools.get_vectorstore')
    def test_hybrid_caches_after_first_call(self, mock_get_vectorstore):
        """Test that Hybrid RAG/CAG caches after first retrieval."""
        from agents.tools.rag_tools import billing_docs_search as billing_fn
        from langgraph.types import Command
        
        mock_vectorstore = Mock()
        mock_vectorstore.similarity_search.return_value = [
            Document(page_content="Policy", metadata={"source": "test.md"})
        ]
        mock_get_vectorstore.return_value = mock_vectorstore

        # First call - no cache (returns Command with update)
        runtime1 = Mock()
        runtime1.state = {}
        result1 = billing_fn.func("policy", runtime1)
        assert isinstance(result1, Command)
        cached = result1.update["billing_policies"]

        # Second call - with cache (returns string)
        runtime2 = Mock()
        runtime2.state = {"billing_policies": cached}
        result2 = billing_fn.func("policy", runtime2)
        assert isinstance(result2, str)

        # Vector store should only be called once
        assert mock_vectorstore.similarity_search.call_count == 1

