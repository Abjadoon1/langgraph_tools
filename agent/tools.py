class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        if tool.name in self.tools:
            raise ValueError("Tool already exists")
        self.tools[tool.name]   = tool

    def get_tool(self, name):
        if name not in self.tools:
            raise ValueError("Tool Not found")
        return self.tools[name]

    def list_tools(self):
        return list(self.tools)
    
    def get_tool_descriptions(self):
        tool_descriptions = {name: {'description': tool_obj.description,
                                    'parameters': tool_obj.parameters} 
                                    for name, tool_obj in self.tools.items()}
        return tool_descriptions
    