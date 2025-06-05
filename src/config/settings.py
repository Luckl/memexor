import os
from pathlib import Path
from dotenv import load_dotenv

from config.constants import (
    WEAVIATE_URL_ENV,
    DEFAULT_WEAVIATE_URL,
    OPENAI_API_KEY_ENV,
    UPLOAD_DIR,
    LOG_DIR,
    WEAVIATE_CLASS
)

# Load environment variables from .env file
load_dotenv()

# Vector store settings
WEAVIATE_URL: str = os.getenv(WEAVIATE_URL_ENV, DEFAULT_WEAVIATE_URL)

# OpenAI settings
OPENAI_API_KEY: str = os.getenv(OPENAI_API_KEY_ENV)
if not OPENAI_API_KEY:
    raise ValueError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")

# Ensure directories exist
for directory in [UPLOAD_DIR, LOG_DIR]:
    Path(directory).mkdir(parents=True, exist_ok=True)

# Re-export WEAVIATE_CLASS for convenience
__all__ = ['WEAVIATE_URL', 'OPENAI_API_KEY', 'WEAVIATE_CLASS'] 