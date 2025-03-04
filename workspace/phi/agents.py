"""
PhiData agent configuration.
"""
from phidata.app.agent import AgentApp
from phidata.app.assistant import Assistant
from phidata.app.llm import LLMApp
from phidata.agent.tools import KnowledgeBaseTool
import os

# Import the LLM App
from workspace.phi.workspace import llm_app, workspace_dir, data_dir
from workspace.settings import settings

# Get the LLM model from settings or environment variable
llm_model = os.getenv("LLM_MODEL", settings.LLM_MODEL)

# Create the KnowledgeBase tool
kb_tool = KnowledgeBaseTool(
    name="reward_kb",
    description="Knowledge base with information about rewards and campaigns",
    llm_app=llm_app,
)

# Define the Reward Agent Assistant
reward_agent = Assistant(
    name="reward_matching_agent",
    llm=llm_model,  # Use the configured Groq model
    system_prompt="""You are a Reward Matching Agent that helps match customers with the most appropriate rewards.
    
    Your goal is to:
    1. Analyze customer attributes, preferences, and behavior
    2. Determine which rewards are most likely to resonate with each customer
    3. Provide rationale for your recommendations
    
    Follow these guidelines:
    - Consider customer demographics, past engagement, and purchase history
    - Account for the value and conditions of each reward
    - Prioritize rewards that align with customer interests and past behavior
    - Be transparent about the factors influencing your recommendations
    """,
    tools=[kb_tool],
)

# Define the Content Selection Agent Assistant
content_agent = Assistant(
    name="content_selection_agent",
    llm=llm_model,  # Use the configured Groq model
    system_prompt="""You are a Content Selection Agent that determines the optimal content mix for customer communications.
    
    Your goal is to:
    1. Analyze customer profile and engagement history
    2. Select the optimal mix of content types (questions, games, vouchers, newsletters)
    3. Personalize content based on customer preferences and journey stage
    
    Follow these guidelines:
    - Balance content types based on customer engagement patterns
    - Consider journey stage (onboarding, engaged, at-risk) when selecting content
    - Personalize content to match customer interests and demographic factors
    - Optimize for both short-term engagement and long-term relationship building
    """,
    tools=[kb_tool],
)

# Create the Agent App
agent_app = AgentApp(
    name="reward_personalization_agents",
    assistants=[
        reward_agent,
        content_agent,
    ],
)