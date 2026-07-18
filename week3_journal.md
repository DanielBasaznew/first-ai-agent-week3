Week 3 Learning Journal: Building My First AI Agent

This journal tracks my daily breakthroughs, code designs, and reflections as I build a custom, framework-free ReAct Agent in Python.

# 📅 Day 1 Reflection: The ReAct Loop Skeleton

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

# 📅 Day 2 Reflection: 📓 Agentic AI Developer


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

# 📅 Day 3 Reflection: Wikipedia tool intergration to my Agent

## What I Built Today
Wikipedia Search Tool: Built a custom tool using the wikipedia-api library. Configured a strict 500-character truncation limit to protect the LLM's context window, and implemented a custom User-Agent string to safely comply with Wikimedia's policies.

Rich Terminal Formatting: Integrated the Rich library to color-code each stage of the agent loop (Yellow for [THOUGHT], Blue for [TOOL], Green for [OBSERVATION], and Bold White for the [FINAL ANSWER]).

Multi-Step Problem Solving: Tested the agent on complex queries requiring logical reasoning, like identifying the current Prime Minister of the UK amidst real-time leadership transitions in 2026.

## Challenges Faced & Solutions
The Truncation/Loop Trap:

Problem: The agent got stuck in a repetitive loop when Wikipedia observations were truncated right before the key answer was visible.

Solution: Upgraded the system prompt with strict rules forbidding consecutive identical searches, and increased the agent loop's max_iterations from 5 to 8 to give it breathing room for deeper paths.

API Limits & 503 Overloads:

Problem: Encountered 503 UNAVAILABLE and rate limit errors during active loop testing.

Solution:

Implemented a production-grade exponential backoff retry loop directly inside call_llm using a Python try/except block.

Enforced a mandatory 2-second sleep delay between iteration steps to respect API limits.

Swapped out rate-limited key environments to a fully functional, high-demand stable model setup using gemini-3.5-flash.

# 📅 Day 4 Reflection: Web Search Integration & Fault-Tolerant Tool Registries

#### What I Built & Solved
*   **Integrated Multi-Source Intelligence**: Successfully built a live `search_web` tool using the `duckduckgo-search` library, transitioning the agent from a static encyclopedic environment to real-time information retrieval.
*   **Centralized Tool Routing & Registry**: Standardized the initialization pattern inside `tools/__init__.py`. Created an explicit mapping via `TOOL_REGISTRY` and wrapped executions within a robust `execute_tool` entry point.
*   **Transient Failure Recovery**: Implemented a loops-based retry pattern (`max_retries = 2`) embedded directly within the tool executor. The system now transparently absorbs network hiccups or API rate limit spikes by executing a 1-second backoff pause before re-trying the operation.
*   **Error-to-Information Loop (Graceful Degradation)**: Configured system boundaries so that unmapped tool names or script crashes do not trigger raw Python stack-trace terminations. Instead, they are captured dynamically, sanitized into an `[OBSERVATION Error]` string, and routed back to the LLM context for real-time path adjustments.

#### Real-World Discovery
Testing the system on complex, time-dependent historical queries (like tracing the exact presidential term timeline for Ethiopia) revealed how vital hybrid search architectures are. The model cleanly gathered historical frameworks using Wikipedia, identified a data gap regarding the exact modern transition date, immediately engaged `search_web` to retrieve news-scraping snippets from diverse URLs, and synthesized the data points into a single timeline. This shows that the true power of an engineering agent doesn't lie in flawless execution, but in its ability to navigate through structural formatting or data boundaries without crashing the running environment.

# 📅 Day 5 Reflection: Conversational Memory Engines & Session Persistence
What I Built & Solved
Stateful Memory Architecture: Upgraded the agent from a stateless "one-shot" script to a conversational agent capable of maintaining context across sequential turns. This allows the system to accurately resolve anaphoras (like "he", "those", or "that") by preserving context.

Decoupled History Tracing: Implemented a persistent history schema outside the core execution runtime. The run_agent loop now accepts a running list of prior clean exchanges (User Questions and Final Answers) and injects them seamlessly before processing new user inputs.

Dual-Layer Telemetry Loggers: Built a post-session disk-writing mechanism triggered upon user exit (exit/quit). The script serializes the execution footprint into a structured .txt file, using a timestamped naming convention (session_YYYY-MM-DD_HH-MM.txt) to preserve records for auditing.

Context Window Efficiency: Opted for a "Clean Exchange" history structure (storing only final question-answer pairs rather than raw intermediate steps, thought traces, and massive raw tool observations). This choice keeps the core system instructions closer to the LLM's active focus area.

Zero-Dependency Meteorological Core: Built and registered an isolated get_weather tool module utilizing synchronous requests parsing of structured JSON data from wttr.in. This setup allows real-time local reporting without requiring paid third-party token keys.

Real-World Discovery
Testing the conversational loop with chained queries (e.g., tracking a subject, analyzing their companies, and filtering by valuation metrics) demonstrated the tension between contextual depth and context window saturation. While preserving every internal thought and raw tool snippet gives the agent maximum context, it exponentially increases token consumption and degrades performance due to the "lost-in-the-middle" effect. Managing state in production requires clear trade-offs: storing clean high-level responses keeps things lean, but building a rolling sliding window or using LLM-driven history summarization is essential for keeping multi-turn agents stable over long sessions.