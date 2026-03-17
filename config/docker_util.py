# -------------------------------------------------------------
# docker_util.py
#
# This file provides utility functions for managing Docker containers
# used for code execution in the agent system. It includes:
# - Creating a DockerCommandLineCodeExecutor for running Python code safely
# - Starting and stopping Docker containers for isolated code execution
# -------------------------------------------------------------

from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

from config.constants import WORK_DIR_DOCKER, TIMEOUT_DOCKER

# Factory function to create and return a DockerCommandLineCodeExecutor instance
# Uses the 'amancevice/pandas' image and workspace settings
# The getDockerCommandLineExecutor function creates a Docker executor using the 'amancevice/pandas' image, which comes with Python, pandas, and other data science libraries pre-installed. This allows the code to run in a safe, ready-to-use environment for data analysis tasks.

def getDockerCommandLineExecutor():
    docker=DockerCommandLineCodeExecutor(
        # Docker image used for code execution; 'amancevice/pandas' provides Python with pandas and other data science libraries pre-installed
        image='amancevice/pandas',
        work_dir=WORK_DIR_DOCKER,
        timeout=TIMEOUT_DOCKER
    )
    return docker

# Async function to start the Docker container for code execution
# Prints status messages for visibility
async def start_docker_container(docker):
    print("Starting Docker Container")
    await docker.start()
    print("Docker Container Started")

# Async function to stop the Docker container after execution
# Prints status messages for visibility
async def stop_docker_container(docker):
    print("Stopping Docker Container")
    await docker.stop()
    print("Docker Container Stopped")