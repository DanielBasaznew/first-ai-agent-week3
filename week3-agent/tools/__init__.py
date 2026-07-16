from .calculator import calculate
from .date_tool import get_date

# This is our central tool registry mapping string names to actual functions
TOOL_REGISTRY = {
    "calculator": calculate,
    "get_date": get_date
}