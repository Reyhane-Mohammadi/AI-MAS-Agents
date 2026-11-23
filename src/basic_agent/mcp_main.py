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


async def main() -> None:
    model = ChatOpenAI(
        model=os.environ["MODEL"],
        timeout=20,
        max_retries=0,
        max_tokens=2048,
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
    print("Loaded MCP tools:", [t.name for t in tools])

    agent = create_agent(model, tools=tools)

    question = (
        "Use the add tool for 47832 + 91347, "
        "use the get_current_time tool, "
        "and use the count_words tool on this text: "
        "'agents use tools to act in the world'."
    )

    result = await agent.ainvoke(
        {"messages": [("user", question)]},
        config={"recursion_limit": 12},
    )

    for message in result["messages"]:
        for tc in getattr(message, "tool_calls", None) or []:
            print("  ->", tc["name"], tc["args"])
        print(f"[{message.type}]", message.content)


if __name__ == "__main__":
    asyncio.run(main())