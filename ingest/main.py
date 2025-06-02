from fastapi import FastAPI, UploadFile, File
from utils.embeddings import embed_text
import requests
import os
import uuid

app = FastAPI()

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
WEAVIATE_INDEX = os.getenv("WEAVIATE_INDEX", "MemoryChunk")

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

@app.post("/upload/text")
async def upload_text(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    vec = embed_text(content)

    # Create the Weaviate object payload
    object_payload = {
        "class": WEAVIATE_INDEX,
        "id": str(uuid.uuid4()),  # unique object ID
        "properties": {
            "content": content,
            "source": file.filename,
            "timestamp": "now"  # for now, could replace with actual timestamp
        },
        "vector": vec
    }

    response = requests.post(f"{WEAVIATE_URL}/v1/objects", json=object_payload)
    response.raise_for_status()

    return {
        "filename": file.filename,
        "embedding_preview": vec[:5],  # preview of the vector
        "weaviate_status": "ok"
    }
