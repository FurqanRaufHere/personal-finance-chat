# src/prompts.py
"""
Prompts and helpers for the Personal Finance Guide personas.

Provides:
- three system prompts (professional, creative, technical)
- a safety add-on appended to each prompt
- utility functions:
    - get_system_prompt(persona)
    - list_personas()
    - make_chat_messages(persona, user_text)
- a tiny CLI test when run as a script
"""

from typing import Dict, List

SAFETY_ADDON = (
    "\n\nImportant: This assistant provides educational information only and not financial, "
    "investment, or tax advice. Avoid recommending specific securities or personalized actions. "
    "If the user asks for regulated or jurisdiction-specific guidance, respond with a general "
    "educational explanation and suggest consulting a licensed professional."
)

PERSONAS: Dict[str, str] = {
    "professional": (
        "You are a professional personal-finance advisor for educational purposes. "
        "Explain budgeting, saving, debt management, and beginner investing in clear, practical language. "
        "Prefer step-by-step tips, short paragraphs, and concrete examples. Avoid personalized financial advice; keep it general and practical."
        + SAFETY_ADDON
    ),
    "creative": (
        "You are a creative companion who teaches money concepts using vivid analogies, micro-stories, and metaphors. "
        "Make lessons memorable and friendly. Always end with a short, actionable takeaway. Keep the advice general (educational, not personalized)."
        + SAFETY_ADDON
    ),
    "technical": (
        "You are a technical finance expert. Provide precise definitions, formulas, and step-by-step calculations "
        "(e.g., compound interest, savings rate, debt payoff timelines). When using math, show variables and the final numeric result. "
        "Keep scope educational; do not provide personalized investment advice."
        + SAFETY_ADDON
    ),
}

DEFAULT_PERSONA = "professional"


def get_system_prompt(persona: str) -> str:
    """
    Return the full system prompt for the given persona (case-insensitive).

    Raises:
        ValueError: if persona is not one of the available keys.
    """
    key = (persona or "").strip().lower()
    if not key:
        key = DEFAULT_PERSONA
    if key not in PERSONAS:
        available = ", ".join(sorted(PERSONAS.keys()))
        raise ValueError(f"Unknown persona: {persona!r}. Available personas: {available}")
    return PERSONAS[key]


def list_personas() -> List[str]:
    """Return a list of available persona keys."""
    return list(PERSONAS.keys())


def make_chat_messages(persona: str, user_text: str) -> List[Dict[str, str]]:
    """
    Build a chat-style messages list suitable for chat APIs.

    Example:
        messages = make_chat_messages("creative", "How can I save money on a student budget?")
        # messages => [
        #   {"role": "system", "content": "...system prompt..."},
        #   {"role": "user", "content": "How can I save money on a student budget?"}
        # ]
    """
    system_prompt = get_system_prompt(persona)
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text},
    ]


__all__ = [
    "SAFETY_ADDON",
    "PERSONAS",
    "DEFAULT_PERSONA",
    "get_system_prompt",
    "list_personas",
    "make_chat_messages",
]

# Small CLI/test helper so you can quickly sanity-check prompts.
if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Test prompts.py - show prompt and built chat messages.")
    parser.add_argument(
        "--persona",
        "-p",
        default=DEFAULT_PERSONA,
        choices=list_personas(),
        help="Persona to use (professional/creative/technical).",
    )
    parser.add_argument("user", nargs="*", help="User message to wrap (default example if omitted).")
    args = parser.parse_args()

    user_text = " ".join(args.user) if args.user else "What's one practical way to start saving money as a student?"
    print(f"Persona: {args.persona}\n")
    print("=== System prompt (first 800 chars) ===")
    print(get_system_prompt(args.persona)[:800] + ("\n..." if len(get_system_prompt(args.persona)) > 800 else "\n"))
    print("\n=== Chat messages (JSON) ===")
    print(json.dumps(make_chat_messages(args.persona, user_text), indent=2))
