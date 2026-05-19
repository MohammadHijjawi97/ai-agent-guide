# Build Your Own AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://platform.openai.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A step-by-step guide to building AI agents from scratch using Python and the OpenAI API. No frameworks. No magic. Pure fundamentals.

You start with a 30-line chatbot and end with a multi-agent pipeline that researches, writes, and edits content autonomously.

---

## Why This Guide Exists

Most AI agent tutorials either:
- Use a framework that hides everything interesting, or
- Assume you already know how LLMs work

This guide assumes only basic Python. Every concept is explained before the code, and every line of code does something you can understand.

---

## What You Will Build

```
Lesson 01   Simple chatbot            Talk to a model via the API
Lesson 02   Tool-using agent          Let the agent call Python functions
Lesson 03   Memory agent              Auto-summarize long conversations
Lesson 04   ReAct agent               Reason step by step before acting
Lesson 05   Full project              Modular research assistant with file I/O
Lesson 06   Multi-agent pipeline      Researcher + Writer + Editor agents
Lesson 07   RAG agent                 Answer questions from your own documents
```

---

## Architecture Overview

```
                        Your Question
                             |
                             v
              +------------------------------+
              |          Agent Loop          |
              |                              |
              |  1. Build messages           |
              |  2. Call LLM                 |
              |  3. Parse response           |
              |  4. Call tool (if needed)    |
              |  5. Add result, repeat       |
              +------------------------------+
                 |         |         |
                 v         v         v
            [Search]  [Calculate]  [Files]
               Tools - plain Python functions
```

RAG adds a retrieval step before the LLM call:

```
Question -> Retrieve relevant chunks -> Inject into prompt -> LLM answers
```

Multi-agent adds coordination:

```
Orchestrator -> Researcher -> Writer -> Editor -> Final output
```

---

## Getting Started

### Requirements

- Python 3.9 or higher
- An OpenAI API key (get one at https://platform.openai.com/api-keys)

### Setup

```bash
# Clone the repo
git clone https://github.com/MohammadHijjawi97/ai-agent-guide.git
cd ai-agent-guide

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="sk-..."    # Mac/Linux
$env:OPENAI_API_KEY = "sk-..."    # Windows PowerShell
```

See [SETUP.md](SETUP.md) for more detail.

---

## Lessons

### Lesson 01 - Your First Chatbot
```bash
cd lessons/01_your_first_chatbot
python chatbot.py
```
Covers: API calls, message format, conversation history, system prompts.

Also includes `chatbot_streaming.py` where tokens appear in real time.

### Lesson 02 - Adding Tools
```bash
cd lessons/02_adding_tools
python tool_agent.py
```
Covers: function calling, tool definitions, the tool dispatch loop.

### Lesson 03 - Memory and Context
```bash
cd lessons/03_memory_and_context
python memory_agent.py
```
Covers: sliding window, summarization memory, persistent storage across sessions.

### Lesson 04 - The ReAct Pattern
```bash
cd lessons/04_react_pattern
python react_agent.py
```
Covers: Reason + Act loop, structured output parsing, multi-step problem solving.

### Lesson 05 - Full Project
```bash
cd lessons/05_full_project
python main.py
```
Covers: modular agent class, multiple tools, file I/O, clean architecture.

### Lesson 06 - Multi-Agent Systems
```bash
cd lessons/06_multi_agent_systems
python multi_agent.py
```
Covers: agent specialization, pipeline orchestration, inter-agent communication.

### Lesson 07 - RAG Agent
```bash
cd lessons/07_rag_agent
python rag_agent.py
```
Covers: document chunking, TF-IDF retrieval, context injection, knowledge base Q&A.
Add your own `.txt` files to `lessons/07_rag_agent/documents/` and ask questions about them.

---

## Project Structure

```
ai-agent-guide/
├── README.md
├── SETUP.md
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── .github/
│   ├── workflows/test.yml
│   └── ISSUE_TEMPLATE/
└── lessons/
    ├── 01_your_first_chatbot/
    │   ├── README.md
    │   ├── chatbot.py
    │   └── chatbot_streaming.py
    ├── 02_adding_tools/
    │   ├── README.md
    │   └── tool_agent.py
    ├── 03_memory_and_context/
    │   ├── README.md
    │   └── memory_agent.py
    ├── 04_react_pattern/
    │   ├── README.md
    │   └── react_agent.py
    ├── 05_full_project/
    │   ├── README.md
    │   ├── main.py
    │   ├── agent.py
    │   └── tools.py
    ├── 06_multi_agent_systems/
    │   ├── README.md
    │   └── multi_agent.py
    └── 07_rag_agent/
        ├── README.md
        ├── rag_agent.py
        └── documents/
```

---

## Key Concepts at a Glance

| Concept | Lesson | One-line explanation |
|---------|--------|----------------------|
| Message loop | 01 | Send a list of messages, get a reply, repeat |
| System prompt | 01 | Instructions the model follows but the user never sees |
| Tool use | 02 | Model requests a function call, you run it, return result |
| Memory | 03 | Summarize old messages to stay within context limits |
| ReAct | 04 | Force the model to write its reasoning before each action |
| Multi-agent | 06 | Multiple specialized agents coordinated by an orchestrator |
| RAG | 07 | Retrieve relevant document chunks and inject as context |

---

## Cost

All lessons use `gpt-4o-mini`. Running the entire guide from start to finish costs well under $0.10.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests for new lessons, bug fixes, and improved explanations are welcome.

---

## License

MIT - see [LICENSE](LICENSE).
