# Contributing

Contributions are welcome and appreciated. This guide is for beginners, so contributions that improve clarity, fix bugs, or add new beginner-friendly examples are especially valued.

## What You Can Contribute

- Fix typos or unclear explanations in any README
- Improve existing code (performance, readability, correctness)
- Add a new lesson (see the Lesson Format section below)
- Add more sample documents to the RAG lesson
- Add new tools to any lesson
- Report bugs via GitHub Issues

## Getting Started

1. Fork the repository
2. Create a branch: `git checkout -b my-improvement`
3. Make your changes
4. Test that the code runs without errors
5. Open a Pull Request with a clear description of what you changed and why

## Lesson Format

Each lesson lives in its own folder under `lessons/`. A complete lesson has:

- `README.md` - explains the concept before showing any code
- One or more `.py` files with working, runnable code
- No dependencies beyond what is in the root `requirements.txt`

The README should follow this structure:
1. The concept (what problem are we solving?)
2. How it works (the key idea, with a simple diagram if helpful)
3. What the code does (overview, not line-by-line)
4. How to run it
5. Things to try (exercises to encourage experimentation)

## Code Style

- Python 3.9+
- No external libraries beyond `openai`, `python-dotenv`, and `requests`
- Clear variable names over clever one-liners
- Minimal comments - let the code speak for itself, add a comment only when the "why" is non-obvious

## Reporting Issues

Use GitHub Issues. Include:
- Which lesson you were running
- The exact error message
- Your Python version (`python --version`)
- Your OS

## Questions

Open a GitHub Discussion if you have a question about the material or want feedback on an idea before building it.
