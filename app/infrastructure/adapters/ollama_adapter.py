import os
from typing import List, Dict, Any, Generator
from ollamafreeapi import OllamaFreeAPI
from app.core.ports.llm_service import LLMService

class OllamaFreeAPIAdapter(LLMService):
    """Adapter for OllamaFreeAPI."""
    
    def __init__(self, base_url: str = None):
        # Base URL can be configured via env var
        self.client = OllamaFreeAPI(host=base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
        
    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Wraps the ollamafreeapi client chat call.
        """
        # Note: adjust parameters as per ollamafreeapi actual implementation
        response = self.client.chat(
            model=model,
            messages=messages,
            stream=False,
            options=kwargs
        )
        return response
        
    def stream_chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Generator[Dict[str, Any], None, None]:
        """
        Wraps the ollamafreeapi client streaming chat call.
        """
        return self.client.chat(
            model=model,
            messages=messages,
            stream=True,
            options=kwargs
        )
        
    def list_models(self) -> List[Dict[str, Any]]:
        """
        Returns a list of local models.
        """
        response = self.client.list()
        return response.get("models", [])
