# -------------------------------------------------------------
# openai_model_client.py
#
# This file sets up the OpenAI model client for use in the agent system.
# It provides a factory function to create an OpenAIChatCompletionClient
# using the specified model and API key from environment variables.
# -------------------------------------------------------------

from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constants import MODEL_OPENAI
import os
from dotenv import load_dotenv

# Optionally load environment variables from a .env file
load_dotenv()

# Factory function to create and return an OpenAI model client
# Uses the model name and API key from environment variables

def get_model_client():
    openai_model_client = OpenAIChatCompletionClient(
        model=MODEL_OPENAI,
        api_key=os.getenv('OPENAI_API_KEY')
    )
    return openai_model_client