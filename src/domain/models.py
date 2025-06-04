from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass(frozen=True)
class Document:
    """A document that can be stored in the vector store."""
    id: str
    text: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = None

@dataclass(frozen=True)
class SearchQuery:
    """A query to search the vector store."""
    text: str
    top_k: int = 5
    embedding: Optional[List[float]] = None

@dataclass(frozen=True)
class SearchResult:
    """A search result from the vector store."""
    document: Document
    score: float 