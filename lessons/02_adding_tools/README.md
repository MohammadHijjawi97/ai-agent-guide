# Lesson 02 - Adding Tools

## The Concept

A chatbot can only talk. An agent can act.

The key difference is **tools**: Python functions that the model can choose to call. Instead of guessing the answer to "What is 1847 * 293?", the agent calls your `calculate()` function and gets the exact result back.

This technique is called **function calling** or **tool use**.

## How It Works

You describe your tools to the model in a structured format (JSON schema). When the model decides to use a tool, it returns a special response that says: "I want to call `calculate` with argument `1847 * 293`". Your code then:

1. Reads which tool the model wants to use
2. Calls the actual Python function
3. Sends the result back to the model
4. The model uses that result to write the final answer

```
User: "What is 1847 times 293?"
    -> Model: "I'll use calculate(1847 * 293)"
        -> Your code calls calculate("1847 * 293") -> "541171"
            -> Model: "The answer is 541,171"
                -> User sees: "The answer is 541,171"
```

## The Tool Definition

Each tool is described like this:

```python
{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a math expression and return the result",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A Python math expression like '2 + 2'"
                }
            },
            "required": ["expression"]
        }
    }
}
```

The `description` fields are critical. The model reads them to decide when and how to use the tool. Write them like you're explaining to a smart person who has never seen your code.

## The Agent Loop

With tools, the flow becomes:

```
Send messages + tools
    -> Model responds with text OR a tool call
        -> If text: done, show the answer
        -> If tool call: run the function, add result, loop again
```

## Tools in This Lesson

- `calculate` - evaluates math expressions safely
- `get_weather` - returns simulated weather data for cities
- `reverse_text` - reverses a string

## Run It

```bash
python tool_agent.py
```

## Things to Try

- "What is 99 to the power of 3?"
- "What's the weather like in Tokyo?"
- "Reverse the phrase 'Hello World'"
- "What is the square root of 2025, and what is the weather in New York?"
  (Watch it use two tools in one turn!)
