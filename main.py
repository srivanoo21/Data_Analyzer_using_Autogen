# -------------------------------------------------------------
# main.py
#
# This file orchestrates the Data Analyzer workflow.
# It sets up the OpenAI model client, Docker executor, and agent team,
# then runs a data analysis task (e.g., generating a graph from iris.csv)
# using agent collaboration and Docker for safe code execution.
# -------------------------------------------------------------

import asyncio
from teams.analyzer_gpt import getDataAnalyzerTeam
from models.openai_model_client import get_model_client
from config.docker_util import getDockerCommandLineExecutor, start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage

# Main async function to run the workflow
# Sets up model client, Docker executor, agent team, and executes the task
async def main():
    openai_model_client = get_model_client()
    docker = getDockerCommandLineExecutor()
    team = getDataAnalyzerTeam(docker, openai_model_client)

    try:
        # Example task: ask for a graph of flower types in iris.csv
        task = 'Can you give me a graph of types of flowers in my data iris.csv'
        await start_docker_container(docker)
        async for message in team.run_stream(task=task):
            print(message)
    except Exception as e:
        print(e)
    finally:
        await stop_docker_container(docker)

# Entry point for script execution
if(__name__=='__main__'):
    asyncio.run(main())
