"""
Streaming version of the chatbot.
Tokens appear in real time instead of waiting for the full response.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = "You are a helpful and friendly assistant. Be clear and concise."


def stream_response(messages: list[dict]) -> str:
    full_response = ""

    print("Bot: ", end="", flush=True)

    with client.chat.completions.stream(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print("\n")
    return full_response


def run_chatbot():
    print("=" * 50)
    print("  Streaming Chatbot")
    print("=" * 50)
    print("Tokens stream in real time. Type 'quit' to exit.\n")

    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})
        response = stream_response(conversation)
        conversation.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    run_chatbot()
