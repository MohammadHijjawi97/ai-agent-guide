import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a friendly and knowledgeable assistant.
Keep your answers clear and concise. If you don't know something, say so."""


def get_response(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content


def run_chatbot():
    print("=" * 50)
    print("  Your First AI Chatbot")
    print("=" * 50)
    print("Type 'quit' or 'exit' to stop.\n")

    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})

        response = get_response(conversation)

        conversation.append({"role": "assistant", "content": response})

        print(f"\nBot: {response}\n")


if __name__ == "__main__":
    run_chatbot()
