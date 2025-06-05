import logging
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.config.constants import MAX_REQUEST_SIZE
from src.domain.models import Document, SearchQuery, SearchResult
from src.application.interfaces import VectorStoreInterface, EmbeddingInterface
from src.infrastructure.vectorstores.weaviate_store import WeaviateVectorStore
from src.infrastructure.embeddings.openai_embeddings import OpenAIEmbeddings

logger = logging.getLogger(__name__)

app = FastAPI(title="Memexor API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
vector_store: VectorStoreInterface = WeaviateVectorStore()
embedding_service: EmbeddingInterface = OpenAIEmbeddings()

@app.post("/upload/text")
async def upload_text(file: UploadFile = File(...)):
    """Upload and index a text file."""
    if file.size and file.size > MAX_REQUEST_SIZE:
        raise HTTPException(413, "File too large")
    
    try:
        content = await file.read()
        text = content.decode()
        
        # Generate embedding
        embedding = await embedding_service.embed_text(text)
        
        # Create document and index
        doc = Document(
            id=file.filename,
            text=text,
            embedding=embedding,
            metadata={"filename": file.filename}
        )
        await vector_store.index([doc])
        
        return {"message": "File indexed successfully"}
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(500, "Error processing file")

@app.post("/tools/search", response_model=List[SearchResult])
async def search(query: SearchQuery):
    """Search for similar documents."""
    try:
        # Generate embedding if not provided
        if not query.embedding:
            query.embedding = await embedding_service.embed_text(query.text)
            
        results = await vector_store.search(query)
        return results
        
    except Exception as e:
        logger.error(f"Error performing search: {str(e)}")
        raise HTTPException(500, "Error performing search") 