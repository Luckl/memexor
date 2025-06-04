# Vector store defaults
DEFAULT_VECTOR_DIMENSION: int = 1536  # OpenAI ada-002 dimension
DEFAULT_TOP_K: int = 5
DEFAULT_BATCH_SIZE: int = 32

# Weaviate configuration
WEAVIATE_CLASS: str = "Document"
WEAVIATE_URL_ENV: str = "WEAVIATE_URL"
DEFAULT_WEAVIATE_URL: str = "http://localhost:8080"

# OpenAI configuration
OPENAI_API_KEY_ENV: str = "OPENAI_API_KEY"
OPENAI_MODEL: str = "text-embedding-ada-002"

# File paths and directories
UPLOAD_DIR: str = "/tmp/memexor/uploads"
LOG_DIR: str = "/var/log/memexor"

# API configuration
MAX_REQUEST_SIZE: int = 10 * 1024 * 1024  # 10MB
REQUEST_TIMEOUT: int = 30  # seconds 