import os
import logging
from modules.config import LLM_PROVIDER

# Cache the LLM instance so it is not re-created on every request
_llm_cache = None

def get_llm():
    """
    Centralized module for LLM selection.
    Hardcoded to use Ollama with llama3.1.
    Caches the instance for faster subsequent calls.
    """
    global _llm_cache
    if _llm_cache is not None:
        return _llm_cache
    
    model_name = "llama3.1"
    logging.info(f"Loading LLM model: {model_name} via ollama")
    
    from langchain_community.llms import Ollama
    try:
        _llm_cache = Ollama(
            model=model_name,
            temperature=0.3,
            num_predict=512,
        )
        return _llm_cache
    except Exception as e:
        logging.error(f"Failed to load Ollama model {model_name}: {e}")
        return None
