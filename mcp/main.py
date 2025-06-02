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
