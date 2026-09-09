"""
Base class for LLM providers
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @property
    @abstractmethod
    def enabled(self) -> bool:
        """Whether the provider is properly configured"""

    @property
    @abstractmethod
    def default_model(self) -> str:
        """The default model to use"""
    
    @property
    @abstractmethod
    def analysis_model(self) -> str:
        """The model to use for code analysis"""

    @abstractmethod
    def chat_completion(
        self, 
        messages: list[dict[str, Any]], 
        model: str | None = None,
        **kwargs
    ) -> str | None:
        """Send a chat completion request to the provider
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Optional model override (uses default_model if not provided)
            **kwargs: Additional arguments (max_tokens, temperature, etc.)
        
        Returns:
            The response content string, or None if failed
        """
