from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class AIProvider(ABC):
    @abstractmethod
    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate response with safety guardrails applied."""
        pass
