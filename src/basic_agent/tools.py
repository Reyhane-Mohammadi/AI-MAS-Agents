from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    return a + b

@tool
def get_weather(city: str) -> str:
    return "sunny, 22°C"