import ast
import math

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
}

CONSTANTS = {"pi": math.pi}


def calculator(expression: str):
    try:
        tree = ast.parse(expression, mode="eval")
        if not validation_node(tree):
            return "Invalid Expression"
        return evaluation_node(tree.body)
    except SyntaxError:
        return f"Error: Invalid expression syntax"
    except ZeroDivisionError:
        return f"Error: Division by Zero"
    except ValueError as e:
        return f"Error: {str(e)}"


def validation_node(node):
    if isinstance(node, ast.Expression):
        return validation_node(node.body)

    elif isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float))

    elif isinstance(node, ast.Name):
        return node.id in CONSTANTS

    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, (ast.USub, ast.UAdd)):
            return False
        return validation_node(node.operand)

    elif isinstance(node, ast.BinOp):
        if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            return False
        return validation_node(node.left) and validation_node(node.right)

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in FUNCTIONS:
            return False
        return all(validation_node(arg) for arg in node.args)

    else:
        return False


def evaluation_node(node):
    if isinstance(node, ast.Constant):
        return node.value

    elif isinstance(node, ast.BinOp):
        left = evaluation_node(node.left)
        right = evaluation_node(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right

    elif isinstance(node, ast.Name):
        constant = CONSTANTS[node.id]
        return constant

    elif isinstance(node, ast.UnaryOp):
        value = evaluation_node(node.operand)

        if isinstance(node.op, ast.USub):
            return -value
        elif isinstance(node.op, ast.UAdd):
            return +value

    elif isinstance(node, ast.Call):
        func = FUNCTIONS[node.func.id]
        evaluate = [evaluation_node(args) for args in node.args]
        result = func(*evaluate)
        return result
