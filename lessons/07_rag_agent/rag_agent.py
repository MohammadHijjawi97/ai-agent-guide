import os
import math
import re
from pathlib import Path
from collections import Counter
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DOCUMENTS_DIR = Path(__file__).parent / "documents"
CHUNK_SIZE    = 150   # words per chunk
TOP_K         = 3     # how many chunks to retrieve per query


# ─── Document Loading and Chunking ─────────────────────────────────────────────

def load_documents(docs_dir: Path) -> list[dict]:
    docs = []
    for path in docs_dir.glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        docs.append({"filename": path.name, "text": text})
    return docs


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_words = []

    for paragraph in paragraphs:
        words = paragraph.split()
        if len(current_words) + len(words) > chunk_size and current_words:
            chunks.append(" ".join(current_words))
            current_words = []
        current_words.extend(words)

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks


def build_index(docs: list[dict]) -> list[dict]:
    index = []
    for doc in docs:
        chunks = split_into_chunks(doc["text"])
        for i, chunk in enumerate(chunks):
            index.append({
                "source": doc["filename"],
                "chunk_id": i,
                "text": chunk,
                "tokens": tokenize(chunk),
            })
    return index


# ─── Simple TF-IDF Retrieval ───────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    return re.findall(r'\b[a-z]{2,}\b', text.lower())


def tf(term: str, tokens: list[str]) -> float:
    count = tokens.count(term)
    return count / len(tokens) if tokens else 0.0


def idf(term: str, index: list[dict]) -> float:
    docs_with_term = sum(1 for entry in index if term in entry["tokens"])
    if docs_with_term == 0:
        return 0.0
    return math.log(len(index) / docs_with_term)


def score_chunk(query_tokens: list[str], chunk: dict, index: list[dict]) -> float:
    return sum(
        tf(term, chunk["tokens"]) * idf(term, index)
        for term in set(query_tokens)
    )


def retrieve(query: str, index: list[dict], top_k: int = TOP_K) -> list[dict]:
    query_tokens = tokenize(query)
    scored = [
        (score_chunk(query_tokens, chunk, index), chunk)
        for chunk in index
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored[:top_k] if score > 0]


# ─── RAG Prompt Builder ────────────────────────────────────────────────────────

def build_prompt(question: str, retrieved: list[dict]) -> list[dict]:
    if not retrieved:
        context = "No relevant documents were found."
    else:
        parts = []
        for r in retrieved:
            parts.append(f"[Source: {r['source']}]\n{r['text']}")
        context = "\n\n".join(parts)

    system = """You are a knowledgeable assistant. Answer questions based on the provided context.
If the context does not contain enough information to answer, say so clearly.
Do not make up facts that are not in the context."""

    user = f"""Context:
{context}

Question: {question}

Answer based on the context above:"""

    return [
        {"role": "system", "content": system},
        {"role": "user",   "content": user},
    ]


def ask(question: str, index: list[dict]) -> tuple[str, list[dict]]:
    retrieved = retrieve(question, index)
    messages = build_prompt(question, retrieved)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
    )

    return response.choices[0].message.content, retrieved


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  RAG Agent - Retrieval-Augmented Generation")
    print("=" * 55)

    if not DOCUMENTS_DIR.exists():
        print(f"Error: documents/ folder not found at {DOCUMENTS_DIR}")
        return

    print(f"Loading documents from {DOCUMENTS_DIR.name}/...")
    docs = load_documents(DOCUMENTS_DIR)

    if not docs:
        print("No .txt files found. Add some to the documents/ folder.")
        return

    print(f"Loaded {len(docs)} document(s).")
    index = build_index(docs)
    print(f"Index built: {len(index)} chunks total.\n")
    print("Ask anything. The agent will retrieve relevant context before answering.")
    print("Type 'sources' after a question to see what was retrieved.")
    print("Type 'quit' to exit.\n")

    last_retrieved = []

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if user_input.lower() == "sources":
            if not last_retrieved:
                print("  No retrieval done yet.\n")
            else:
                print("\n  Retrieved chunks:")
                for r in last_retrieved:
                    print(f"  [{r['source']}] {r['text'][:100]}...")
                print()
            continue

        answer, last_retrieved = ask(user_input, index)
        sources = list({r["source"] for r in last_retrieved})

        print(f"\nAgent: {answer}")
        if sources:
            print(f"  (Sources: {', '.join(sources)})")
        print()


if __name__ == "__main__":
    main()
