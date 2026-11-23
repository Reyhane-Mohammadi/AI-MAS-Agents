# Multi-Agent Systems — Learning Agentic Ai

This repository contains two exercises that build a tool-calling agent
with LangChain/LangGraph and an LLM served by Groq.

- **Exercise 1:** basic ReAct agent with two local tools
- **Exercise 2:** the same tools moved into an MCP server, plus two new tools

---

## Project structure
```
src/basic_agent/
  tools.py           # Exercise 1: add, get_weather (LangChain @tool)
  main.py            # Exercise 1: agent run
  mcp_server.py      # Exercise 2: MCP server with 4 tools
  mcp_main.py        # Exercise 2: agent connected to the MCP server
  routing_smoke.py   # Exercise 2: routing test (6 cases)
smoke_test.py        # Exercise 1: routing test (4 cases)
```

## Requirements
- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- A free Groq API key

## Setup
```
uv sync
```
Create a `.env` file in the project root (see `.env.example`):
```
OPENAI_API_KEY=your_groq_key_here
OPENAI_BASE_URL=https://api.groq.com/openai/v1
MODEL=openai/gpt-oss-20b
```
`.env` is listed in `.gitignore`, so the key is never committed.

On Windows (cmd), set the source path once per terminal:
```
set PYTHONPATH=src
```

---

## Exercise 1: Basic tool-calling agent

A ReAct agent: the LLM decides whether to call a tool, the program runs
the tool, and the result goes back to the LLM until it can answer.

Tools (`tools.py`):
- `add(a, b)` — exact integer addition
- `get_weather(city)` — returns fixed mock data

Run:
```
uv run python -m basic_agent.main
```
Test (4 cases: `add`, `get_weather`, both, and no tool):
```
uv run python smoke_test.py
```
Result: all 4 cases passed.

---

## Exercise 2: MCP server with two new tools

The tools now live in an MCP server (`mcp_server.py`, stdio transport).
The agent discovers them at runtime through `MultiServerMCPClient`.

Tools exposed (4):
- `add` and `get_weather` (from Exercise 1)
- `get_current_time` — **new**, returns the current local date and time
- `count_words` — **new**, counts words and characters in a text

Run:
```
uv run python -m basic_agent.mcp_main
```
Routing test (6 cases):
```
uv run python -m basic_agent.routing_smoke
```
Result: all 6 cases passed.

---

## Issues I ran into
- **Model not available:** `llama-3.1-8b-instant` returned a 404 for my
  key, so I listed the available models and used `openai/gpt-oss-20b`,
  which supports tool calling.
- **`No module named 'basic_agent'`:** Python did not find the `src`
  folder, so I set `PYTHONPATH=src`. For the MCP subprocess I pass the
  path explicitly through the `env` key in `MultiServerMCPClient`,
  because the environment variable is not inherited.
- **Missing docstring:** `@tool` raised a `ValueError` when a tool had
  no docstring. The docstring is what the model reads to choose a tool.
- **Empty answer with `max_tokens=512`:** the reasoning model used the
  budget for thinking, so I raised it to 2048.
- **Tool not called:** the model counted words itself instead of calling
  `count_words`. I made the request more explicit.
- **`run_python` skipped:** the Docker sandbox tool from the class
  example was not implemented (no Docker on my Windows setup).