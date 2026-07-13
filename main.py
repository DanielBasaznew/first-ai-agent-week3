# main.py
from agent import run_agent

def main():
    # We will ask a question that triggers our mock "Ethiopia" logic to test the loop
    question = "Can you look up the profile of Ethiopia and summarize its capital?"
    
    # Run the agent
    final_output = run_agent(question)
    
    print("\n================ FINAL AGENT OUTPUT ================")
    print(final_output)
    print("====================================================")

if __name__ == "__main__":
    main()