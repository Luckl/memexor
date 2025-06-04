from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import os
import requests

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
INDEX_NAME = os.getenv("WEAVIATE_INDEX", "MemoryChunk")  # class name in Weaviate schema

app = FastAPI()

class SearchArgs(BaseModel):
    query: str
    filters: dict = {}  # optional metadata filters

class MCPRequest(BaseModel):
    tool: str
    args: SearchArgs

class MCPResponse(BaseModel):
    results: List[str]

@app.on_event("startup")
def ensure_schema():
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

@app.post("/tools/search", response_model=MCPResponse)
async def mcp_search(req: MCPRequest):
    query = req.args.query
    filter_clauses = req.args.filters

    weaviate_payload = {
        "query": f"""
        {{
            Get {{
                {INDEX_NAME} (
                    nearText: {{
                        concepts: ["{query}"]
                    }}
                    limit: 5
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

    print("Payload:", weaviate_payload)
    print("Weaviate response:", response.text)

    response.raise_for_status()  # will raise HTTPError on 4xx/5xx

    data = response.json()

    # Navigate the nested structure
    results = []
    try:
        entries = data["data"]["Get"].get(INDEX_NAME, [])
        for entry in entries:
            content = entry.get("content", "")
            source = entry.get("source", "unknown")
            timestamp = entry.get("timestamp", "no timestamp")
            formatted = f"[{timestamp}] {content} (source: {source})"
            results.append(formatted)
    except KeyError:
        results = ["No results found or unexpected Weaviate response."]

    return {"results": results}