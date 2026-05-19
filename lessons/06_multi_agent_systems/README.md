# Lesson 06 - Multi-Agent Systems

## The Concept

One agent is smart. A team of agents is powerful.

Multi-agent systems split a complex task across several specialized agents, each with a defined role. Just like a company has researchers, writers, and editors, an agent pipeline can too.

## Why Multiple Agents?

A single agent handling a long, multi-step task tends to:
- Lose track of the goal partway through
- Mix up responsibilities (researching while trying to write)
- Produce lower quality output than a focused specialist

Splitting into roles forces clarity. Each agent does one thing well, then hands off.

## The Pipeline in This Lesson

We build a "Content Studio" with three agents and one orchestrator:

```
Orchestrator
    |
    |-- Researcher Agent   -> gathers facts on a topic
    |-- Writer Agent       -> turns facts into a draft article
    |-- Editor Agent       -> reviews and polishes the draft
    |
    v
Final published article
```

Each agent has its own system prompt, its own role, and its own output format. The orchestrator sequences them and passes outputs between them.

## Communication Patterns

There are two common ways agents communicate:

**Pipeline (what we build here)**
```
Agent A -> Agent B -> Agent C
```
Simple, predictable, good for linear workflows.

**Blackboard / Shared State**
```
All agents read/write a shared "workspace"
```
More flexible, better for tasks where order isn't fixed.

## What the Code Does

`multi_agent.py` defines:
- `Agent` class: a simple wrapper around a system prompt and a conversation
- `ResearcherAgent`: searches for facts on a given topic
- `WriterAgent`: receives research notes and writes a structured article
- `EditorAgent`: receives the draft and returns an improved version with feedback
- `run_pipeline()`: orchestrates the full flow and saves the result

## Run It

```bash
python multi_agent.py
```

Enter any topic and watch three agents collaborate to produce a polished article.

## Things to Try

- "quantum computing"
- "the history of the internet"
- "why sleep is important"
- Change the `WriterAgent`'s system prompt to write in a different style (technical, casual, poetic)
- Add a fourth "FactChecker" agent between the Researcher and Writer
