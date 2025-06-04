import pytest
from domain.models import Document, SearchQuery, SearchResult

def test_document_creation():
    """Test creating a Document instance."""
    doc = Document(
        id="test-1",
        text="Hello world",
        embedding=[0.1, 0.2, 0.3],
        metadata={"source": "test"}
    )
    assert doc.id == "test-1"
    assert doc.text == "Hello world"
    assert doc.embedding == [0.1, 0.2, 0.3]
    assert doc.metadata == {"source": "test"}

def test_search_query_defaults():
    """Test SearchQuery default values."""
    query = SearchQuery(text="test query")
    assert query.text == "test query"
    assert query.top_k == 5
    assert query.embedding is None

def test_search_result_creation():
    """Test creating a SearchResult instance."""
    doc = Document(id="test-1", text="Hello world")
    result = SearchResult(document=doc, score=0.95)
    assert result.document == doc
    assert result.score == 0.95 