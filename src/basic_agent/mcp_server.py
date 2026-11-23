from __future__ import annotations

from datetime import datetime
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("basic-agent-tools")


@mcp.tool()
def add(
    a: Annotated[int, Field(description="First integer to add")],
    b: Annotated[int, Field(description="Second integer to add")],
) -> int:
    """Add two integers exactly. Use this for arithmetic instead of estimating."""
    return a + b


@mcp.tool()
def get_weather(
    city: Annotated[str, Field(description="City name, e.g. Paris")]
) -> str:
    """Get the current weather for a city. This is a stub for class use."""
    return "sunny, 22°C"


# ---------- دو ابزار جدید (تمرین) ----------

@mcp.tool()
def get_current_time() -> str:
    """Get the current local date and time of the computer running this server.
    Use for questions like 'what time is it?' or 'what is today's date?'.
    Do NOT use for weather or arithmetic."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@mcp.tool()
def count_words(
    text: Annotated[str, Field(description="The exact text to analyze")]
) -> str:
    """Count the words and characters in a given text exactly.
    Use when the user asks how many words or characters a text has.
    Do NOT use for arithmetic; use the add tool for that."""
    return f"words={len(text.split())}, characters={len(text)}"


if __name__ == "__main__":
    mcp.run()  # stdio transport