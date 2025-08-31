import os
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Personas
PERSONAS = {
    "professional": "You are a Professional Assistant. Explain budgeting and investments in simple financial language.",
    "creative": "You are a Creative Companion. Turn money lessons into stories and analogies (like 'your wallet is a garden').",
    "technical": "You are a Technical Expert. Provide detailed breakdowns of compound interest, savings rates, and tax calculations."
}

# Questions you want to test
QUESTIONS = [
    "How should a beginner start budgeting?",
    "Explain compound interest in a simple way.",
]

OUTPUT_FILE = Path("docs/prompt_comparison.md")


def ask_persona(client, persona_prompt, question):
    """Send the persona + question to Groq API."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # You can swap model if needed
        messages=[
            {"role": "system", "content": persona_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def main():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing GROQ_API_KEY in environment.")

    client = Groq(api_key=api_key)

    md_lines = [
        "# Prompt Comparison\n",
        "This table compares how different personas respond to the same financial question.\n",
    ]

    for q in QUESTIONS:
        md_lines.append(f"\n## Question: {q}\n")
        md_lines.append("| Persona | Response |\n")
        md_lines.append("|---------|----------|\n")

        results = {}
        for persona, prompt in PERSONAS.items():
            answer = ask_persona(client, prompt, q)
            results[persona] = answer
            md_lines.append(f"| **{persona.capitalize()}** | {answer.replace('|', ' ')} |\n")

        # Quick analysis
        analysis = f"""
**Analysis**:  
- Professional → {results['professional'][:80]}...  
- Creative → {results['creative'][:80]}...  
- Technical → {results['technical'][:80]}...  
"""
        md_lines.append(analysis)

    # Save to markdown
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"✅ Prompt comparison saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
