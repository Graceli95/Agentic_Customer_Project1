"""
Document Loader Module for RAG/CAG Implementation.

This module handles loading and splitting documents from various file formats.
Supports .txt, .md, and .pdf files with configurable chunking.

Phase: 5 - RAG/CAG Integration
LangChain Version: 1.0+
Last Updated: November 4, 2025
"""

import logging
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

# Default chunking configuration
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200


def load_documents(
    directory: str | Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[Document]:
    """
    Load and split documents from a directory.
    
    Supports:
    - .txt files (TextLoader)
    - .md files (TextLoader - markdown is text)
    
    Args:
        directory: Path to directory containing documents
        chunk_size: Maximum characters per chunk
        chunk_overlap: Characters to overlap between chunks
        
    Returns:
        List of split document chunks with metadata
        
    Example:
        >>> docs = load_documents("backend/data/docs/technical")
        >>> print(f"Loaded {len(docs)} chunks")
    """
    directory_path = Path(directory)
    
    if not directory_path.exists():
        logger.error(f"Directory not found: {directory}")
        return []
    
    logger.info(f"Loading documents from: {directory}")
    
    all_documents = []
    
    try:
        # Load .txt files
        txt_loader = DirectoryLoader(
            str(directory_path),
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=False,
            use_multithreading=False,
        )
        txt_docs = txt_loader.load()
        logger.info(f"Loaded {len(txt_docs)} .txt files")
        all_documents.extend(txt_docs)
        
    except Exception as e:
        logger.warning(f"No .txt files found or error loading: {e}")
    
    try:
        # Load .md files (markdown is just text, so we can use TextLoader)
        md_loader = DirectoryLoader(
            str(directory_path),
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=False,
            use_multithreading=False,
        )
        md_docs = md_loader.load()
        logger.info(f"Loaded {len(md_docs)} .md files")
        all_documents.extend(md_docs)
        
    except Exception as e:
        logger.warning(f"No .md files found or error loading: {e}")
    
    if not all_documents:
        logger.warning(f"No documents found in {directory}")
        return []
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],  # Try paragraph, then line, then word
    )
    
    logger.info(f"Splitting {len(all_documents)} documents (chunk_size={chunk_size}, overlap={chunk_overlap})")
    split_documents = text_splitter.split_documents(all_documents)
    
    # Add chunk metadata
    for i, doc in enumerate(split_documents):
        doc.metadata["chunk_index"] = i
        doc.metadata["total_chunks"] = len(split_documents)
    
    logger.info(f"Created {len(split_documents)} chunks from {len(all_documents)} documents")
    
    return split_documents


def load_single_document(file_path: str | Path) -> str:
    """
    Load a single document file as plain text.
    
    Used for Pure CAG loading (compliance documents).
    
    Args:
        file_path: Path to document file
        
    Returns:
        Document content as string
        
    Example:
        >>> content = load_single_document("backend/data/docs/compliance/privacy-policy.md")
        >>> print(len(content))
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return ""
    
    try:
        # Determine loader based on extension
        extension = file_path.suffix.lower()
        
        if extension in [".txt", ".md"]:
            loader = TextLoader(str(file_path))
        else:
            logger.warning(f"Unsupported file type: {extension}, trying TextLoader")
            loader = TextLoader(str(file_path))
        
        docs = loader.load()
        
        if docs:
            content = docs[0].page_content
            logger.info(f"Loaded {file_path.name}: {len(content)} characters")
            return content
        else:
            logger.warning(f"No content found in {file_path}")
            return ""
            
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {e}")
        return ""


def get_document_stats(documents: List[Document]) -> dict:
    """
    Get statistics about loaded documents.
    
    Args:
        documents: List of document chunks
        
    Returns:
        Dictionary with stats (count, avg_length, total_chars)
    """
    if not documents:
        return {"count": 0, "avg_length": 0, "total_chars": 0}
    
    total_chars = sum(len(doc.page_content) for doc in documents)
    avg_length = total_chars // len(documents)
    
    return {
        "count": len(documents),
        "avg_length": avg_length,
        "total_chars": total_chars,
        "sources": len(set(doc.metadata.get("source", "") for doc in documents)),
    }


# Module-level test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testing document loader...")
    print()
    
    # Test loading from a directory
    test_dir = Path(__file__).parent / "docs" / "technical"
    if test_dir.exists():
        docs = load_documents(test_dir)
        stats = get_document_stats(docs)
        print(f"Loaded: {stats['count']} chunks from {stats['sources']} files")
        print(f"Average chunk size: {stats['avg_length']} characters")
    else:
        print(f"Test directory not found: {test_dir}")

