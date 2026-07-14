import os
import sys
import re
from google import genai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from prompts import SYSTEM_PROMPT

load_dotenv()
console = Console()

try:
    client = genai.Client()
except Exception as e:
    console.print(f"[bold red]Initialization Error:[/bold red] Make sure GEMINI_API_KEY is set in your .env. Details: {e}")
    sys.exit(1)

def call_llm(messages: list) -> str:
    """Helper function to call Gemini 2.5 Flash with our running conversation history."""
    try:
        # Convert our custom dictionary format to Gemini API content format
        contents = []
        for msg in messages:
            # We map system instruction to the system config, but send conversation history in contents
            if msg["role"] == "system":
                continue
            contents.append(msg["content"])
            
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config={
                'system_instruction': SYSTEM_PROMPT,
                'temperature': 0.0, # Lower temperature for stable reasoning and strict tag-following
            }
        )
        return response.text
    except Exception as e:
        console.print(f"[bold red]API Generation Error:[/bold red] {e}")
        sys.exit(1)

def parse_tool_call(response_text: str) -> tuple[str, str]:
    """Parses a string formatted as [TOOL]: tool_name | tool_input using regular expressions."""
    match = re.search(r'\[TOOL\]:\s*([^|]+)\|\s*(.*)', response_text)
    if match:
        tool_name = match.group(1).strip()
        tool_input = match.group(2).strip()
        return tool_name, tool_input
    return "unknown", "none"

def execute_mock_tool(tool_name: str, tool_input: str) -> str:
    """A safe placeholder tool to verify our loop's observational intake."""
    console.print(f"🔧 [bold cyan]Executing Tool [{tool_name}] with input: '{tool_input}'[/bold cyan]...")
    # Simulated responses based on typical testing scenarios
    if "wikipedia" in tool_name.lower():
        return f"Mock Wikipedia content for '{tool_input}': Paris is the capital of France, known for the Eiffel Tower."
    return f"Mock response: The tool '{tool_name}' ran successfully with input '{tool_input}'."

def run_agent(user_question: str, max_iterations: int = 5):
    """The master ReAct loop: Think -> Act -> Observe -> Repeat."""
    console.print(Panel(f"[bold green]User Question:[/bold green] {user_question}", title="[bold white]Agent Starting Session[/bold white]", border_style="green"))
    
    # Initialize the session history with the core layout
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]
    
    for i in range(max_iterations):
        console.print(f"\n[bold yellow]--- 🔄 Iteration {i+1}/{max_iterations} ---[/bold yellow]")
        
        # Step 1: Query the Brain
        response = call_llm(messages)
        console.print(Panel(response.strip(), title=f"🧠 Model Step {i+1} Output", border_style="yellow"))
        
        # Keep track of assistant's thoughts/actions in memory
        messages.append({"role": "assistant", "content": response})
        
        # Step 2: Analyze Output Tags
        if "[FINAL ANSWER]" in response:
            # We extracted our answer, the loop is finished!
            console.print("\n[bold green]🏁 Final Answer Arrived![/bold green]")
            return
            
        elif "[TOOL]" in response:
            # Parse the target tool and argument
            tool_name, tool_input = parse_tool_call(response)
            
            # Step 3: Run local code and retrieve the payload
            tool_result = execute_mock_tool(tool_name, tool_input)
            console.print(f"👁️ [bold magenta]Observation Received:[/bold magenta] {tool_result}")
            
            # Step 4: Inject the observation back into conversation memory for the next loop
            messages.append({"role": "user", "content": f"[OBSERVATION]: {tool_result}"})
            
        else:
            # The model is purely processing thought, or did not follow standard syntax.
            # We append a reminder to keep moving toward a final answer or tool action.
            messages.append({"role": "user", "content": "Please continue. Remember to use [TOOL] or [FINAL ANSWER] next."})
            
    console.print("\n[bold red]⚠️ Max iterations reached without finding a definitive answer.[/bold red]")

if __name__ == "__main__":
    # Test execution
    test_question = "What is the capital of France? Use wikipedia if you need to."
    run_agent(test_question)
