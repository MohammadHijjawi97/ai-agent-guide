# Build Your Own AI Agent - A Beginner's Guide

This project walks you through building AI agents from scratch, starting with a simple chatbot and ending with a fully autonomous research assistant. Every lesson builds on the last one.

No machine learning degree required. If you know basic Python, you're ready.

---

## What is an AI Agent?

A regular chatbot answers questions. An AI agent takes actions.

An agent can browse information, run calculations, remember past conversations, and chain multiple steps together to solve a problem on its own. Think of it as giving a brain to a robot that can use tools.

---

## Lessons

| # | Lesson | What You Build |
|---|--------|---------------|
| 01 | Your First Chatbot | Talk to a language model via Python |
| 02 | Adding Tools | Let the agent call functions |
| 03 | Memory and Context | Give the agent a working memory |
| 04 | The ReAct Pattern | Teach the agent to reason step by step |
| 05 | Full Project | A research assistant with multiple tools |

---

## Prerequisites

- Python 3.9 or higher
- An OpenAI API key (get one at platform.openai.com)
- Basic Python knowledge (variables, functions, loops)

---

## Setup

Follow the steps in [SETUP.md](SETUP.md) before starting any lesson.

---

## How to Use This Guide

Work through the lessons in order. Each folder has:
- A `README.md` explaining the concept
- A Python file with the working code

Read the README first, then run the code, then try breaking it and experimenting.

---

## Concepts Covered

- Language model APIs and how they work
- The message/conversation loop
- Tool use and function calling
- Memory strategies: full history, summary, and sliding window
- The ReAct (Reason + Act) pattern
- Building a real agent with a loop that runs until the task is done

---

## Project Structure

```
ai-agent-guide/
├── README.md
├── SETUP.md
├── requirements.txt
├── .gitignore
└── lessons/
    ├── 01_your_first_chatbot/
    ├── 02_adding_tools/
    ├── 03_memory_and_context/
    ├── 04_react_pattern/
    └── 05_full_project/
```
