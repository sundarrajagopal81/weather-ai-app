"""Client for interacting with local open-source LLM (Ollama-style API)."""
import requests
from config import get_llm_base_url, get_llm_model_name


def generate_chat_response(system_prompt: str, user_prompt: str) -> str:
    """
    Generate a chat response from the local LLM.
    
    Args:
        system_prompt: System message to set the assistant's behavior
        user_prompt: User message/question
        
    Returns:
        Generated text response from the LLM
        
    Raises:
        requests.RequestException: If the LLM server is unreachable or returns an error
    """
    base_url = get_llm_base_url()
    model_name = get_llm_model_name()
    
    url = f"{base_url}/api/chat"
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False  # Get complete response at once
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract the message content from the response
        # Ollama returns: {"message": {"role": "assistant", "content": "..."}, ...}
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()
        elif "content" in data:
            return data["content"].strip()
        else:
            raise ValueError("Unexpected LLM response format")
            
    except requests.exceptions.ConnectionError:
        raise requests.RequestException(
            f"LLM server not reachable. Make sure Ollama or your local LLM server "
            f"is running at {base_url}."
        )
    except requests.exceptions.Timeout:
        raise requests.RequestException(
            "LLM request timed out. The model might be taking too long to respond."
        )
    except requests.exceptions.HTTPError as e:
        raise requests.RequestException(
            f"LLM server returned an error: {e.response.status_code}. "
            f"Response: {e.response.text}"
        )
