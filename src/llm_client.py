# src/llm_client.py
import os
from typing import List, Dict, Optional

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Groq client
from groq import Groq

# load .env if present
load_dotenv()

class LLMClient:
    """
    Small wrapper around the Groq Python client for chat completions.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile", temperature: float = 0.7):
        api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Set the environment variable or pass api_key.")
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10),
           retry=retry_if_exception_type(Exception))
    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        """
        Send a chat request. `messages` is a list of dicts like:
          {"role": "system"|"user"|"assistant", "content": "text"}
        Returns the assistant text (string).
        Retries transient errors up to 3 times.
        """
        temperature = self.temperature if temperature is None else temperature

        try:
            resp = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=temperature,
            )
        except Exception as exc:
            # You can inspect exc to handle rate limits or unauthorized differently.
            # For now, re-raise a clearer message.
            raise RuntimeError(f"Groq API request failed: {exc}") from exc

        # Groq returns choices similar to the example in their docs
        try:
            content = resp.choices[0].message.content
        except Exception:
            # Defensive fallback if structure differs
            content = str(resp)

        return content
