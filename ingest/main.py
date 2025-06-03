from fastapi import FastAPI, UploadFile, File
from utils.embeddings import embed_text
from utils.weaviate import ensure_schema, add_object

app = FastAPI()

@app.on_event("startup")
def startup_event():
    ensure_schema()

@app.post("/upload/text")
async def upload_text(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    vec = embed_text(content)

    # Add the object to Weaviate
    add_object(
        content=content,
        source=file.filename,
        timestamp="now",  # for now, could replace with actual timestamp
        vector=vec
    )

    return {
        "filename": file.filename,
        "embedding_preview": vec[:5],  # preview of the vector
        "weaviate_status": "ok"
    }
