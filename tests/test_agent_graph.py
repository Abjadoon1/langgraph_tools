import pytest

from agent import Agent, Tool, ToolRegistry, ToolDecision


@pytest.fixture
def registry():
    registry = ToolRegistry()

    def double(value):
        return value * 2

    double_tool = Tool(
        name="double",
        description="Double a number",
        function=double,
        parameters={"value": "int"},
    )

    registry.register(double_tool)

    return registry


@pytest.fixture
def agent(registry):
    return Agent(registry)


def initial_state(message="test"):
    return {
        "message": message,
        "decision": None,
        "history": [],
        "steps": 0,
    }


# 1. Direct answer:
# agent_node → decision_route → END
def test_direct_answer(agent, monkeypatch):

    decision = ToolDecision(action="answer", answer="Hello")

    monkeypatch.setattr(agent, "ask_llm", lambda message, history=None: decision)

    app = agent.build_graph()

    result = app.invoke(initial_state())

    assert result["decision"].action == "answer"
    assert result["decision"].answer == "Hello"
    assert result["history"] == []
    assert result["steps"] == 0


# 2. Tool call:
# agent → tool → agent → answer
def test_tool_routing(agent, monkeypatch):

    decisions = iter(
        [
            ToolDecision(
                action="tool",
                tool_name="double",
                arguments=[{"name": "value", "value": 5}],
            ),
            ToolDecision(action="answer", answer="The result is 10"),
        ]
    )

    monkeypatch.setattr(agent, "ask_llm", lambda message, history=None: next(decisions))

    app = agent.build_graph()

    result = app.invoke(initial_state())

    assert result["steps"] == 1

    assert len(result["history"]) == 1

    assert result["history"][0]["tool"] == "double"

    assert result["history"][0]["result"] == 10

    assert result["decision"].action == "answer"

    assert result["decision"].answer == "The result is 10"


# 3. Tool throws exception:
# graph should not crash
def test_tool_exception_is_added_to_history(agent, monkeypatch):

    def broken_tool(value):
        raise ValueError("Something went wrong")

    broken = Tool(
        name="broken",
        description="Tool that raises an error",
        function=broken_tool,
        parameters={"value": "int"},
    )

    agent.tools.register(broken)

    decisions = iter(
        [
            ToolDecision(
                action="tool",
                tool_name="broken",
                arguments=[{"name": "value", "value": 5}],
            ),
            ToolDecision(action="answer", answer="The tool failed"),
        ]
    )

    monkeypatch.setattr(agent, "ask_llm", lambda message, history=None: next(decisions))

    app = agent.build_graph()

    result = app.invoke(initial_state())

    assert len(result["history"]) == 1

    assert result["history"][0]["tool"] == "broken"

    assert result["history"][0]["result"] == "Tool Error: Something went wrong"

    assert result["decision"].action == "answer"


# 4. Multiple tool calls:
# agent → tool → agent → tool → agent → answer
def test_multiple_tool_calls(agent, monkeypatch):

    decisions = iter(
        [
            ToolDecision(
                action="tool",
                tool_name="double",
                arguments=[{"name": "value", "value": 2}],
            ),
            ToolDecision(
                action="tool",
                tool_name="double",
                arguments=[{"name": "value", "value": 4}],
            ),
            ToolDecision(action="answer", answer="Finished"),
        ]
    )

    monkeypatch.setattr(agent, "ask_llm", lambda message, history=None: next(decisions))

    app = agent.build_graph()

    result = app.invoke(initial_state())

    assert result["steps"] == 2

    assert len(result["history"]) == 2

    assert result["history"][0]["result"] == 4

    assert result["history"][1]["result"] == 8

    assert result["decision"].answer == "Finished"


# 5. Graph step limit
def test_graph_step_limit(agent, monkeypatch):

    decision = ToolDecision(
        action="tool", tool_name="double", arguments=[{"name": "value", "value": 2}]
    )

    monkeypatch.setattr(agent, "ask_llm", lambda message, history=None: decision)

    app = agent.build_graph()

    result = app.invoke(initial_state())

    assert result["steps"] == 5

    assert len(result["history"]) == 5

    # Current graph behaviour:
    # it stops while decision is still a tool decision.
    assert result["decision"].action == "tool"
    assert result["decision"].answer is None
