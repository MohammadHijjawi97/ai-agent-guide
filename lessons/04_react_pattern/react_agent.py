import os
import math
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_STEPS = 10  # Prevent infinite loops


# ─── Tools ─────────────────────────────────────────────────────────────────────

KNOWLEDGE_BASE = {
    "python":         "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. Known for its readable syntax.",
    "eiffel tower":   "The Eiffel Tower is a wrought-iron lattice tower in Paris, France. Built in 1889 by Gustave Eiffel. Height: 330 meters.",
    "telephone":      "The telephone was invented by Alexander Graham Bell in 1876. The first words spoken were: 'Mr. Watson, come here. I want to see you.'",
    "moon":           "The Moon is Earth's only natural satellite. Distance from Earth: 384,400 km. Diameter: 3,474 km.",
    "mount everest":  "Mount Everest is the highest mountain on Earth at 8,849 meters above sea level. Located in the Himalayas on the Nepal-Tibet border.",
    "paris":          "Paris is the capital of France with a population of about 2.1 million in the city proper and 12 million in the greater metropolitan area.",
    "france":         "France is a country in Western Europe. Capital: Paris. Population: about 68 million. Official language: French.",
    "solar system":   "The solar system has 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
    "dna":            "DNA (deoxyribonucleic acid) is a molecule that carries genetic information. It has a double helix structure, discovered by Watson and Crick in 1953.",
}

SEARCH_INDEX = {
    "population":     "According to recent estimates, world population is about 8 billion people.",
    "speed of light": "The speed of light in a vacuum is approximately 299,792,458 meters per second.",
    "gravity":        "The gravitational acceleration on Earth's surface is approximately 9.81 m/s squared.",
    "water":          "Water (H2O) has a boiling point of 100 degrees Celsius and a freezing point of 0 degrees Celsius at sea level.",
    "pi":             "Pi is approximately 3.14159265358979. It is the ratio of a circle's circumference to its diameter.",
}


def search(query: str) -> str:
    query_lower = query.lower()
    for keyword, result in {**KNOWLEDGE_BASE, **SEARCH_INDEX}.items():
        if keyword in query_lower or query_lower in keyword:
            return result
    return f"No search results found for '{query}'. Try a more specific query."


def calculate(expression: str) -> str:
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


def lookup(topic: str) -> str:
    key = topic.lower().strip()
    if key in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[key]
    for k, v in KNOWLEDGE_BASE.items():
        if key in k or k in key:
            return v
    return f"No entry found for '{topic}' in the knowledge base."


TOOL_MAP = {
    "search":    search,
    "calculate": calculate,
    "lookup":    lookup,
}


# ─── System Prompt ─────────────────────────────────────────────────────────────

REACT_SYSTEM_PROMPT = """You are a reasoning agent. Solve problems step by step using this exact format:

[Thought]: Write what you know and what your next step is.
[Action]: tool_name("argument")

OR when you have the final answer:

[Thought]: I now have all the information needed.
[Answer]: Your complete answer here.

Available tools:
- search("query") - search for general information
- calculate("expression") - evaluate math using Python syntax (use math.sqrt, math.pi, etc.)
- lookup("topic") - look up a specific topic in the knowledge base

Rules:
- Always start with a [Thought].
- Every [Thought] must be followed by either [Action] or [Answer].
- Never skip a [Thought].
- Only one tool call per [Action] line.
- Stop as soon as you have a complete answer."""


# ─── Parser ────────────────────────────────────────────────────────────────────

def parse_step(text: str) -> tuple[str, str | None, str | None]:
    """
    Returns (step_type, tool_name, tool_arg) where step_type is
    'thought', 'action', or 'answer'.
    """
    action_match = re.search(r'\[Action\]:\s*(\w+)\("([^"]*)"\)', text, re.IGNORECASE)
    if action_match:
        return "action", action_match.group(1), action_match.group(2)

    answer_match = re.search(r'\[Answer\]:\s*(.+)', text, re.IGNORECASE | re.DOTALL)
    if answer_match:
        return "answer", None, answer_match.group(1).strip()

    return "thought", None, None


# ─── Agent Loop ────────────────────────────────────────────────────────────────

def run_react_agent(user_question: str) -> str:
    messages = [
        {"role": "system", "content": REACT_SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]

    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2,
            stop=["[Observation]"],
        )

        output = response.choices[0].message.content.strip()
        print(f"\n{output}")

        step_type, tool_name, tool_arg = parse_step(output)

        if step_type == "answer":
            return tool_arg

        if step_type == "action":
            tool_func = TOOL_MAP.get(tool_name)
            if tool_func is None:
                observation = f"Unknown tool '{tool_name}'. Available: search, calculate, lookup."
            else:
                observation = tool_func(tool_arg)

            observation_text = f"[Observation]: {observation}"
            print(observation_text)

            messages.append({"role": "assistant", "content": output})
            messages.append({"role": "user", "content": observation_text})
        else:
            # Only a thought, no action - push the model to continue
            messages.append({"role": "assistant", "content": output})
            messages.append({"role": "user", "content": "Continue."})

    return "Agent reached the step limit without producing a final answer."


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  ReAct Agent - Reasoning + Acting")
    print("=" * 55)
    print("Watch the agent think step by step.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print("\n" + "=" * 55)
        print("Agent is thinking...\n")

        answer = run_react_agent(user_input)

        print("\n" + "=" * 55)
        print(f"Final Answer: {answer}")
        print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
