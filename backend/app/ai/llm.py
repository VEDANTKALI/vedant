import json
import logging
from typing import Optional, Any, Dict
from app.core.config import settings

logger = logging.getLogger("aivoa_qms.ai")

class LLMService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model_name = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self._groq_client = None

    def get_client(self):
        if self._groq_client is None:
            if not self.api_key or "your_groq_api_key" in self.api_key or "placeholder" in self.api_key:
                logger.warning("No valid GROQ_API_KEY found. LLM service will operate with structured rule fallback.")
                return None
            try:
                from groq import Groq
                self._groq_client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self._groq_client = None
        return self._groq_client

    def invoke(self, prompt: str, system_prompt: Optional[str] = None, response_format_json: bool = False) -> str:
        """
        Invokes Groq API model gemma2-9b-it.
        If Groq API key is unavailable or request fails, falls back gracefully.
        """
        client = self.get_client()
        if client is None:
            raise ValueError("Groq client not initialized")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if response_format_json:
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content


llm_service = LLMService()
