import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_text(text: str):
    response = openai.Embedding.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response['data'][0]['embedding']
