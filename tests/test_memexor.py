import requests
import pytest

INGEST_URL = "http://localhost:8000/upload/text"
MCP_URL = "http://localhost:8010/tools/search"

@pytest.fixture(scope="module")
def upload_sample_file():
    text = "This is a test document about the future of memory interfaces."
    files = {
        "file": ("sample.txt", text, "text/plain")
    }

    response = requests.post(INGEST_URL, files=files)
    assert response.status_code == 200, f"Ingest failed: {response.text}"
    return response.json()

def test_mcp_search(upload_sample_file):
    query = "memory interfaces"
    payload = {
        "tool": "search",
        "args": {"query": query}
    }

    response = requests.post(MCP_URL, json=payload)
    assert response.status_code == 200, f"Search failed: {response.text}"

    results = response.json().get("results", [])
    assert any("memory interfaces" in r.lower() for r in results), "Expected query result not found"
