import sys
from datetime import datetime
from rich.console import Console
from agent import run_agent

console = Console()

def save_session_log(history: list):
    """Compiles the session memory and saves it to a timestamped file."""
    if not history:
        return
        
    # Generate timestamp matching the current session format
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"session_{timestamp}.txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== AGENT SESSION LOG: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
            for message in history:
                role = message["role"].upper()
                content = message["content"]
                f.write(f"[{role}]:\n{content}\n")
                f.write("-" * 40 + "\n")
        console.print(f"[bold green]💾 Session successfully logged to disk: {filename}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]⚠️ Failed to write session log: {e}[/bold red]")

def main():
    console.print("[bold purple]====================================================================[/bold purple]")
    console.print("[bold purple]                  🕵️‍♂️ WELCOME TO THE ReAct AGENT ENGINE              [/bold purple]")
    console.print("[bold purple]====================================================================[/bold purple]")
    console.print("Ask your agent any question. It will think, run tools, and find your answer.")
    console.print("Type [bold red]'exit'[/bold red] to close the agent session.\n")
    
    # Step A: Persistent memory array that lives through the whole session
    session_history = []
    while True:
        try:
            user_question = input("❓ Ask Agent: ").strip()
            if not user_question:
                continue
            if user_question.lower() == 'exit':
                console.print("[bold yellow]Shutting down agent session. Goodbye![/bold yellow]")
                save_session_log(session_history)
                break
            
            # Step B: Pass the session_history array as an argument
            final_response = run_agent(user_question, history=session_history)
            if final_response:
                session_history.append({"role": "user", "content": user_question})
                session_history.append({"role": "assistant", "content": final_response})

            console.print("\n" + "="*80 + "\n")
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Session cancelled. Goodbye![/bold yellow]")
            break

if __name__ == "__main__":
    main()