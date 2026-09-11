from agent import Tool, ToolRegistry, Agent, ToolDecision
from pathlib import Path

add = lambda a,b : a + b
sub = lambda a,b : a - b
mul = lambda a,b : a * b
div = lambda a,b : a / b

def search_file(file_path, query):
    matches= []
    with open(file_path, 'r') as file:
        for line in file:
            if query.lower() in line.lower():
                matches.append(line.strip())
    if matches:
        return matches
    return 'query not found in given file'

add_tool = Tool(name= 'add', description='add two numbers', function= add, parameters={'a':'number', 'b': 'number'})
sub_tool = Tool(name= 'sub', description='sub two numbers', function= sub, parameters={'a':'number', 'b': 'number'})
mul_tool = Tool(name= 'mul', description='mul two numbers', function= mul, parameters={'a':'number', 'b': 'number'})
div_tool = Tool(name= 'div', description='divide two numbers', function= div, parameters={'a':'number', 'b': 'number'})
file_search = Tool(name = 'search_file', description='Search file for given query', function= search_file, parameters={'file_path': 'str', 'query': 'str'})

registry = ToolRegistry()
registry.register(add_tool)
registry.register(sub_tool)
registry.register(mul_tool)
registry.register(div_tool)
registry.register(file_search)

message = input("Query: ")
agent = Agent(registry)


app = agent.build_graph()

initial_state = {
    "message": message,
    "decision": None,
    "history": [],
    "steps": 0
}

result = app.invoke(initial_state)
print(result['decision'].answer)