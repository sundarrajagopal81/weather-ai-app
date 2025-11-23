"""Configuration management using environment variables."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_llm_base_url() -> str:
    """Get the local LLM base URL from environment variables."""
    base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    return base_url.rstrip("/")


def get_llm_model_name() -> str:
    """Get the local LLM model name from environment variables."""
    model_name = os.getenv("LLM_MODEL_NAME", "llama3")
    if not model_name:
        raise ValueError(
            "LLM_MODEL_NAME not found in environment variables. "
            "Please set it in your .env file."
        )
    return model_name
