from agent import Tool, ToolRegistry, Agent
from agent.calculator import calculator
from agent.file_search import find_file, search_file
from agent.websearch_tool import search_web

calculator_tool = Tool(
    name="calculator",
    description="Safely evaluate mathematical expressions",
    function=calculator,
    parameters={"expression": "str"},
)

find_file_tool = Tool(
    name="find_file",
    description="Locate a file in local project folders when the exact file path is not known",
    function=find_file,
    parameters={"filename": "str"},
)

file_search_tool = Tool(
    name="search_file",
    description="Search inside a known file path for text matching a query",
    function=search_file,
    parameters={"file_path": "str", "query": "str"},
)

websearch_tool = Tool(
    name="search_web",
    description="Search the web for current or external information that is not available from local files or existing knowledge",
    function=search_web,
    parameters={"query": "str"},
)

registry = ToolRegistry()
registry.register(calculator_tool)
registry.register(find_file_tool)
registry.register(file_search_tool)
registry.register(websearch_tool)

message = input("Query: ")
agent = Agent(registry)


app = agent.build_graph()

initial_state = {"message": message, "decision": None, "history": [], "steps": 0}

result = app.invoke(initial_state)
print(print(result["history"]), result["decision"].answer)
