import logging
from typing import List
import openai

from config.settings import OPENAI_API_KEY
from config.constants import OPENAI_MODEL, DEFAULT_BATCH_SIZE
from application.interfaces import EmbeddingInterface

logger = logging.getLogger(__name__)

class OpenAIEmbeddings(EmbeddingInterface):
    """OpenAI implementation of the embedding interface."""
    
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for a single text string."""
        try:
            response = await openai.Embedding.acreate(
                input=text,
                model=OPENAI_MODEL
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        embeddings = []
        
        # Process in batches to avoid rate limits
        for i in range(0, len(texts), DEFAULT_BATCH_SIZE):
            batch = texts[i:i + DEFAULT_BATCH_SIZE]
            try:
                response = await openai.Embedding.acreate(
                    input=batch,
                    model=OPENAI_MODEL
                )
                batch_embeddings = [data["embedding"] for data in response["data"]]
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                logger.error(f"Error generating batch embeddings: {str(e)}")
                raise
                
        return embeddings 