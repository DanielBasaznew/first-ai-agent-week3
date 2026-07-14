import sys
from rich.console import Console
from agent import run_agent

console = Console()

def main():
    console.print("[bold purple]====================================================================[/bold purple]")
    console.print("[bold purple]                  🕵️‍♂️ WELCOME TO THE ReAct AGENT ENGINE              [/bold purple]")
    console.print("[bold purple]====================================================================[/bold purple]")
    console.print("Ask your agent any question. It will think, run tools, and find your answer.")
    console.print("Type [bold red]'exit'[/bold red] to close the agent session.\n")

    while True:
        try:
            user_question = input("❓ Ask Agent: ").strip()
            if not user_question:
                continue
            if user_question.lower() == 'exit':
                console.print("[bold yellow]Shutting down agent session. Goodbye![/bold yellow]")
                break
            
            # Run the agent loop with the user's custom question
            run_agent(user_question)
            console.print("\n" + "="*80 + "\n")
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Session cancelled. Goodbye![/bold yellow]")
            break

if __name__ == "__main__":
    main()