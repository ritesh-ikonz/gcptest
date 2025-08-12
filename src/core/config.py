import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from google.cloud import secretmanager
from..services.llm_service import LLMService

class Settings(BaseSettings):
    gcp_project_id: str | None = os.environ.get("GCP_PROJECT_ID")
    groq_api_key_secret_name: str = "groq-api-key"

@lru_cache
def get_settings() -> Settings:
    return Settings()

@lru_cache
def get_groq_api_key() -> str:
    """
    Retrieves the Groq API key from Google Cloud Secret Manager.
    Caches the result to avoid repeated API calls.
    """
    settings = get_settings()
    if not settings.gcp_project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{settings.gcp_project_id}/secrets/{settings.groq_api_key_secret_name}/versions/latest"
    
    try:
        response = client.access_secret_version(request={"name": secret_name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        # In a real app, add more robust error handling and logging
        raise RuntimeError(f"Failed to access secret: {e}") from e

@lru_cache
def get_llm_service() -> LLMService:
    """
    FastAPI dependency to create and cache a singleton LLMService instance.
    """
    api_key = get_groq_api_key()
    return LLMService(api_key=api_key)