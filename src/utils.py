# src/utils.py
from typing import List, Dict

# A message is just a dict: {role: "system"|"user"|"assistant", content: str}
Message = Dict[str, str]


def start_history(system_prompt: str) -> List[Message]:
    """Initialize conversation history with a system prompt."""
    return [{"role": "system", "content": system_prompt}]


def append_user(history: List[Message], text: str) -> None:
    """Append a user message to history."""
    history.append({"role": "user", "content": text})


def append_assistant(history: List[Message], text: str) -> None:
    """Append an assistant message to history."""
    history.append({"role": "assistant", "content": text})


def truncate_history(history: List[Message], max_messages: int = 20) -> List[Message]:
    """
    (Optional) Limit history length to avoid huge context windows.
    Keeps system prompt + last N messages.
    """
    if len(history) <= max_messages:
        return history
    return [history[0]] + history[-(max_messages - 1):]
