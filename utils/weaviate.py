import os
import requests
import uuid

# Default Weaviate connection parameters
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
WEAVIATE_INDEX = os.getenv("WEAVIATE_INDEX", "MemoryChunk")

def get_weaviate_url():
    """Get the Weaviate URL from environment variables or use default."""
    return WEAVIATE_URL

def get_weaviate_index():
    """Get the Weaviate index name from environment variables or use default."""
    return WEAVIATE_INDEX

def ensure_schema():
    """Ensure the MemoryChunk schema exists in Weaviate."""
    schema_check = requests.get(f"{WEAVIATE_URL}/v1/schema")
    if "MemoryChunk" not in schema_check.text:
        print("Creating MemoryChunk schema...")
        requests.post(f"{WEAVIATE_URL}/v1/schema", json={
            "class": "MemoryChunk",
            "description": "A chunk of memory ingested from a text, audio, or video stream.",
            "vectorizer": "text2vec-openai",
            "properties": [
                {"name": "content", "dataType": ["text"]},
                {"name": "source", "dataType": ["text"]},
                {"name": "timestamp", "dataType": ["text"]}
            ]
        })

def add_object(content, source, timestamp, vector):
    """Add an object to Weaviate with the given content, source, timestamp, and vector."""
    object_payload = {
        "class": WEAVIATE_INDEX,
        "id": str(uuid.uuid4()),  # unique object ID
        "properties": {
            "content": content,
            "source": source,
            "timestamp": timestamp
        },
        "vector": vector
    }

    response = requests.post(f"{WEAVIATE_URL}/v1/objects", json=object_payload)
    response.raise_for_status()
    return response.json()

def search_objects(query, limit=5):
    """Search for objects in Weaviate using the given query."""
    weaviate_payload = {
        "query": f"""
        {{
            Get {{
                {WEAVIATE_INDEX} (
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

    response = requests.post(f"{WEAVIATE_URL}/v1/graphql", json=weaviate_payload)
    response.raise_for_status()
    
    data = response.json()
    
    # Navigate the nested structure
    results = []
    try:
        entries = data["data"]["Get"].get(WEAVIATE_INDEX, [])
        for entry in entries:
            content = entry.get("content", "")
            source = entry.get("source", "unknown")
            timestamp = entry.get("timestamp", "no timestamp")
            formatted = f"[{timestamp}] {content} (source: {source})"
            results.append(formatted)
    except KeyError:
        results = ["No results found or unexpected Weaviate response."]
    
    return results