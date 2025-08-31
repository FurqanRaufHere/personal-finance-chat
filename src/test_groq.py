# src/test_groq.py
from src.llm_client import LLMClient
from src.prompts import get_system_prompt

def main():
    client = LLMClient()  # reads GROQ_API_KEY from env
    system = get_system_prompt("professional")
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": "As a student, what's one practical way to save $20/month?"}
    ]
    resp = client.chat(messages)
    print("=== Assistant Response ===")
    print(resp)

if __name__ == "__main__":
    main()
