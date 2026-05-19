# Lesson 04 - The ReAct Pattern

## The Concept

In Lesson 02, we gave the agent tools and let it decide when to use them. That works for simple tasks. But for complex multi-step problems, the agent needs to think more deliberately.

The **ReAct pattern** (Reasoning + Acting) teaches the agent to think out loud before it acts. At each step, the agent must:

1. **Reason** - write down what it knows, what it needs, and what it plans to do next
2. **Act** - use a tool or produce the final answer
3. **Observe** - receive the result and go back to step 1

## Why This Matters

Without structured reasoning, agents can skip steps, use the wrong tool, or give up early. Forcing the model to write its thoughts makes errors more visible and easier to fix.

This is the same idea behind "chain of thought" prompting, but with a structured format and a real action loop.

## The Loop

```
[Thought]: I need to find X before I can answer Y.
[Action]: tool_name("argument")
[Observation]: result from the tool

[Thought]: Now I have X. I can compute Y.
[Action]: another_tool("argument")
[Observation]: result

[Thought]: I have everything I need.
[Answer]: Final response to the user.
```

The agent keeps looping until it writes `[Answer]` instead of `[Action]`.

## Parsing the Output

We parse the model's text response to extract:
- What type of step it is (Thought, Action, or Answer)
- The tool name and arguments if it's an Action

This parsing is done with simple string matching in `react_agent.py`.

## Tools in This Lesson

- `search` - simulates a web search and returns short snippets
- `calculate` - evaluates math expressions
- `lookup` - looks up a specific topic in a local knowledge base

## Run It

```bash
python react_agent.py
```

## Things to Try

- "How many days are there in 5 years and 3 months?"
- "What is the capital of France, and what is its population squared?"
- "Who invented the telephone, and in what year? Then calculate how many years ago that was."
