import time
import logging
from .calculator import calculate
from .date_tool import get_date
from .wikipedia_tool import search_wikipedia
from .web_search import search_web  
from tools.weather_tool import get_weather

# Map tool names to their actual Python functions
TOOL_REGISTRY = {
    "calculator": calculate,
    "get_date": get_date,
    "wikipedia": search_wikipedia,
    "get_weather": get_weather,
    "search_web": search_web   
}

def execute_tool(name: str, argument: str) -> str:
    """
    Central router that finds and runs a tool by name.
    Guarantees a string output, retries on transient failures, 
    and prevents any tool crash from killing the agent loop.
    """
    clean_name = name.strip()
    
    # 3. Defensive Check: Handle LLM tool name hallucinations
    if clean_name not in TOOL_REGISTRY:
        valid_tools = ", ".join(TOOL_REGISTRY.keys())
        return f"[OBSERVATION Error]: Tool '{clean_name}' does not exist. Please use one of: [{valid_tools}]."
    
    # 4. Global Safety Net + Retry Loop
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            tool_function = TOOL_REGISTRY[clean_name]
            result = tool_function(argument)
            return str(result)
            
        except Exception as e:
            # If we still have retry attempts remaining, pause briefly and try again
            if attempt < max_retries:
                logging.warning(f"Tool '{clean_name}' failed on attempt {attempt + 1}. Retrying in 1 second...")
                time.sleep(1)
                continue
            # If all retries are exhausted, return the error message gracefully as an observation
            return f"[OBSERVATION Error]: The tool '{clean_name}' encountered an execution failure after {max_retries + 1} attempts. Details: {e}"