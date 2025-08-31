import argparse
import os
from groq import Groq
from dotenv import load_dotenv
from src.prompts import get_system_prompt
from src.utils import start_history, append_user, append_assistant, truncate_history

# Load environment variables from .env file
load_dotenv()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona", default="professional", help="Choose persona: professional, creative, technical")
    parser.add_argument("--stream", action="store_true", help="Stream output token by token")
    args = parser.parse_args()

    # Get system prompt for persona
    try:
        system_prompt = get_system_prompt(args.persona)
    except ValueError as e:
        print(e)
        return

    # Print disclaimer
    print("Disclaimer: This chat is for educational purposes only, not financial advice.\n")

    # Init history
    history = start_history(system_prompt)

    # Init Groq client
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye 👋")
            break

        append_user(history, user_input)
        history = truncate_history(history)

        if args.stream:
            # Streaming mode
            print("Assistant: ", end="", flush=True)
            response_text = ""
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=history,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.get("content", "")
                print(delta, end="", flush=True)
                response_text += delta
            print()
            append_assistant(history, response_text)
        else:
            # Non-streaming mode
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=history,
            )
            reply = response.choices[0].message.content
            print(f"Assistant: {reply}\n")
            append_assistant(history, reply)


if __name__ == "__main__":
    main()
