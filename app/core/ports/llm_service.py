from typing import List, Protocol
from typing import Any, Dict, Generator

class LLMService(Protocol):
    """Port for interacting with LLM providers."""
    
    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Send a chat request (non-streaming)."""
        ...
        
    def stream_chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Generator[Dict[str, Any], None, None]:
        """Send a chat request (streaming)."""
        ...
        
    def list_models(self) -> List[Dict[str, Any]]:
        """List available models in the backend."""
        ...
