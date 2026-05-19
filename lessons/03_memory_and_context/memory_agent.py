import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MEMORY_FILE = Path(__file__).parent / "memory.txt"
MAX_MESSAGES = 10  # Summarize when we hit this many user/assistant pairs

SYSTEM_PROMPT = """You are a helpful personal assistant with excellent memory.
Pay attention to what the user tells you about themselves, their preferences, and their goals."""

SUMMARIZE_PROMPT = """The following is a conversation between you and the user.
Summarize the key points, facts about the user, decisions made, and anything important to remember.
Write the summary in second person as if talking to yourself ("The user told me...", "We discussed...").
Keep it under 200 words.

Conversation:
{conversation}"""


def load_memory() -> str:
    if MEMORY_FILE.exists():
        return MEMORY_FILE.read_text(encoding="utf-8").strip()
    return ""


def save_memory(summary: str):
    MEMORY_FILE.write_text(summary, encoding="utf-8")
    print(f"\n  [Memory saved to {MEMORY_FILE.name}]")


def summarize_conversation(messages: list[dict]) -> str:
    conversation_text = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in messages
        if m["role"] in ("user", "assistant")
    )

    prompt = SUMMARIZE_PROMPT.format(conversation=conversation_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def build_initial_messages(existing_memory: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if existing_memory:
        messages.append({
            "role": "system",
            "content": f"Here is a summary of your memory from previous conversations:\n\n{existing_memory}"
        })
        print("  [Loaded memory from previous session]\n")

    return messages


def get_response(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content


def count_exchanges(messages: list[dict]) -> int:
    return sum(1 for m in messages if m["role"] == "user")


def run_agent():
    print("=" * 50)
    print("  AI Agent with Memory")
    print("=" * 50)
    print(f"  Auto-summarizes after {MAX_MESSAGES} exchanges.")
    print("  Type 'quit' to exit, 'memory' to view current memory.\n")

    existing_memory = load_memory()
    messages = build_initial_messages(existing_memory)

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            if count_exchanges(messages) > 2:
                print("\n  Saving session to memory...")
                summary = summarize_conversation(messages)
                save_memory(summary)
            print("Goodbye!")
            break

        if user_input.lower() == "memory":
            mem = load_memory()
            if mem:
                print(f"\n  [Current memory]\n  {mem}\n")
            else:
                print("\n  [No memory saved yet]\n")
            continue

        messages.append({"role": "user", "content": user_input})

        response = get_response(messages)

        messages.append({"role": "assistant", "content": response})

        print(f"\nAgent: {response}\n")

        # Auto-summarize when the conversation grows too long
        if count_exchanges(messages) >= MAX_MESSAGES:
            print("\n  [Conversation is long. Summarizing to save memory...]\n")
            summary = summarize_conversation(messages)
            save_memory(summary)

            # Reset to a fresh conversation with the summary as context
            messages = build_initial_messages(summary)
            print("  [Memory compacted. Continuing with fresh context.]\n")


if __name__ == "__main__":
    run_agent()
