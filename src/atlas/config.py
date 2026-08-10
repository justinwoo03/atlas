from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env against the repo root, NOT the current working directory.
# `env_file=".env"` is relative to wherever you ran the command from, so it
# loads correctly from the repo root and silently loads NOTHING from anywhere
# else — every setting falls back to its default and your keys become empty
# strings. That surfaces as a 401 from the provider, which sends you
# debugging the wrong system entirely.
#
# __file__ is src/atlas/config.py, so parents[2] is the repo root. In the
# Docker image there is no .env and pydantic-settings tolerates that: on ECS
# the secrets arrive as real environment variables from the task definition.
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra="ignore")

    # -- Infrastructure -----------------------------------------------------
    database_url: str = "postgresql://atlas:atlas@localhost:5432/atlas"
    redis_url: str = "redis://localhost:6379/0"

    # -- Credentials --------------------------------------------------------
    # These MUST default to empty strings. This file is tracked by git; .env
    # is not. A real key as a default here is a key in your repo, and once
    # pushed it is public forever — deleting it later does not help, because
    # git history keeps every version of every file.
    #
    # Values come from .env locally, and from SSM Parameter Store via the ECS
    # task definition in production. Never from this file.
    anthropic_api_key: str = ""
    voyage_api_key: str = ""
    cohere_api_key: str = ""

    # -- Models -------------------------------------------------------------
    # Prices and IDs drift; keep them here rather than scattered inline.
    embedding_model: str = "voyage-4"
    embedding_dim: int = 1024
    generation_model: str = "claude-sonnet-5"
    cheap_model: str = "claude-haiku-4-5-20251001"

    # -- Reranking ----------------------------------------------------------
    # "local" runs a cross-encoder on your machine (no rate limits, which is
    # what makes week 4's benchmark and week 5's load test possible).
    # "cohere" uses the API.
    reranker: str = "local"
    cohere_rerank_model: str = "rerank-v3.5"
    local_rerank_model: str = "BAAI/bge-reranker-v2-m3"

    # -- Chunking -----------------------------------------------------------
    chunk_size: int = 512
    chunk_overlap: int = 64


settings = Settings()
