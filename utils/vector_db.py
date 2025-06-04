from abc import ABC, abstractmethod
import os
from typing import List, Dict, Any

class VectorDB(ABC):
    """Abstract base class for vector database operations."""
    
    @abstractmethod
    def ensure_schema(self):
        """Ensure the schema exists in the vector database."""
        pass
    
    @abstractmethod
    def add_object(self, content: str, source: str, timestamp: str, vector: List[float]):
        """Add an object to the vector database with the given content, source, timestamp, and vector."""
        pass
    
    @abstractmethod
    def search_objects(self, query: str, limit: int = 5) -> List[str]:
        """Search for objects in the vector database using the given query."""
        pass

class WeaviateDB(VectorDB):
    """Weaviate implementation of the VectorDB interface."""
    
    def __init__(self):
        import requests
        import uuid
        self.requests = requests
        self.uuid = uuid
        self.url = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
        self.index = os.getenv("WEAVIATE_INDEX", "MemoryChunk")
    
    def ensure_schema(self):
        """Ensure the MemoryChunk schema exists in Weaviate."""
        schema_check = self.requests.get(f"{self.url}/v1/schema")
        if "MemoryChunk" not in schema_check.text:
            print("Creating MemoryChunk schema...")
            self.requests.post(f"{self.url}/v1/schema", json={
                "class": "MemoryChunk",
                "description": "A chunk of memory ingested from a text, audio, or video stream.",
                "vectorizer": "text2vec-openai",
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {"name": "source", "dataType": ["text"]},
                    {"name": "timestamp", "dataType": ["text"]}
                ]
            })
    
    def add_object(self, content: str, source: str, timestamp: str, vector: List[float]):
        """Add an object to Weaviate with the given content, source, timestamp, and vector."""
        object_payload = {
            "class": self.index,
            "id": str(self.uuid.uuid4()),  # unique object ID
            "properties": {
                "content": content,
                "source": source,
                "timestamp": timestamp
            },
            "vector": vector
        }

        response = self.requests.post(f"{self.url}/v1/objects", json=object_payload)
        response.raise_for_status()
        return response.json()
    
    def search_objects(self, query: str, limit: int = 5) -> List[str]:
        """Search for objects in Weaviate using the given query."""
        weaviate_payload = {
            "query": f"""
            {{
                Get {{
                    {self.index} (
                        nearText: {{
                            concepts: ["{query}"]
                        }}
                        limit: {limit}
                    ) {{
                        content
                        source
                        timestamp
                    }}
                }}
            }}
            """
        }

        response = self.requests.post(f"{self.url}/v1/graphql", json=weaviate_payload)
        response.raise_for_status()
        
        data = response.json()
        
        # Navigate the nested structure
        results = []
        try:
            entries = data["data"]["Get"].get(self.index, [])
            for entry in entries:
                content = entry.get("content", "")
                source = entry.get("source", "unknown")
                timestamp = entry.get("timestamp", "no timestamp")
                formatted = f"[{timestamp}] {content} (source: {source})"
                results.append(formatted)
        except KeyError:
            results = ["No results found or unexpected Weaviate response."]
        
        return results

class MilvusDB(VectorDB):
    """Milvus implementation of the VectorDB interface."""
    
    def __init__(self):
        from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
        self.connections = connections
        self.Collection = Collection
        self.FieldSchema = FieldSchema
        self.CollectionSchema = CollectionSchema
        self.DataType = DataType
        self.utility = utility
        
        self.host = os.getenv("MILVUS_HOST", "localhost")
        self.port = os.getenv("MILVUS_PORT", "19530")
        self.collection_name = os.getenv("MILVUS_COLLECTION", "MemoryChunk")
        self.dim = 1536  # Dimension of OpenAI embeddings
        
        # Connect to Milvus
        self.connections.connect(host=self.host, port=self.port)
    
    def ensure_schema(self):
        """Ensure the MemoryChunk collection exists in Milvus."""
        if not self.utility.has_collection(self.collection_name):
            print(f"Creating {self.collection_name} collection...")
            
            # Define fields for the collection
            fields = [
                self.FieldSchema(name="id", dtype=self.DataType.INT64, is_primary=True, auto_id=True),
                self.FieldSchema(name="content", dtype=self.DataType.VARCHAR, max_length=65535),
                self.FieldSchema(name="source", dtype=self.DataType.VARCHAR, max_length=255),
                self.FieldSchema(name="timestamp", dtype=self.DataType.VARCHAR, max_length=255),
                self.FieldSchema(name="vector", dtype=self.DataType.FLOAT_VECTOR, dim=self.dim)
            ]
            
            # Create collection schema
            schema = self.CollectionSchema(fields=fields, description="Memory chunks from various sources")
            
            # Create collection
            collection = self.Collection(name=self.collection_name, schema=schema)
            
            # Create an IVF_FLAT index for vector field
            index_params = {
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
            collection.create_index(field_name="vector", index_params=index_params)
            collection.load()
    
    def add_object(self, content: str, source: str, timestamp: str, vector: List[float]):
        """Add an object to Milvus with the given content, source, timestamp, and vector."""
        collection = self.Collection(self.collection_name)
        
        # Insert data
        data = [
            [content],
            [source],
            [timestamp],
            [vector]
        ]
        
        collection.insert([data])
        return {"status": "success"}
    
    def search_objects(self, query: str, limit: int = 5) -> List[str]:
        """Search for objects in Milvus using the given query vector."""
        from utils.embeddings import embed_text
        
        # Generate embedding for the query
        query_vector = embed_text(query)
        
        collection = self.Collection(self.collection_name)
        collection.load()
        
        # Define search parameters
        search_params = {
            "metric_type": "COSINE",
            "params": {"nprobe": 10}
        }
        
        # Perform the search
        results = collection.search(
            data=[query_vector],
            anns_field="vector",
            param=search_params,
            limit=limit,
            output_fields=["content", "source", "timestamp"]
        )
        
        # Format results
        formatted_results = []
        for hits in results:
            for hit in hits:
                content = hit.entity.get("content", "")
                source = hit.entity.get("source", "unknown")
                timestamp = hit.entity.get("timestamp", "no timestamp")
                formatted = f"[{timestamp}] {content} (source: {source})"
                formatted_results.append(formatted)
        
        if not formatted_results:
            formatted_results = ["No results found."]
        
        return formatted_results

def get_vector_db() -> VectorDB:
    """Factory function to get the appropriate vector database implementation based on environment variables."""
    if os.getenv("MILVUS_HOST"):
        try:
            return MilvusDB()
        except ImportError:
            print("Warning: Milvus Python SDK not installed. Falling back to Weaviate.")
    
    # Default to Weaviate
    return WeaviateDB()