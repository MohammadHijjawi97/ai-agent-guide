from agent import ResearchAgent


HELP_TEXT = """
Commands:
  help   - show this help message
  reset  - clear the conversation and start over
  quit   - exit

Sample tasks:
  "Search for quantum computing and save a report."
  "What is today's date?"
  "Calculate the area of a circle with radius 14.5"
  "Search for machine learning, then compare it with AI in a saved report."
"""


def main():
    print("=" * 55)
    print("  Research Assistant - Full Agent Project")
    print("=" * 55)
    print("Type 'help' for commands or just ask me anything.\n")

    agent = ResearchAgent()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if cmd == "help":
            print(HELP_TEXT)
            continue

        if cmd == "reset":
            agent.reset()
            continue

        print()
        response = agent.chat(user_input)
        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()
