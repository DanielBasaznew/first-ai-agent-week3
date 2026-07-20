# Custom ReAct AI Agent from Scratch (Week 3)

A lightweight, robust AI Agent engine built completely from scratch in Python following the **ReAct (Reasoning and Acting)** framework pattern. This implementation operates entirely without external orchestration frameworks (like LangChain or CrewAI), exposing the underlying token processing, loop dynamics, and tool routing architecture explicitly.

## 🧠 Architectural Overview

The agent executes an iterative loop processing cycle: **User Query ➔ Thought ➔ Action/Tool Execution ➔ Observation ➔ Reflection**. 

+-------------------------------------------------------+
|                      User Input                       |
+-------------------------------------------------------+
|
v
+------------------------------+
+----------->|   [THOUGHT] Reasoning Loop   |<-----------+
|            +------------------------------+            |
|                           |                            |
|                           v                            |
|             +----------------------------+             |
|             |  [TOOL] Selection & Call   |             |
|             +----------------------------+             |
|                           |                            |
|                           v                            |
|            +------------------------------+            |
|            | [OBSERVATION] Tool Execution |            |
|            +------------------------------+            |
|                           |                            |
+---------------------------+                            |
|
v
+-------------------------------+
| [FINAL ANSWER] Output Formatter|
+-------------------------------+


### ⚙️ Hardened Defensive Guards
To transition from a conceptual pipeline into a stable application, the engine implements several deterministic engineering wrappers:
* **Max Iterations Emergency Guard:** Enforces a rigid iteration threshold loop break to intercept infinite conversational reasoning traps, returning an explicit string diagnostic instead of crashing the system history tracker.
* **Global Registry Router & Safety Net:** Intercepts hallucinated tool strings dynamically by validating requests against an explicit dictionary dispatch matrix, automatically retrying flaky network operations.
* **Strict Context Window Truncation:** Intercepts out-of-bounds tokens by cropping downstream search outputs to target thresholds, defending the LLM context attention threshold.
* **Network & Empty Input Sanitizers:** Enforces runtime timeouts across asynchronous I/O sockets and filters whitespace values before making network requests.

## 🛠️ Built-in Tool Ecosystem

1. **`calculator`**: Evaluates string-based mathematical formulations. Optimized for compound equation mapping.
2. **`get_date`**: Translates relative descriptive string queries into target timestamps.
3. **`wikipedia`**: Fetches clean, historical contexts from the Wikipedia summary endpoint.
4. **`search_web`**: Connects via DuckDuckGo text scraping to grab real-time live info.
5. **`get_weather`**: Fetches structured weather payloads instantly from `wttr.in`.

## 🚀 Installation & Execution

### 1. Set Up the Environment
Clone the repository, create a virtual environment, and install dependencies:
```bash
python -m venv .venv
source .venv/Scripts/activate # On Windows MINGW/Bash
pip install requests wikipedia-api duckduckgo-search rich python-dotenv
2. Configure Environment Variables
Create a .env file in the root directory and supply your model parameters:

Code snippet
GEMINI_API_KEY=your_api_key_here
3. Start the Agent Loop
Bash
python week3-agent/main.py

``` 
# 📊 Live Verification Session Run

DELL@Daniel-Basaznew MINGW64 ~/Documents/Code/first-ai-agent-week3 (main)
$ c:/Users/DELL/Documents/Code/first-ai-agent-week3/.venv/Scripts/python.exe c:/Users/DELL/Documents/Code/first-ai-agent-week3/week3-agent/main.py
====================================================================
                 🕵️‍♂️ WELCOME TO THE ReAct AGENT ENGINE              
====================================================================
Ask your agent any question. It will think, run tools, and find your answer.
Type 'exit' to close the agent session.

❓ Ask Agent: Find out when the 2022 FIFA World Cup winner was founded as a football association, calculate how many years ago that was, and tell me today's date.
╭─────────────────────────────────────────────────────────────────── Agent Starting Session ────────────────────────────────────────────────────────────────────╮
│ User Question: Find out when the 2022 FIFA World Cup winner was founded as a football association, calculate how many years ago that was, and tell me today's date. │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

--- 🔄 Iteration 1/8 ---
[SYSTEM]: Pausing for 2 seconds to protect API rate limits...
╭─────────────────────────────────────────────────────────────────── 🧠 Model Step 1 Output ────────────────────────────────────────────────────────────────────╮
│ [THOUGHT]: The user wants to know three specific pieces of information that require separate steps:                            │
│ 1. Find the winner of the 2022 FIFA World Cup and look up when their football association was founded.                        │
│ 2. Calculate how many years ago that founding date was from the current year (2026).                                          │
│ 3. Retrieve today's date using the systemic calendar tools.                                                                    │
│ I will begin by searching for the winner of the 2022 FIFA World Cup to verify the nation.                                     │
│                                                                                                                               │
│ [TOOL]: search_web | "winner of 2022 FIFA World Cup"                                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
👁️ Observation Received: 1. Title: 2022 FIFA World Cup - Wikipedia
   Snippet: The 2022 FIFA World Cup was an international football tournament won by Argentina, who defeated France on penalties in the final.
   URL: https://en.wikipedia.org/wiki/2022_FIFA_World_Cup

--- 🔄 Iteration 2/8 ---
[SYSTEM]: Pausing for 2 seconds to protect API rate limits...
╭─────────────────────────────────────────────────────────────────── 🧠 Model Step 2 Output ────────────────────────────────────────────────────────────────────╮
│ [THOUGHT]: The 2022 FIFA World Cup winner is Argentina. Now I need to figure out when the Argentine Football Association       │
│ (AFA) was officially founded. I will look this up on Wikipedia.                                                               │
│                                                                                                                               │
│ [TOOL]: wikipedia | "Argentine Football Association"                                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
👁️ Observation Received: The Argentine Football Association (Spanish: Asociación del Fútbol Argentino, AFA) is the governing body of football in Argentina. Based in Buenos Aires, it was founded on 21 February 1893, making it the oldest football association in South America...

--- 🔄 Iteration 3/8 ---
[SYSTEM]: Pausing for 2 seconds to protect API rate limits...
╭─────────────────────────────────────────────────────────────────── 🧠 Model Step 3 Output ────────────────────────────────────────────────────────────────────╮
│ [THOUGHT]: The Argentine Football Association was founded in 1893. The current year is 2026. I will use the calculator tool  │
│ to compute exactly how many years ago that was (2026 - 1893).                                                                 │
│                                                                                                                               │
│ [TOOL]: calculator | 2026 - 1893                                                                                              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
👁️ Observation Received: 133

--- 🔄 Iteration 4/8 ---
[SYSTEM]: Pausing for 2 seconds to protect API rate limits...
╭─────────────────────────────────────────────────────────────────── 🧠 Model Step 4 Output ────────────────────────────────────────────────────────────────────╮
│ [THOUGHT]: The calculation shows it was 133 years ago. Now, the final requirement is to check the exact calendar text for    │
│ today's full date tracking.                                                                                                   │
│                                                                                                                               │
│ [TOOL]: get_date | "today"                                                                                                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
👁️ Observation Received: 2026-07-20

--- 🔄 Iteration 5/8 ---
[SYSTEM]: Pausing for 2 seconds to protect API rate limits...
╭─────────────────────────────────────────────────────────────────── 🧠 Model Step 5 Output ────────────────────────────────────────────────────────────────────╮
│ [FINAL ANSWER]: The winner of the 2022 FIFA World Cup was Argentina. The Argentine Football Association (AFA) was founded on │
│ February 21, 1893, which was exactly 133 years ago relative to the current year 2026. Today's date is July 20, 2026.           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🏁 Final Answer Arrived!

================================================================================

❓ Ask Agent: exit
Shutting down agent session. Goodbye!
💾 Session successfully logged to disk: session_2026-07-20_23-35.txt
(.venv) 
DELL@Daniel-Basaznew MINGW64 ~/Documents/Code/first-ai-agent-week3 (main)

``` 
```
# 💡 Engineering Insights
Building a ReAct loop from the ground up proves that an agent's capability isn't derived from complex third-party abstraction layers, but from clear systemic execution criteria inside a system prompt. By strictly regulating how the agent splits its thinking phases from its tool usage phases, a standard LLM can be organized into a reliable automated system capable of handling complex internet workflows safely.