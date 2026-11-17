import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from basic_agent.tools import add, get_weather

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MODEL", "llama-3.1-8b-instant"),
    timeout=20,
    max_retries=0,
)
agent = create_agent(llm, tools=[add, get_weather])

if __name__ == "__main__":
    q = "Use the add tool for 47832 + 91347, and tell me the weather in Paris."
    result = agent.invoke({"messages": [("user", q)]})
    for m in result["messages"]:
        for tc in getattr(m, "tool_calls", None) or []:
            print("  ->", tc["name"], tc["args"])
        print(f"[{m.type}]", m.content)