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