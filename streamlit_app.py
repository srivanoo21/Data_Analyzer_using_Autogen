# -------------------------------------------------------------
# streamlit_app.py
#
# This script provides a Streamlit web interface for the Analyzer GPT system.
# Users can upload a CSV file, enter a data analysis task, and interact with agents
# that analyze the data and generate results using OpenAI and Docker.
# -------------------------------------------------------------

import streamlit as st
import asyncio
import os

from teams.analyzer_gpt import getDataAnalyzerTeam
from models.openai_model_client import get_model_client
from config.docker_util import getDockerCommandLineExecutor, start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

# Set Streamlit app title
st.title('Analyser GPT- Digital Data Analyzer') 

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Initialize Streamlit session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None
if('images_shown') not in st.session_state:
    st.session_state.images_shown=[]

# Input box for user task
task = st.chat_input("Enter your task here...")

# Async function to run the Analyzer GPT workflow
# Starts Docker, loads agent team, streams messages, and handles output/errors
async def run_analyser_gpt(docker, openai_model_client, task):
    try:
        await start_docker_container(docker)
        team = getDataAnalyzerTeam(docker, openai_model_client)

        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)

        async for message in team.run_stream(task=task):
            # Display messages from different agents in Streamlit chat
            if isinstance(message, TextMessage):
                if message.source.startswith('user'):
                    with st.chat_message('user', avatar='👤'):
                        st.markdown(message.content)
                elif message.source.startswith('Data_Analyzer_agent'):
                    with st.chat_message('Data Analyzer', avatar='🤖'):
                        st.markdown(message.content)
                elif message.source.startswith('Python_Code_Executor'):
                    with st.chat_message('Data Analyzer', avatar='👨‍💻'):
                        st.markdown(message.content)
                st.session_state.messages.append(message.content)
            elif isinstance(message, TaskResult):
                st.markdown(f'Stop Reason :{message.stop_reason}')
                st.session_state.messages.append(message.stop_reason)

        st.session_state.autogen_team_state = await team.save_state()
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return e
    finally:   
        await stop_docker_container(docker)

# Dummy async function for demonstration
async def do_something_big():
    await asyncio.sleep(1)  # Simulate a long-running task

# Display previous messages in Streamlit
if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(msg)

# Main logic: handle file upload and task input
if task:
   if uploaded_file is not None: 
        # Ensure temp directory exists
        if not os.path.exists('temp'):
            os.makedirs('temp', exist_ok=True)
        # Save uploaded CSV file
        with open('temp/data.csv', 'wb') as f:
            f.write(uploaded_file.getbuffer())
        # Set up model client and Docker executor
        openai_model_client = get_model_client()
        docker = getDockerCommandLineExecutor()
        # Run the Analyzer GPT workflow
        error = asyncio.run(run_analyser_gpt(docker, openai_model_client, task))
        if error:
            st.error(f'An error occured: {error}')
        # Display output image if generated
        if os.path.exists('temp/output.png'):
            st.image('temp/output.png')
   else:
       st.warning('Please upload the file and provide the task')
else:
    st.warning('Please provide the task') 