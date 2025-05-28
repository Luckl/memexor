from fastapi import FastAPI, UploadFile, File
from utils.embeddings import embed_text
import requests

app = FastAPI()

@app.post("/upload/text")
async def upload_text(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    vec = embed_text(content)
    # TODO: push to Weaviate
    return {"filename": file.filename, "embedding": vec[:5]}  # preview
