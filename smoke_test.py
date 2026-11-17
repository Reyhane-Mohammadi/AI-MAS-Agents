from basic_agent.main import agent

cases = [
    ("What is 47832 + 91347? Use the add tool.", ["add"]),
    ("What is the weather in Paris?", ["get_weather"]),
    ("Use add for 47+30, and also the weather in Paris.", ["add", "get_weather"]),
    ("Tell me a joke.", []),
]

for q, expect in cases:
    r = agent.invoke({"messages": [("user", q)]}, config={"recursion_limit": 10})
    called = [
        tc["name"]
        for m in r["messages"]
        for tc in (getattr(m, "tool_calls", None) or [])
    ]
    status = "PASS" if set(called) == set(expect) else "FAIL"
    print(status, "|", q[:45], "|", called)