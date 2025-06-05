import logging
from typing import List
import weaviate
from src.config.settings import WEAVIATE_URL, WEAVIATE_CLASS
from src.domain.models import Document, SearchQuery, SearchResult
from src.application.interfaces import VectorStoreInterface

logger = logging.getLogger(__name__)

class WeaviateVectorStore(VectorStoreInterface):
    """Weaviate implementation of the vector store interface."""
    
    def __init__(self):
        self._client = weaviate.Client(WEAVIATE_URL)
        self._ensure_schema()
    
    def _ensure_schema(self) -> None:
        """Ensure the required schema exists in Weaviate."""
        if not self._client.schema.contains({"classes": [{"class": WEAVIATE_CLASS}]}):
            class_obj = {
                "class": WEAVIATE_CLASS,
                "vectorizer": "none",  # We provide vectors explicitly
                "properties": [
                    {"name": "text", "dataType": ["text"]},
                    {"name": "metadata", "dataType": ["object"],
                     "nestedProperties": [
                         {"name": "filename", "dataType": ["text"]},
                         {"name": "timestamp", "dataType": ["date"]},
                         {"name": "source", "dataType": ["text"]}
                     ]}
                ]
            }
            self._client.schema.create_class(class_obj)
            logger.info(f"Created schema for class {WEAVIATE_CLASS}")
    
    async def index(self, docs: List[Document]) -> None:
        """Add documents to the Weaviate index."""
        with self._client.batch as batch:
            for doc in docs:
                properties = {
                    "text": doc.text,
                    "metadata": doc.metadata or {
                        "filename": "unknown",
                        "timestamp": None,
                        "source": "unknown"
                    }
                }
                batch.add_data_object(
                    data_object=properties,
                    class_name=WEAVIATE_CLASS,
                    vector=doc.embedding
                )
        logger.info(f"Indexed {len(docs)} documents")
    
    async def search(self, query: SearchQuery) -> List[SearchResult]:
        """Search for similar documents in Weaviate."""
        result = (
            self._client.query
            .get(WEAVIATE_CLASS, ["text", "metadata"])
            .with_near_vector({"vector": query.embedding})
            .with_limit(query.top_k)
            .with_additional(["distance"])
            .do()
        )
        
        docs = []
        for item in result["data"]["Get"][WEAVIATE_CLASS]:
            doc = Document(
                id=item["_additional"]["id"],
                text=item["text"],
                metadata=item["metadata"],
                embedding=None  # We don't return embeddings
            )
            docs.append(SearchResult(
                document=doc,
                score=1 - item["_additional"]["distance"]
            ))
        
        return docs 