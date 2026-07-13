# agent.py
import re
from google import genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()

# Initialize the Gemini Client securely using the modern Google GenAI SDK
# It automatically picks up the GEMINI_API_KEY environment variable.
client = genai.Client()

def call_llm(messages: list) -> str:
    """
    Sends the entire message history to Gemini 2.5 Flash and returns the text response.
    """
    # Format our flat chat history dicts into the modern SDK's contents list structure
    contents = []
    for msg in messages:
        contents.append({
            "role": msg["role"],
            "parts": [{"text": msg["content"]}]
        })
        
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents
        )
        return response.text.strip()
    except Exception as e:
         return f"[ERROR]: API call failed. Details: {str(e)}"

def parse_tool_call(response_text: str):
    """
    Looks for the [TOOL]: tool_name | tool_input pattern using Regex.
    Returns (tool_name, tool_input).
    """
    # Regex search to safely parse our bracketed notation
    match = re.search(r"\[TOOL\]:\s*([^|]+)\|\s*(.*)", response_text)
    if match:
        tool_name = match.group(1).strip()
        tool_input = match.group(2).strip()
        return tool_name, tool_input
    return None, None

def execute_tool(tool_name: str, tool_input: str) -> str:
    """
    A temporary mock executor. Tomorrow we will hook up real API tools!
    """
    print(f"\n⚙️  [SYSTEM EXECUTING]: Running tool '{tool_name}' with input '{tool_input}'...")
    
    # Simple mock behaviors to test the loop's reaction
    if "ethiopia" in tool_input.lower():
        return "Ethiopia is located in the Horn of Africa. Its capital city is Addis Ababa."
    return f"Mock output for {tool_name} using input '{tool_input}'"

def run_agent(user_question: str, max_iterations: int = 5):
    """
    The heart of our framework. It drives the ReAct loop:
    Reason -> Act -> Observe -> Reason.
    """
    # Keep track of the entire conversation state
    messages = [
        {"role": "user", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]
    
    print(f"\n🚀 Starting Agent Loop for query: '{user_question}'")
    
    for i in range(1, max_iterations + 1):
        print(f"\n--- 🔄 Iteration {i}/{max_iterations} ---")
        
        # 1. Ask the cognitive controller (Gemini) what to do next
        response = call_llm(messages)
        print(f"🤖 [MODEL RESPONSE]:\n{response}")
        
        # Save the assistant's response to maintain conversation history context
        messages.append({"role": "user", "content": f"[ASSISTANT RESPONSE]: {response}"})
        
        # 2. Parse the response: Did it give a final answer, or run a tool?
        if "[FINAL ANSWER]" in response:
            print("\n🎉 Agent arrived at the final answer!")
            return response
            
        elif "[TOOL]" in response:
            tool_name, tool_input = parse_tool_call(response)
            
            if tool_name and tool_input:
                # 3. Execute the tool locally in Python
                tool_result = execute_tool(tool_name, tool_input)
                
                # 4. Feed the observation back to the LLM
                observation_msg = f"[OBSERVATION]: {tool_result}"
                print(f"👁️  [OBSERVATION SENT TO LLM]: {observation_msg}")
                messages.append({"role": "user", "content": observation_msg})
            else:
                # If parsing failed, alert the model to try again
                error_msg = "[SYSTEM ERROR]: Could not parse tool call format. Make sure to output exactly '[TOOL]: tool_name | tool_input'"
                print(f"⚠️ {error_msg}")
                messages.append({"role": "user", "content": error_msg})
                
        else:
            # The model is just writing thoughts or didn't follow formatting rules
            print("📝 Model is thinking or didn't trigger a tool. Continuing...")
            
    return "❌ Max iterations reached without a final answer."