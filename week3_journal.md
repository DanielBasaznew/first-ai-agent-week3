Week 3 Learning Journal: Building My First AI Agent

This journal tracks my daily breakthroughs, code designs, and reflections as I build a custom, framework-free ReAct Agent in Python.

📅 Day 1 Reflection: The ReAct Loop Skeleton

1. The ReAct Architecture

Here is how my agent's decision-making loop processes information:

    +-----------------------------------------+
    |              User Question              |
    +-----------------------------------------+
                         |
                         v
    +-----------------------------------------+
    |               [THOUGHT]                 | <---------+
    |  "What do I know? What do I need?"      |           |
    +-----------------------------------------+           |
                         |                                |
                         | (Decides next move)            |
                         v                                |
         /---------------\                                |
        /  Is the answer  \                               |
       <   known?          >                              |
        \                 /                               |
         \---------------/                                |
           /           \                                  |
    (Yes) /             \ (No: Needs Data)                |
         v               v                                |
+---------------+  +--------------------------+           |
| [FINAL ANSWER]|  |         [TOOL]           |           |
| (Halts Loop)  |  |  (Invocates API call)    |           |
+---------------+  +--------------------------+           |
                         |                                |
                         v                                |
                   +------------+                         |
                   | [OBSERVE]  | ------------------------+
                   | (API Data) |  (Injects data to memory)
                   +------------+


2. What happens if a tool fails?

If a tool fails in a basic implementation (e.g., the Wikipedia API returns an HTTP 500 error or the internet drops):

The Crash Scenario: The Python code executing the tool will throw an unhandled exception (error), causing our whole terminal program to crash immediately.

The Production Fix: To make our agent resilient, we must wrap every tool execution in a try/except block. If a tool fails, instead of letting Python crash, we catch the error and pass it back to the agent as a regular [OBSERVATION] (e.g., [OBSERVATION]: Error: Service temporarily offline. Please try another way.). This allows the agent to analyze the failure, think of a backup plan (like trying a different search tool), and keep running safely.

📅 Day 2 Reflection: 📓 Agentic AI Developer


## 🚀 Today's Milestone: Bringing the ReAct Loop to Life
Today was a massive milestone. I moved from yesterday's mock skeleton to building and orchestrating my very first multi-file, production-grade ReAct (Reasoning and Acting) Agent completely from scratch. Seeing the agent coordinate multiple real Python tools in real-time was the moment agentic engineering truly clicked for me.

### 🛠️ What I Built & Solved Today
1. **Secure AST Calculator Tool (`tools/calculator.py`):** 
   - Avoided the security vulnerabilities of raw `eval()` by writing a tree-walking interpreter using Python's Abstract Syntax Tree (`ast`). 
   - Handled Python 3.14+ deprecations by removing outdated references to `ast.Num` in favor of `ast.Constant`.
   - Embedded robust `try/except` safeguards to gracefully return math syntax and division-by-zero errors back to the model as text rather than crashing the Python environment.
2. **Context-Aware Date Tool (`tools/date_tool.py`):**
   - Integrated `python-dateutil` to calculate dynamic temporal queries like "90 days from today" and "12 weeks ago".
   - **Crucial Bug Fix:** Debugged a parser flaw where the word "today" in offset queries (e.g., "90 days from today") caused the tool to truncate early and return the current date. Reconfigured the parsing logic to check for numeric offsets before falling back to the default current date.
3. **Dynamic Tool Registry (`tools/__init__.py`):**
   - Created a central dictionary mapping string requests directly to executable functions.
4. **Environment Isolation & Virtualization (`.venv`):**
   - Successfully transitioned the project into a clean, isolated virtual environment, resolving dependency resolution issues for packages like `rich`, `python-dotenv`, and `google-genai`.

---

### 🧠 Architectural Observations & Reflections

#### 1. Multi-Step Orchestration Performance
When tested with the question, *"What is the current time, and what do you get if you multiply the current hour by 5?"*, the agent demonstrated true orchestration capabilities:
* **Iteration 1:** It called `get_date | now` and observed: `Thursday, July 16, 2026 (Current Time: 12:59 PM)`.
* **Iteration 2:** It successfully parsed the hour `12` out of the observation, formulated a math string, called `calculator | 12 * 5`, and received `60`.
* **Iteration 3:** It consolidated the raw data points into a perfect, natural-language explanation.

#### 2. The Power of Structured Tagging & System Instructions
The system instructions inside `prompts.py` acted as a solid behavioral contract. Because the agent was forced to reason before execution, it systematically decomposed the problem instead of blindly guessing.

#### 3. Why Agents Need Strict System Tool Constraints
While modern LLMs like `gemini-2.5-flash` are highly intelligent, they are notoriously poor at mental arithmetic. When left to calculate without a tool, they rely on token pattern-matching, which often results in subtle, incorrect calculations. 
* *Engineering Insight:* To build reliable production agents, we must enforce rigid prompt instructions that restrict the model from performing calculations internally and force it to yield to safe, sandboxed sandboxes like our AST calculator.