from agent import Tool, ToolRegistry, Agent
from agent.calculator import calculator
from pathlib import Path


def search_file(file_path, query):
    matches = []
    with open(file_path, "r") as file:
        for line in file:
            if query.lower() in line.lower():
                matches.append(line.strip())
    if matches:
        return matches
    return "query not found in given file"


calculator_tool = Tool(
    name="calculator",
    description="Safely evaluate mathematical expressions",
    function=calculator,
    parameters={"expression": "str"},
)
file_search = Tool(
    name="search_file",
    description="Search file for given query",
    function=search_file,
    parameters={"file_path": "str", "query": "str"},
)

registry = ToolRegistry()
registry.register(calculator_tool)
registry.register(file_search)

message = input("Query: ")
agent = Agent(registry)


app = agent.build_graph()

initial_state = {"message": message, "decision": None, "history": [], "steps": 0}

result = app.invoke(initial_state)
print(result)
