import os
import json
import math
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ─── Tool Functions ────────────────────────────────────────────────────────────

def calculate(expression: str) -> str:
    """Safely evaluate a math expression."""
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


def get_weather(city: str) -> str:
    """Return simulated weather for a given city."""
    data = {
        "london":    "Overcast, 14C, light wind from the west",
        "new york":  "Partly cloudy, 21C, calm",
        "tokyo":     "Light rain, 17C, humid",
        "dubai":     "Sunny, 38C, dry",
        "paris":     "Mostly sunny, 19C, gentle breeze",
        "sydney":    "Clear sky, 24C, warm",
        "berlin":    "Cloudy, 11C, strong wind",
        "toronto":   "Snow flurries, -3C, cold",
    }
    key = city.lower().strip()
    return data.get(key, f"No weather data available for '{city}'.")


def reverse_text(text: str) -> str:
    """Reverse a string of text."""
    return text[::-1]


# ─── Tool Registry ─────────────────────────────────────────────────────────────

TOOL_FUNCTIONS = {
    "calculate":    calculate,
    "get_weather":  get_weather,
    "reverse_text": reverse_text,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression and return the numeric result. Supports standard math operations and Python's math module functions like sqrt, sin, cos, log.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A Python math expression, e.g. '2 ** 8' or 'math.sqrt(144)'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather conditions for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'London' or 'Tokyo'"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reverse_text",
            "description": "Reverse a string of text character by character.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to reverse"
                    }
                },
                "required": ["text"]
            }
        }
    }
]


# ─── Agent Loop ────────────────────────────────────────────────────────────────

def run_agent(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to tools. Always use the appropriate tool when it helps you give a better or more accurate answer."
        },
        {"role": "user", "content": user_message}
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # Convert to a plain dict so we can append it
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                }
                for tc in (message.tool_calls or [])
            ] or None
        })

        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"  [Tool call: {name}({args})]")

            func = TOOL_FUNCTIONS.get(name)
            if func is None:
                result = f"Unknown tool: {name}"
            else:
                result = func(**args)

            print(f"  [Result: {result}]")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  AI Agent with Tools")
    print("=" * 50)
    print("Try: 'What is 99 to the power of 3?'")
    print("Try: 'What's the weather in London?'")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print()
        response = run_agent(user_input)
        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
