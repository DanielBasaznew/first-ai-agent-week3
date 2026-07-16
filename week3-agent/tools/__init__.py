from .calculator import calculate
from .date_tool import get_date
from .wikipedia_tool import search_wikipedia

# Map tool names to their actual Python functions
TOOL_REGISTRY = {
    "calculator": calculate,
    "get_date": get_date,
    "wikipedia": search_wikipedia  
}