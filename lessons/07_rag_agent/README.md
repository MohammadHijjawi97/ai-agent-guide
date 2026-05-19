# Lesson 07 - RAG: Retrieval-Augmented Generation

## The Problem with LLMs

Language models have a knowledge cutoff. They don't know about your private documents, your company's internal wiki, or anything written after their training date. You can't just ask GPT-4 about your codebase or last month's meeting notes.

**RAG** (Retrieval-Augmented Generation) solves this.

## What RAG Does

Instead of relying only on the model's built-in knowledge, RAG:

1. **Loads** your documents into a searchable store
2. **Splits** them into small chunks
3. When a question comes in, **retrieves** the most relevant chunks
4. **Injects** those chunks into the prompt as context
5. The model **answers** using the retrieved information

```
Question: "What does our refund policy say?"

  -> Retrieve top 3 relevant chunks from your documents
  -> Prompt: "Answer based on this context: [chunks]"
  -> Answer: "According to the policy, refunds are..."
```

The model doesn't need to know the answer in advance - it reads it from your documents in real time.

## How Retrieval Works (Without a Vector Database)

Full RAG systems use vector databases (like Pinecone, Chroma, or FAISS) to store and search document embeddings. In this lesson, we build a lightweight version using:

- **TF-IDF** style scoring (term frequency) for keyword-based retrieval
- Simple cosine similarity for ranking chunks
- No external database required

This teaches the concept without the infrastructure. Once you understand it, switching to a real vector DB is straightforward.

## Files in This Lesson

- `rag_agent.py` - the full RAG pipeline
- `documents/` - a folder of sample `.txt` documents the agent learns from

## The Pipeline

```
Load .txt files from documents/
    -> Split into chunks (by paragraph)
        -> Build a simple word-frequency index
            -> On each question, score and retrieve top-K chunks
                -> Build prompt with retrieved context
                    -> Get answer from LLM
```

## Run It

```bash
python rag_agent.py
```

Add your own `.txt` files to the `documents/` folder and the agent will automatically learn from them.

## Things to Try

- Add a file about yourself and ask the agent questions about it
- Ask a question that no document can answer - watch it say so
- Change `TOP_K` in the code from 3 to 1 or 5 and see how it affects quality
- Try adding a long Wikipedia article as a `.txt` file and querying it
