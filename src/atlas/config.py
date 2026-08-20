from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# __file__ is src/atlas/config.py so parents[2] is the repo root
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra="ignore")

    # INFRASTRUCTURE
    database_url: str = "postgresql://atlas:atlas@localhost:5432/atlas"
    redis_url: str = "redis://localhost:6379/0"

    # CREDENTIALS
    # These MUST default to empty strings, get actually values from .env
    anthropic_api_key: str = ""
    voyage_api_key: str = ""
    cohere_api_key: str = ""

    # MODELS
    # Change model ID's or prices here
    embedding_model: str = "voyage-4"
    embedding_dim: int = 1024
    generation_model: str = "claude-sonnet-5"
    cheap_model: str = "claude-haiku-4-5-20251001"  # 1/3 cost of sonnet

    # RERANKING
    reranker: str = "local"
    voyage_rerank_model: str = "rerank-2.5"
    cohere_rerank_model: str = "rerank-v3.5"
    local_rerank_model: str = "BAAI/bge-reranker-v2-m3"

    # CHUNKING (tokens)
    chunk_size: int = 512
    chunk_overlap: int = 64


# module-level instance so multiple files that import settings can share one object``
settings = Settings()
