# -------------------------------------------------------------
# analyzer_gpt.py
#
# This file defines the team setup for the Data Analyzer workflow.
# It creates a RoundRobinGroupChat with a DataAnalyzerAgent and a CodeExecutorAgent,
# and sets up a termination condition for the conversation.
# -------------------------------------------------------------

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.Code_executor_agent import getCodeExecutorAgent
from agents.Data_analyzer_agent import getDataAnalyzerAgent

# Factory function to create and return the Data Analyzer Team
# Combines the DataAnalyzerAgent and CodeExecutorAgent in a group chat
# Sets a termination condition ('STOP') and a maximum number of turns

def getDataAnalyzerTeam(docker, model_client):
    code_executor_agent = getCodeExecutorAgent(docker)
    data_analyzer_agent = getDataAnalyzerAgent(model_client)

    text_mention_termination = TextMentionTermination('STOP')

    team = RoundRobinGroupChat(
        participants=[data_analyzer_agent, code_executor_agent],
        max_turns=10,
        termination_condition=text_mention_termination
    )

    return team