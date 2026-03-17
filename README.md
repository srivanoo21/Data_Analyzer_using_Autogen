# Analyzer_GPT_modular

This project implements a modular, agent-based system for automated data analysis, using OpenAI for reasoning and Docker for safe code execution.

## Project Structure & Key Scripts

- **main.py**: Orchestrates the workflow. Sets up the OpenAI model client, Docker executor, and agent team. Runs the data analysis task (e.g., generating a graph from iris.csv) using agent collaboration and Docker for safe code execution.
- **agents/**: Contains agent logic.
  - **Data_analyzer_agent.py**: Analyzes data, generates Python code to answer user questions, and collaborates with the Code Executor Agent.
  - **Code_executor_agent.py**: Executes Python code in Docker, handles errors/output, and returns results to the Data Analyzer Agent.
- **models/openai_model_client.py**: Sets up the OpenAI client for agent communication and code generation.
- **config/docker_util.py**: Manages Docker container lifecycle, providing functions to start/stop containers and create the Docker executor.
- **teams/analyzer_gpt.py**: Builds the agent team, combining Data Analyzer and Code Executor agents in a collaborative group chat with a termination condition.
- **iris.csv**: Example data file used for analysis tasks.
- **streamlit_app.py**: Web interface for interactive data analysis (optional).

## Workflow Overview

1. User provides a task (e.g., analyze iris.csv).
2. **main.py** orchestrates everything:
   - Calls **models/openai_model_client.py** to set up the OpenAI model client.
   - Calls **config/docker_util.py** to set up Docker for code execution.
   - Calls **teams/analyzer_gpt.py** to build the agent team.
3. **teams/analyzer_gpt.py** combines:
   - **agents/Data_analyzer_agent.py** (analyzes data, generates code)
   - **agents/Code_executor_agent.py** (executes code in Docker)
4. **Data_analyzer_agent.py** analyzes the data and generates Python code.
5. **Code_executor_agent.py** executes the code, handles errors/output.
6. Output is sent back to **Data_analyzer_agent.py** for final analysis and explanation.
7. The process uses **iris.csv** as the data source.
8. The flow ends when the STOP condition is met and the task is complete.

## Project Flow (ASCII Diagram)

```
User Input/Task
      |
   main.py
      |
  +-----------------------------+
  |                             |
models/openai_model_client.py    |
config/docker_util.py            |
teams/analyzer_gpt.py            |
      |                         |
  +-----------------------------+
      |
  agents/Data_analyzer_agent.py
      |
  agents/Code_executor_agent.py
      |
  Docker Execution
      |
  Output/Error Handling
      |
  Data_analyzer_agent.py (Final Analysis)
      |
  Task Complete (STOP)
```

---

This README provides a clear overview of the folder structure, script functions, and the full workflow for the Analyzer_GPT_modular project.