#!/usr/bin/env python3
"""
Document Indexing Script for RAG/CAG Implementation.

This script loads documents from the docs directory and indexes them into
ChromaDB vector stores for retrieval.

Usage:
    python scripts/index_documents.py --domain technical
    python scripts/index_documents.py --domain billing
    python scripts/index_documents.py --domain general
    python scripts/index_documents.py --all

Phase: 5 - RAG/CAG Integration
Last Updated: November 4, 2025
"""

import argparse
import logging
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.document_loader import load_documents, get_document_stats
from data.vectorstore import get_vectorstore, clear_vectorstore

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def index_domain(domain: str, force: bool = False) -> bool:
    """
    Index documents for a specific domain.
    
    Args:
        domain: Domain name (technical, billing, general)
        force: If True, clear existing index before indexing
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"{'='*60}")
        logger.info(f"Indexing domain: {domain}")
        logger.info(f"{'='*60}")
        
        # Clear existing index if force flag set
        if force:
            logger.info(f"Force flag set - clearing existing vector store for {domain}")
            clear_vectorstore(domain)
        
        # Load documents from domain directory
        docs_dir = Path(__file__).parent.parent / "data" / "docs" / domain
        
        if not docs_dir.exists():
            logger.error(f"Directory not found: {docs_dir}")
            return False
        
        logger.info(f"Loading documents from: {docs_dir}")
        documents = load_documents(docs_dir)
        
        if not documents:
            logger.warning(f"No documents found in {docs_dir}")
            return False
        
        # Print statistics
        stats = get_document_stats(documents)
        logger.info(f"Loaded {stats['count']} chunks from {stats['sources']} source files")
        logger.info(f"Average chunk size: {stats['avg_length']} characters")
        logger.info(f"Total content: {stats['total_chars']} characters")
        
        # Get or create vector store
        logger.info(f"Initializing vector store for domain: {domain}")
        vectorstore = get_vectorstore(domain)
        
        if not vectorstore:
            logger.error(f"Failed to initialize vector store for {domain}")
            return False
        
        # Check if already indexed
        existing_count = vectorstore._collection.count()
        if existing_count > 0 and not force:
            logger.warning(f"Vector store already contains {existing_count} documents")
            logger.warning(f"Use --force to re-index (will clear existing data)")
            return False
        
        # Add documents to vector store
        logger.info(f"Adding {len(documents)} chunks to vector store...")
        vectorstore.add_documents(documents)
        
        # Verify indexing
        final_count = vectorstore._collection.count()
        logger.info(f"✓ Successfully indexed {final_count} documents for {domain}")
        
        # Test retrieval
        logger.info("Testing retrieval...")
        test_query = {
            "technical": "error 500",
            "billing": "refund policy",
            "general": "company services"
        }.get(domain, "information")
        
        results = vectorstore.similarity_search(test_query, k=2)
        logger.info(f"Test query '{test_query}' returned {len(results)} results")
        
        if results:
            logger.info(f"Sample result: {results[0].page_content[:100]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"Error indexing domain {domain}: {e}", exc_info=True)
        return False


def main():
    """Main entry point for indexing script."""
    parser = argparse.ArgumentParser(
        description="Index documents into ChromaDB vector stores",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Index technical documents
  python scripts/index_documents.py --domain technical
  
  # Index all domains
  python scripts/index_documents.py --all
  
  # Force re-index (clear existing)
  python scripts/index_documents.py --domain billing --force
        """
    )
    
    parser.add_argument(
        "--domain",
        choices=["technical", "billing", "general"],
        help="Domain to index"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Index all domains"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Clear existing index before indexing"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.domain and not args.all:
        parser.error("Either --domain or --all must be specified")
    
    # Determine which domains to index
    if args.all:
        domains = ["technical", "billing", "general"]
        logger.info("Indexing all domains...")
    else:
        domains = [args.domain]
    
    # Index each domain
    success_count = 0
    failure_count = 0
    
    for domain in domains:
        if index_domain(domain, force=args.force):
            success_count += 1
        else:
            failure_count += 1
        print()  # Blank line between domains
    
    # Print summary
    logger.info(f"{'='*60}")
    logger.info("Indexing Summary")
    logger.info(f"{'='*60}")
    logger.info(f"Successfully indexed: {success_count} domain(s)")
    if failure_count > 0:
        logger.warning(f"Failed to index: {failure_count} domain(s)")
    logger.info(f"{'='*60}")
    
    # Exit with appropriate code
    sys.exit(0 if failure_count == 0 else 1)


if __name__ == "__main__":
    main()

