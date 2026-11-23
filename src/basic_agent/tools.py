from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return "sunny, 22°C"