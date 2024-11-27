# LLM-tutor

The goal of this project is to develop a generic tutor that can help guide and walk users through problems. On our first look at this problem, we first wanted to make it strictly an algorithmic problem solver, so that when given problems similar to the those on websites like LeetCode, this tutor would help the user solve them by providing hints. However, after looking at additional libraries, we wanted to expand the definition of this tutor to work for not just algorithm based problems, and instead be a generic tutor. To achieve this goal, we hope to use the Autogen library to help us dynamically create tutors. 

# Current stage
Right now, we are working on creating benchmarks for each of the agents, so that we can ensure that the models are performing as intended. 


# Dynamic Programming Tutor with AutoGen

## Project Overview
An intelligent tutoring system that dynamically creates specialized agents to help users solve programming problems. The system analyzes queries, creates appropriate tutoring agents, and enhances solutions using a hybrid approach of core programming patterns and online search.

---

## Architecture

### Core Components

#### Query Analyzer Agent
- Analyzes user input.
- Determines problem complexity and domain.
- Extracts key concepts.
- Provides structured analysis for the tutor.

#### Tutor Agent (Main Orchestrator)
- Makes decisions based on query analysis.
- Creates specialized agents for complex problems.
- Uses a general solver for simple problems.
- Manages solution flow.
- Handles user interaction.

#### Problem Solver
- Dynamically created for complex problems.
- General solver for simple problems.
- Provides initial solution approaches.

#### Solution Enhancer (Hybrid Approach)
- Core RAG for fundamental patterns.
- Online search integration for specific details.
- Combines both for comprehensive improvement.

#### Gradio UI
- Problem input interface.
- Code editor.
- Interactive chat.
- Solution display.

---

## Project Structure

```tree
tutoring_system/
├── agents/
│   ├── query_analyzer.py
│   ├── tutor_agent.py
│   ├── problem_solver.py
│   └── solution_enhancer.py
├── core_knowledge/
│   ├── patterns.json
│   ├── best_practices.json
│   └── optimization_techniques.json
├── ui/
│   ├── app.py
│   └── components.py
├── utils/
│   ├── code_executor.py
│   └── search_integration.py
├── evaluation/
│   ├── test_cases.py
│   └── metrics.py
└── main.py
```
