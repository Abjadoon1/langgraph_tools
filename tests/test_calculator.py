import pytest
from agent.calculator import calculator
import math


def test_normalcalculation():
    result = calculator("2 * 4")
    assert result == 8


def test_nested():
    result = calculator("2 * 4 + (22 / 4) ")
    assert result == 13.5


def test_support_function():
    result = calculator("sqrt(pi * 4)")
    assert result == pytest.approx(3.5449077018110318)


def test_invalid_expression():
    assert calculator("2 ** 4") == "Invalid Expression"


def test_invalid_format():
    assert calculator("abc * 4") == "Invalid Expression"


def test_invalid_value():
    assert calculator("2 + 8 / 0") == "Error: Division by Zero"


def test_constant():
    assert calculator("pi") == pytest.approx(math.pi)


def test_syntax_error():
    assert calculator("2 +") == "Error: Invalid expression syntax"


def test_unary_negative():
    assert calculator("-5 + 2") == -3


def test_nested_function():
    assert calculator("sqrt(16) + sin(pi / 2)") == pytest.approx(5)


def test_block_import():
    assert calculator("__import__('os')") == "Invalid Expression"


def test_block_attribute_access():
    assert calculator("math.sqrt(16)") == "Invalid Expression"
