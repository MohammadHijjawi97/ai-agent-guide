# Setup Guide

## Step 1 - Clone the Repo

If you haven't already:

```bash
git clone https://github.com/YOUR_USERNAME/ai-agent-guide.git
cd ai-agent-guide
```

## Step 2 - Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

## Step 3 - Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4 - Set Your API Key

Get a key at https://platform.openai.com/api-keys

Then set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

Or create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-your-key-here
```

The lessons that use `python-dotenv` will load it automatically.

## Step 5 - Verify Everything Works

```bash
python -c "from openai import OpenAI; print('Ready!')"
```

If you see `Ready!`, you're good to go.

---

## Cost Note

All lessons use `gpt-4o-mini`, which is very cheap. Running all lessons together costs less than a few cents.
