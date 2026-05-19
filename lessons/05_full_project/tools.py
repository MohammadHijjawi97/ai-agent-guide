import math
import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"


# ─── Tool Functions ────────────────────────────────────────────────────────────

def search_web(query: str) -> str:
    """Simulate a web search. In a real project, replace this with a real API call."""
    database = {
        "python": (
            "Python is a high-level, general-purpose programming language created by Guido van Rossum "
            "and first released in 1991. It emphasizes code readability and simplicity. Python is widely "
            "used in web development, data science, artificial intelligence, automation, and scripting. "
            "Popular frameworks include Django, Flask, FastAPI, and NumPy."
        ),
        "machine learning": (
            "Machine learning is a subset of artificial intelligence that enables systems to learn "
            "from data without being explicitly programmed. Key categories include supervised learning, "
            "unsupervised learning, and reinforcement learning. Common algorithms: linear regression, "
            "decision trees, neural networks, and support vector machines."
        ),
        "quantum computing": (
            "Quantum computing uses quantum-mechanical phenomena like superposition and entanglement "
            "to perform computations. Unlike classical bits (0 or 1), quantum bits (qubits) can exist "
            "in multiple states simultaneously. Applications include cryptography, drug discovery, "
            "and optimization problems. Major players: IBM, Google, IonQ, and Rigetti."
        ),
        "artificial intelligence": (
            "Artificial intelligence (AI) refers to the simulation of human intelligence in machines. "
            "Modern AI is largely powered by large language models (LLMs), deep learning, and neural "
            "networks. Key milestones: Deep Blue (1997), AlphaGo (2016), GPT series (2018-present). "
            "Applications span healthcare, finance, autonomous vehicles, and creative tools."
        ),
        "climate change": (
            "Climate change refers to long-term shifts in global temperatures and weather patterns. "
            "Human activity since the Industrial Revolution has been the primary driver through "
            "greenhouse gas emissions. Effects include rising sea levels, more frequent extreme weather, "
            "and biodiversity loss. The Paris Agreement (2015) set a target of limiting warming to 1.5 degrees Celsius."
        ),
        "blockchain": (
            "Blockchain is a distributed ledger technology where data is stored in linked blocks across "
            "many computers, making it tamper-resistant. Originally developed for Bitcoin (2009). "
            "Applications beyond cryptocurrency: smart contracts, supply chain tracking, digital identity, "
            "and decentralized finance (DeFi)."
        ),
        "space exploration": (
            "Space exploration involves the investigation of outer space using astronomy and space technology. "
            "Key achievements: Moon landing (1969), International Space Station (1998-present), Mars rovers. "
            "Current frontiers: Mars colonization plans (SpaceX, NASA), James Webb Space Telescope discoveries, "
            "and commercial spaceflight."
        ),
    }

    query_lower = query.lower()
    for keyword, content in database.items():
        if keyword in query_lower or any(word in keyword for word in query_lower.split()):
            return f"Search results for '{query}':\n\n{content}"

    return (
        f"No results found for '{query}'. "
        "Try a broader query like 'python', 'machine learning', 'quantum computing', "
        "'artificial intelligence', 'climate change', 'blockchain', or 'space exploration'."
    )


def calculate(expression: str) -> str:
    """Evaluate a math expression safely."""
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {e}"


def write_file(filename: str, content: str) -> str:
    """Write content to a file in the output directory."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    safe_name = Path(filename).name  # Strip any directory traversal
    file_path = OUTPUT_DIR / safe_name
    file_path.write_text(content, encoding="utf-8")
    return f"File saved: {file_path}"


def read_file(filename: str) -> str:
    """Read a file from the output directory."""
    safe_name = Path(filename).name
    file_path = OUTPUT_DIR / safe_name
    if not file_path.exists():
        return f"File not found: {filename}"
    return file_path.read_text(encoding="utf-8")


def get_current_date() -> str:
    """Return the current date and time."""
    now = datetime.now()
    return now.strftime("Today is %A, %B %d, %Y. The time is %H:%M.")


def list_files() -> str:
    """List all saved files in the output directory."""
    if not OUTPUT_DIR.exists():
        return "No files saved yet."
    files = list(OUTPUT_DIR.iterdir())
    if not files:
        return "No files saved yet."
    names = [f.name for f in files if f.is_file()]
    return "Saved files:\n" + "\n".join(f"  - {n}" for n in names)


# ─── Tool Dispatcher ───────────────────────────────────────────────────────────

TOOL_FUNCTIONS = {
    "search_web":      search_web,
    "calculate":       calculate,
    "write_file":      write_file,
    "read_file":       read_file,
    "get_current_date": get_current_date,
    "list_files":      list_files,
}


def call_tool(name: str, arguments: dict) -> str:
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return f"Unknown tool: '{name}'"
    try:
        return func(**arguments)
    except TypeError as e:
        return f"Tool argument error: {e}"


# ─── Tool Definitions (for OpenAI API) ─────────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search for information on a topic. Returns a summary of relevant content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g. 'machine learning' or 'climate change'"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression. Supports Python math syntax including math.sqrt, math.pi, math.log, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A Python math expression, e.g. '2 ** 10' or 'math.sqrt(144)'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Save text content to a file. Use this to write reports, notes, or any text the user wants to save.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The filename, e.g. 'report.txt' or 'notes.md'"
                    },
                    "content": {
                        "type": "string",
                        "description": "The full text content to write to the file"
                    }
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a previously saved file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The filename to read, e.g. 'report.txt'"
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get the current date and time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files that have been saved in this session.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]
