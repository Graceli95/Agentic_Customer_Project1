"""
Vector Store Module for RAG/CAG Implementation.

This module provides ChromaDB vector store instances for different domains.
Each domain (technical, billing, general) has its own vector store with
persistent storage.

Phase: 5 - RAG/CAG Integration
LangChain Version: 1.0+
Last Updated: November 4, 2025
"""

import logging
import os
from pathlib import Path
from typing import Optional

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)

# Base directory for all vector stores
CHROMA_BASE_DIR = Path(__file__).parent / "chroma_db"


def get_vectorstore(domain: str, embedding_model: str = "text-embedding-3-small") -> Optional[Chroma]:
    """
    Get or create a ChromaDB vector store for a specific domain.
    
    Args:
        domain: Domain name (technical, billing, general)
        embedding_model: OpenAI embedding model to use
        
    Returns:
        ChromaDB vector store instance, or None if initialization fails
        
    Example:
        >>> vectorstore = get_vectorstore("technical")
        >>> docs = vectorstore.similarity_search("error 500", k=3)
    """
    try:
        # Validate domain
        valid_domains = ["technical", "billing", "general"]
        if domain not in valid_domains:
            logger.error(f"Invalid domain: {domain}. Must be one of {valid_domains}")
            return None
        
        # Create persist directory for this domain
        persist_directory = CHROMA_BASE_DIR / domain
        persist_directory.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initializing vector store for domain: {domain}")
        logger.info(f"Persist directory: {persist_directory}")
        
        # Initialize embeddings
        embeddings = OpenAIEmbeddings(model=embedding_model)
        
        # Create or load ChromaDB vector store
        vectorstore = Chroma(
            collection_name=f"{domain}_docs",
            embedding_function=embeddings,
            persist_directory=str(persist_directory),
        )
        
        # Log collection info
        doc_count = vectorstore._collection.count()
        logger.info(f"Vector store loaded: {domain} ({doc_count} documents)")
        
        return vectorstore
        
    except Exception as e:
        logger.error(f"Failed to initialize vector store for {domain}: {e}")
        return None


def get_all_vectorstores() -> dict[str, Chroma]:
    """
    Get vector stores for all domains.
    
    Returns:
        Dictionary mapping domain names to vector store instances
        
    Example:
        >>> stores = get_all_vectorstores()
        >>> tech_docs = stores["technical"].similarity_search("error", k=3)
    """
    domains = ["technical", "billing", "general"]
    stores = {}
    
    for domain in domains:
        vectorstore = get_vectorstore(domain)
        if vectorstore:
            stores[domain] = vectorstore
        else:
            logger.warning(f"Could not load vector store for domain: {domain}")
    
    return stores


def clear_vectorstore(domain: str) -> bool:
    """
    Clear all documents from a domain's vector store.
    
    Useful for re-indexing or cleanup.
    
    Args:
        domain: Domain name to clear
        
    Returns:
        True if successful, False otherwise
    """
    try:
        persist_directory = CHROMA_BASE_DIR / domain
        
        if not persist_directory.exists():
            logger.info(f"No vector store exists for domain: {domain}")
            return True
        
        # Delete the entire directory
        import shutil
        shutil.rmtree(persist_directory)
        logger.info(f"Cleared vector store for domain: {domain}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to clear vector store for {domain}: {e}")
        return False


# Module-level initialization check
if __name__ == "__main__":
    # Test vector store initialization
    logging.basicConfig(level=logging.INFO)
    
    print("Testing vector store initialization...")
    print()
    
    for domain in ["technical", "billing", "general"]:
        print(f"Domain: {domain}")
        vs = get_vectorstore(domain)
        if vs:
            count = vs._collection.count()
            print(f"  ✓ Initialized ({count} documents)")
        else:
            print(f"  ✗ Failed to initialize")
        print()

