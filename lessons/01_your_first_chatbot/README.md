# Lesson 01 - Your First Chatbot

## The Concept

Every AI agent starts as a chatbot. Before we add memory or tools, we need to understand the fundamental loop that powers everything:

```
You send a message
    -> The model reads it and generates a response
        -> You display the response
            -> Repeat
```

That's it. The magic happens inside the model, but from our code's perspective, we're just sending text and receiving text.

## How the API Works

When you call an LLM API, you send a list of messages. Each message has two fields:

- `role` - who sent it: `"user"`, `"assistant"`, or `"system"`
- `content` - what was said

The model reads the entire list and writes the next message. This is how it appears to "remember" what was said earlier in the conversation.

```python
messages = [
    {"role": "system",    "content": "You are a helpful assistant."},
    {"role": "user",      "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user",      "content": "How do I install it?"},  # <-- latest message
]
```

The model sees all four messages and writes a response to the last one.

## The System Message

The first message with role `"system"` sets the behavior of the assistant. It's like giving instructions to an employee before the workday starts. The user never sees it directly.

## What the Code Does

`chatbot.py` runs a simple loop:
1. Ask the user for input
2. Append it to the conversation history
3. Send the full history to the model
4. Print and store the response
5. Go back to step 1

## Run It

```bash
python chatbot.py
```

## Things to Try

- Change the system message to give the bot a different personality
- Ask a follow-up question and see how it uses context from earlier in the conversation
- Print the full `messages` list to see what the model actually receives
