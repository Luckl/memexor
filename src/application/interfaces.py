from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models import Document, SearchQuery, SearchResult

class VectorStoreInterface(ABC):
    """Abstract interface for vector stores."""
    
    @abstractmethod
    async def index(self, docs: List[Document]) -> None:
        """Add documents to the vector index."""
        ...

    @abstractmethod
    async def search(self, query: SearchQuery) -> List[SearchResult]:
        """Return documents most similar to the query."""
        ...

class EmbeddingInterface(ABC):
    """Abstract interface for embedding models."""
    
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for a text string."""
        ...

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        ... 