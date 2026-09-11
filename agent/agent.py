from pydantic import BaseModel, Field, model_validator
from typing import Literal, TypedDict
from openai import OpenAI
from dotenv import load_dotenv
import os
from .tools import ToolRegistry
from langgraph.graph import StateGraph, END

load_dotenv()
api = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api)


class ToolArguments(BaseModel):
    name: str
    value: str | int | float


class ToolDecision(BaseModel):
    action: Literal["tool", "answer"]
    tool_name: str | None = None
    arguments: list[ToolArguments] = Field(default_factory=list)
    answer: str | None = None

    @model_validator(mode="after")
    def action_validator(self):
        if self.action == "tool" and self.tool_name == None:
            raise ValueError("tool_name is required when action is tool")
        if self.action == "answer" and self.answer == None:
            raise ValueError("answer is required when action is answer")
        return self


class AgentState(TypedDict):
    message: str
    decision: ToolDecision | None
    history: list[dict]
    steps: int


class Agent:
    def __init__(self, tools: ToolRegistry):
        self.tools = tools

    def ask_llm(self, message, history=None):
        tool_schemas = self.tools.get_tool_descriptions()
        tool_instructions = f"""
Available tools: {tool_schemas}

If one of the available tools is appropriate:
- select that tool
- use its exact name
- provide arguments using its exact parameter names

If previous tool results are provided:
- use them to decide whether another tool is needed
- if another tool is needed, select it
- otherwise answer the original question

If no tool is needed:
- answer directly
"""

        if not history:
            llm_input = message
        else:
            llm_input = f"""
Original question: {message}
Previous tool result: {history} Decide what to do next.
"""
        response = client.responses.parse(
            model="gpt-5.6",
            instructions=tool_instructions,
            input=llm_input,
            text_format=ToolDecision,
        )

        return response.output_parsed

    def tool_call(self, decision: ToolDecision):
        tool = self.tools.get_tool(decision.tool_name)
        kwargs = {argument.name: argument.value for argument in decision.arguments}
        result = tool.execute(**kwargs)
        return result

    def agent_node(self, state: AgentState):
        message = state["message"]
        history = state["history"]

        decision = self.ask_llm(message, history)
        return {"decision": decision}

    def decision_route(self, state: AgentState):
        decision = state["decision"]
        if state["steps"] >= 5:
            return END
        if decision.action == "answer":
            return END
        elif decision.action == "tool":
            return "tool_node"

    def tool_node(self, state: AgentState):
        decision = state["decision"]
        history = state["history"].copy()
        try:
            tool_result = self.tool_call(decision)
        except Exception as e:
            tool_result = f"Tool Error: {str(e)}"
        history.append({"tool": decision.tool_name, "result": tool_result})

        return {"history": history, "steps": state["steps"] + 1}

    def build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("agent_node", self.agent_node)
        graph.add_node("tool_node", self.tool_node)
        graph.set_entry_point("agent_node")
        graph.add_conditional_edges("agent_node", self.decision_route)
        graph.add_edge("tool_node", "agent_node")
        app = graph.compile()
        return app
