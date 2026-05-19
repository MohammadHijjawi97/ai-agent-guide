# Lesson 05 - Full Project: Research Assistant

## What We're Building

A research assistant that can:
- Search for information (simulated web search)
- Read and write local text files
- Perform calculations
- Keep a conversation history
- Save research reports to disk

This combines everything from Lessons 01 through 04 into one clean, modular codebase.

## File Structure

```
05_full_project/
├── README.md
├── main.py       - entry point and conversation loop
├── agent.py      - the agent class and loop logic
├── tools.py      - all tool functions and their definitions
└── output/       - saved reports appear here (created automatically)
```

## Architecture

```
main.py
  |
  v
Agent (agent.py)
  |-- manages conversation history
  |-- runs the tool loop
  |-- calls OpenAI API
  |
  v
Tools (tools.py)
  |-- search_web()
  |-- read_file()
  |-- write_file()
  |-- calculate()
  |-- get_current_date()
```

The `Agent` class in `agent.py` is the brain. It holds the conversation, calls the LLM, interprets tool calls, and dispatches them to `tools.py`. The tools are just plain functions that know nothing about the agent.

## Design Decisions

**Why separate tools.py from agent.py?**  
Tools should be testable on their own. You can import any function from `tools.py` directly in the Python shell without running the full agent.

**Why a class for the Agent?**  
The agent needs state (conversation history, system prompt). A class is the natural place for that. Functions would need to pass state around as arguments everywhere.

**Why not use frameworks like LangChain?**  
To show you exactly what's happening. Once you understand this code, frameworks will make sense. If you start with frameworks, you'll have no idea what's going on when something breaks.

## Run It

```bash
python main.py
```

## Sample Tasks to Try

- "Search for information about quantum computing and write a short report about it."
- "What is the square root of 8765, and save the calculation to a file called calc.txt"
- "Search for Python and search for machine learning, then compare them in a saved report."
- "What is today's date?"

## Extending This Project

Ideas for making it your own:
- Add a real web search using the SerpAPI or DuckDuckGo
- Connect to a real database and add a `query_db` tool
- Add a `send_email` tool (with careful guardrails!)
- Build a UI on top of it with Streamlit
- Add tool use logging to a SQLite file for auditing
