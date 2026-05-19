import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOL_DEFINITIONS, call_tool

load_dotenv()

SYSTEM_PROMPT = """You are a research assistant with access to several tools.

Your capabilities:
- Searching for information on topics
- Performing calculations
- Reading and writing files
- Telling the current date and time
- Listing saved files

Be thorough but concise. When asked to write a report, produce well-structured, readable content.
When searching, do not fabricate information - only use what the search tool returns.
Always confirm when you have saved a file."""


class ResearchAgent:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.history: list[dict] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def _append(self, role: str, content: str, tool_calls=None, tool_call_id: str = None):
        msg: dict = {"role": role, "content": content}
        if tool_calls is not None:
            msg["tool_calls"] = tool_calls
        if tool_call_id is not None:
            msg["tool_call_id"] = tool_call_id
        self.history.append(msg)

    def _call_llm(self) -> object:
        return self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            temperature=0.5,
        )

    def chat(self, user_message: str) -> str:
        self._append("user", user_message)

        while True:
            response = self._call_llm()
            msg = response.choices[0].message

            if not msg.tool_calls:
                self._append("assistant", msg.content)
                return msg.content

            # Build serializable tool_calls list
            tool_calls_data = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                }
                for tc in msg.tool_calls
            ]

            self._append("assistant", msg.content or "", tool_calls=tool_calls_data)

            for tc in msg.tool_calls:
                name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    args = {}

                print(f"  [Tool] {name}({self._format_args(args)})")
                result = call_tool(name, args)
                print(f"  [Result] {result[:120]}{'...' if len(result) > 120 else ''}")

                self._append(
                    role="tool",
                    content=result,
                    tool_call_id=tc.id
                )

    def _format_args(self, args: dict) -> str:
        if not args:
            return ""
        parts = []
        for k, v in args.items():
            if isinstance(v, str) and len(v) > 40:
                parts.append(f'{k}="{v[:40]}..."')
            else:
                parts.append(f'{k}="{v}"')
        return ", ".join(parts)

    def reset(self):
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        print("  [Conversation cleared]")
