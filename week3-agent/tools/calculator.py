import ast
import operator

# Define the mathematical operators we want to support
SUPPORTED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,  # To support negative numbers (e.g., -5)
    ast.UAdd: operator.pos,  # To support positive prefix (e.g., +5)
}

def safe_eval(node):
    """
    Recursively walks the Abstract Syntax Tree (AST) to evaluate only safe mathematical operations.
    """
    # 1. If it's a raw number, return it (ast.Constant handles this in modern Python)
    if isinstance(node, ast.Constant):
        return node.value
        
    # 2. If it's a binary operation (e.g., left_node + right_node)
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        
        if op_type in SUPPORTED_OPERATORS:
            # Handle division by zero safely
            if op_type == ast.Div and right == 0:
                raise ZeroDivisionError("division by zero is not allowed")
            return SUPPORTED_OPERATORS[op_type](left, right)
        else:
            raise TypeError(f"Unsupported operator: {node.op.__class__.__name__}")
            
    # 3. If it's a unary operation (e.g., -5)
    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in SUPPORTED_OPERATORS:
            return SUPPORTED_OPERATORS[op_type](operand)
        else:
            raise TypeError(f"Unsupported unary operator: {node.op.__class__.__name__}")
            
    # 4. Block everything else
    else:
        raise TypeError(f"Unsupported syntax: {node.__class__.__name__}")
def calculate(expression: str) -> str:
    """
    Calculates a math expression safely and returns the result as a string.
    Wraps execution in try/except to prevent crashes.
    """
    try:
        # Parse the string into an AST
        # mode='eval' expects a single expression
        tree = ast.parse(expression, mode='eval')
        
        # Evaluate the root of the tree
        result = safe_eval(tree.body)
        return str(result)
        
    except ZeroDivisionError:
        return "[OBSERVATION Error]: Division by zero is mathematically impossible."
    except Exception as e:
        return f"[OBSERVATION Error]: Could not calculate expression. Details: {e}"

# This block allows you to test the file directly
if __name__ == "__main__":
    # Test cases
    print("Testing basic math: 347 * 28 =", calculate("347 * 28"))
    print("Testing parenthesis: (100 + 50) / 3 =", calculate("(100 + 50) / 3"))
    print("Testing negative numbers: -10 * 5 =", calculate("-10 * 5"))
    print("Testing bad syntax evaluation: print('hello') =", calculate("print('hello')"))
    print("Testing division by zero: 5 / 0 =", calculate("5 / 0"))