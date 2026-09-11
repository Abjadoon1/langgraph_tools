import pytest
from agent import models, calculator
from agent.tools import ToolRegistry


@pytest.fixture
def registry():
    tool1 = models.Tool(
        name="calculator",
        description="Safely evaluate mathematical expressions",
        function=calculator,
        parameters={"expression": "str"},
    )
    registry = ToolRegistry()
    registry.register(tool1)
    return registry


def test_registertools(registry):
    assert "calculator" in registry.tools


def test_get_registered_tool(registry):
    tool = registry.get_tool("calculator")
    assert tool.name == "calculator"


def test_list_alltools(registry):
    tool = registry.list_tools()
    assert len(tool) == 1


def test_duplicatetools(registry):
    tool2 = models.Tool(
        name="calculator",
        description="Safely evaluate mathematical expressions",
        function=calculator,
        parameters={"expression": "str"},
    )
    with pytest.raises(ValueError, match="Tool already exists"):
        registry.register(tool2)


def test_notregistered(registry):
    with pytest.raises(ValueError, match="Tool Not found"):
        registry.get_tool("web_search")
