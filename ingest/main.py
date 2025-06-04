# Modified main.py to use vector_db.py interface

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import os

# Import the vector_db interface
from utils.vector_db import get_vector_db

app = FastAPI()

# Initialize the vector database
vector_db = get_vector_db()

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
    # Use the vector_db interface to ensure schema
    vector_db.ensure_schema()

@app.post("/tools/search", response_model=MCPResponse)
async def mcp_search(req: MCPRequest):
    query = req.args.query
    # filters = req.args.filters  # Not used in current implementation, but kept for future use

    # Use the vector_db interface to search for objects
    results = vector_db.search_objects(query=query, limit=5)

    # If no results, provide a default message
    if not results:
        results = ["No results found."]

    return {"results": results}