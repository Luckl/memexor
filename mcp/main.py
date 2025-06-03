from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from utils.weaviate import ensure_schema, search_objects

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
def startup_event():
    ensure_schema()

@app.post("/tools/search", response_model=MCPResponse)
async def mcp_search(req: MCPRequest):
    query = req.args.query
    # Note: filter_clauses are not currently used in the search_objects function

    # Use the search_objects function from the weaviate utility
    results = search_objects(query, limit=5)

    return {"results": results}
