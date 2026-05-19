import os
from dataclasses import dataclass, field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ─── Base Agent ────────────────────────────────────────────────────────────────

@dataclass
class Agent:
    name: str
    role: str
    history: list = field(default_factory=list)

    def __post_init__(self):
        self.history = [{"role": "system", "content": self.role}]

    def run(self, message: str) -> str:
        self.history.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            temperature=0.6,
        )

        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply


# ─── Specialist Agents ─────────────────────────────────────────────────────────

def make_researcher() -> Agent:
    return Agent(
        name="Researcher",
        role="""You are a research specialist. When given a topic, you produce a structured set of
research notes covering: key facts, historical context, current state, notable figures or examples,
and open questions. Be factual and thorough. Format as bullet points under clear headings.
Do not write prose - this is raw research material for a writer to use."""
    )


def make_writer() -> Agent:
    return Agent(
        name="Writer",
        role="""You are a skilled article writer. You receive research notes and transform them into
a well-structured, engaging article for a general audience. Your article should have:
- A compelling headline
- An introduction that hooks the reader
- 3 to 5 body sections with clear headings
- A conclusion with a takeaway
Write in an informative but accessible tone. No jargon without explanation."""
    )


def make_editor() -> Agent:
    return Agent(
        name="Editor",
        role="""You are a senior editor. You receive a draft article and improve it by:
- Fixing any grammar or clarity issues
- Improving sentence flow and word choice
- Ensuring logical structure and smooth transitions
- Making the opening paragraph stronger
- Cutting unnecessary words
Return the full polished article followed by a short "Editor's Notes" section listing
the main changes you made."""
    )


# ─── Pipeline Orchestrator ─────────────────────────────────────────────────────

def run_pipeline(topic: str) -> dict:
    print(f"\nStarting content pipeline for: '{topic}'")
    print("=" * 55)

    researcher = make_researcher()
    writer = make_writer()
    editor = make_editor()

    # Step 1: Research
    print(f"\n[1/3] Researcher is gathering information...")
    research_notes = researcher.run(
        f"Research this topic thoroughly: {topic}"
    )
    print(f"  Done. ({len(research_notes.split())} words of notes)")

    # Step 2: Write
    print(f"\n[2/3] Writer is drafting the article...")
    draft = writer.run(
        f"Write an article based on these research notes:\n\n{research_notes}"
    )
    print(f"  Done. ({len(draft.split())} words)")

    # Step 3: Edit
    print(f"\n[3/3] Editor is reviewing and polishing...")
    final = editor.run(
        f"Edit and improve this article draft:\n\n{draft}"
    )
    print(f"  Done. ({len(final.split())} words)")

    return {
        "topic":          topic,
        "research_notes": research_notes,
        "draft":          draft,
        "final_article":  final,
    }


def save_output(result: dict):
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    safe_name = result["topic"].replace(" ", "_").lower()[:40]
    path = os.path.join(output_dir, f"{safe_name}_article.md")

    content = f"""# Research Pipeline Output
**Topic:** {result['topic']}

---

## Research Notes

{result['research_notes']}

---

## First Draft

{result['draft']}

---

## Final Article

{result['final_article']}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n  Saved to: {path}")
    return path


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  Multi-Agent Content Studio")
    print("  Researcher -> Writer -> Editor")
    print("=" * 55)
    print("Enter a topic and three agents will collaborate to")
    print("produce a polished article.\n")

    while True:
        topic = input("Topic (or 'quit'): ").strip()

        if not topic:
            continue

        if topic.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = run_pipeline(topic)

        print("\n" + "=" * 55)
        print("FINAL ARTICLE")
        print("=" * 55)
        print(result["final_article"])

        save_output(result)

        again = input("\nRun another topic? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
