from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv()
SRC_DIR = str(Path(__file__).resolve().parents[1])

CASES = [
    ("What is 47832 + 91347? Use the add tool.", {"add"}),
    ("What is the weather in Paris?", {"get_weather"}),
    ("What time is it right now?", {"get_current_time"}),
    ("Use the count_words tool: how many words are in 'the quick brown fox jumps over the lazy dog'?", {"count_words"}),
    ("Use add for 47 + 30, and also tell me the time.", {"add", "get_current_time"}),
    ("Tell me a joke.", set()),
]


async def main() -> None:
    model = ChatOpenAI(
        model=os.environ["MODEL"], timeout=20, max_retries=0, max_tokens=2048
    )
    client = MultiServerMCPClient(
        {
            "basic": {
                "transport": "stdio",
                "command": sys.executable,
                "args": ["-m", "basic_agent.mcp_server"],
                "env": {"PYTHONPATH": SRC_DIR},
            }
        }
    )
    tools = await client.get_tools()
    agent = create_agent(model, tools=tools)

    for query, expected in CASES:
        result = await agent.ainvoke(
            {"messages": [("user", query)]},
            config={"recursion_limit": 12},
        )
        called = {
            tc["name"]
            for m in result["messages"]
            for tc in (getattr(m, "tool_calls", None) or [])
        }
        status = "PASS" if called == expected else "FAIL"
        print(f"{status} | {query[:50]:50} | expected={expected} got={called}")


if __name__ == "__main__":
    asyncio.run(main())