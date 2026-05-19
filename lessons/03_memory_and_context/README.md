# Lesson 03 - Memory and Context

## The Problem

In Lesson 01, we kept the full conversation history in a list. This works, but it has a cost: every API call sends the entire conversation. Long conversations get expensive and eventually hit the model's context limit.

Real agents need smart memory management.

## Three Memory Strategies

### 1. Full History (what we did in Lesson 01)
Keep every message. Simple but doesn't scale.

**Good for:** Short tasks, debugging  
**Bad for:** Long sessions, repeated use

### 2. Sliding Window
Keep only the last N messages. When the window is full, drop the oldest user/assistant pair.

```
[system] [user1] [bot1] [user2] [bot2] [user3] [bot3]
                         ^ drop this pair when limit hit
```

**Good for:** Long conversations where recent context matters most  
**Bad for:** When early context contains critical info

### 3. Summarization (what this lesson covers)
When the history grows too long, ask the model to compress it into a short summary. That summary becomes the new "memory" and gets inserted at the start of fresh conversations.

```
[system] [SUMMARY: earlier we talked about X, Y, Z] [recent messages...]
```

**Good for:** Very long sessions, retaining key facts over time  
**Bad for:** Requires an extra API call to summarize

## Episodic vs Semantic Memory

There are also two ways to think about what to store:

- **Episodic memory** - what happened: "The user asked about Python and I explained lists"
- **Semantic memory** - what was learned: "The user is a beginner who prefers simple examples"

The `memory_agent.py` in this lesson uses a summarization approach with semantic extraction.

## What the Code Does

`memory_agent.py` demonstrates:
- Tracking message count and token estimate
- Auto-summarizing when the conversation gets too long
- Inserting the summary back as context for the next turn
- Saving the final summary to a file so it persists across sessions

## Run It

```bash
python memory_agent.py
```

Have a long conversation and watch the agent summarize itself when it needs to.

## Things to Try

- Tell the agent several facts about yourself across many messages
- After it summarizes, ask it to recall what you told it
- Open the saved `memory.txt` file and read what it retained
