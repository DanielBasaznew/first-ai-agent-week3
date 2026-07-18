import os
import sys
import re
from google import genai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from prompts import SYSTEM_PROMPT
import time
import sys

load_dotenv()

import logging

# Configure background file logger to append details silently to 'agent.log'
logging.basicConfig(
    filename='agent.log',
    filemode='a', # 'a' means append so it saves previous test sessions too
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

console = Console()

try:
    client = genai.Client()
except Exception as e:
    console.print(f"[bold red]Initialization Error:[/bold red] Make sure GEMINI_API_KEY is set in your .env. Details: {e}")
    sys.exit(1)



def call_llm(messages: list, max_retries: int = 3, initial_delay: int = 3) -> str:
    """
    Helper function to call Gemini 3.5 Flash with our running conversation history.
    Includes automated exponential backoff retries for 503/429 network exceptions.
    """
    # Convert our custom dictionary format to Gemini API content format
    contents = []
    for msg in messages:
        if msg["role"] == "system":
            continue
        contents.append(msg["content"])
        
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=contents,
                config={
                    'system_instruction': SYSTEM_PROMPT,
                    'temperature': 0.0,
                }
            )
            return response.text
            
        except Exception as e:
            error_str = str(e)
            
            # Check if it is a temporary server issue (503/UNAVAILABLE) or a rate limit (429)
            if "503" in error_str or "429" in error_str or "UNAVAILABLE" in error_str:
                # Calculate backoff delay: 3 seconds, then 6 seconds, then 12 seconds
                sleep_time = initial_delay * (2 ** attempt)
                console.print(f"\n[bold yellow]⚠️ [API Warning]: Server busy or throttled. Retrying in {sleep_time}s... (Attempt {attempt + 1}/{max_retries})[/bold yellow]")
                time.sleep(sleep_time)
            else:
                # If it's a completely different error (credentials, bad syntax, etc.), crash immediately
                console.print(f"[bold red]API Execution Error:[/bold red] {e}")
                sys.exit(1)
                
    # If all retry attempts failed
    console.print("\n[bold red]❌ Critical Error: Exhausted all retries without a response from Gemini API.[/bold red]")
    sys.exit(1)

def parse_tool_call(response_text: str) -> tuple[str, str]:
    """Parses a string formatted as [TOOL]: tool_name | tool_input using regular expressions."""
    match = re.search(r'\[TOOL\]:\s*([^|]+)\|\s*(.*)', response_text)
    if match:
        tool_name = match.group(1).strip()
        tool_input = match.group(2).strip()
        return tool_name, tool_input
    return "unknown", "none"

from tools import TOOL_REGISTRY

def execute_tool(tool_name: str, tool_input: str) -> str:
    """
    Looks up a tool name in the registry and runs it with the provided input.
    Guarantees a text observation back even if the underlying function crashes.
    """
    tool_name = tool_name.lower().strip()
    
    if tool_name in TOOL_REGISTRY:
        try:
            # Wrap the actual function call in a local safety net
            return TOOL_REGISTRY[tool_name](tool_input)
        except Exception as e:
            return f"[OBSERVATION Error]: The tool '{tool_name}' encountered a runtime issue. Details: {e}"
    else:
        return f"[OBSERVATION Error]: Tool '{tool_name}' not found. Available tools are: {list(TOOL_REGISTRY.keys())}"
def run_agent(user_question: str, history: list = None, max_iterations: int = 8):
    """The master ReAct loop: Think -> Act -> Observe -> Repeat."""
    console.print(
        Panel(
            f"[bold green]User Question:[/bold green] {user_question}",
            title="[bold white]Agent Starting Session[/bold white]",
            border_style="green"
        )
    )
    
    if history is None:
        history = []

    # 1. Start with the system prompt instruction
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    # 2. Inject ALL previous clean conversational turns from the session
    for turn in history:
        messages.append(turn)
        
    # 3. Finally, append the brand-new question the user just typed
    messages.append({"role": "user", "content": user_question})
    
    for i in range(max_iterations):
        console.print(f"\n[bold yellow]--- 🔄 Iteration {i+1}/{max_iterations} ---[/bold yellow]")
        
        # 2. Add the pause here to protect your API quota
        console.print("[dim gray][SYSTEM]: Pausing for 2 seconds to protect API rate limits...[/dim gray]")
        time.sleep(2)

        # Step 1: Query the Brain
        response = call_llm(messages)
        logging.info(f"Iteration {i+1} - Model Output:\n{response}") # LOG THE AI OUTPUT
        console.print(Panel(response.strip(), title=f"🧠 Model Step {i+1} Output", border_style="yellow"))
        
        # Keep track of assistant's thoughts/actions in memory
        messages.append({"role": "assistant", "content": response})
        
        # Step 2: Analyze Output Tags
        if "[FINAL ANSWER]" in response:
            logging.info(f"Final Answer Reached: {response}") # LOG THE SUCCESS
            # We extracted our answer, the loop is finished!
            console.print("\n[bold green]🏁 Final Answer Arrived![/bold green]")
            return response
            
        elif "[TOOL]" in response:
            # Parse the target tool and argument
            tool_name, tool_input = parse_tool_call(response)
            logging.info(f"Executing Tool: {tool_name} | Input: {tool_input}") # LOG THE TOOL CALL
            
            # Step 3: Run local code and retrieve the payload
            tool_result = execute_tool(tool_name, tool_input)
            logging.info(f"Observation Received: {tool_result}") # LOG THE RESULT
            console.print(f"👁️ [bold magenta]Observation Received:[/bold magenta] {tool_result}")
            
            # Step 4: Inject the observation back into conversation memory for the next loop
            messages.append({"role": "user", "content": f"[OBSERVATION]: {tool_result}"})
            
        else:
            # The model is purely processing thought, or did not follow standard syntax.
            # We append a reminder to keep moving toward a final answer or tool action.
            messages.append({"role": "user", "content": "Please continue. Remember to use [TOOL] or [FINAL ANSWER] next."})
            
    console.print("\n[bold red]⚠️ Max iterations reached without finding a definitive answer.[/bold red]")
    return None
if __name__ == "__main__":
    # Test execution
    test_question = "What is the capital of France? Use wikipedia if you need to."
    run_agent(test_question)
