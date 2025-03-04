"""
PhiData workspace configuration.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional

from phidata.workspace import WorkspaceConfig
from phidata.app.llm import LLMApp
from phidata.task.script import ScriptTask
from phidata.app.fastapi import FastApiApp

# Set workspace directory
workspace_dir = Path(__file__).parent.parent.resolve()
data_dir = Path(workspace_dir).parent / "data"

# Define the workspace
workspace = WorkspaceConfig(
    # Workspace name used for naming cloud resources
    name="reward-personalization-agent",
    # Path to the workspace directory
    workspace_dir=workspace_dir,
)

# Define the FastAPI App
api_app = FastApiApp(
    name="api",
    app_dir=workspace_dir,
    module="app:app",
    port=8000,
)

# Define LLM App
llm_app = LLMApp(
    name="llm",
    # Required: LLM API key
    llm_api_key="${GROQ_API_KEY}",
    llm_provider="groq",
    llm_model="${LLM_MODEL}",
    # Define the knowledge base
    knowledge_base={
        # Storage dir for the knowledge base
        "storage_dir": data_dir / "knowledge_base",
    },
    # Define the workspace resources
    workspace_resources={
        # Tasks
        "tasks": [
            ScriptTask(
                name="seed-data",
                script_path=workspace_dir.parent / "scripts" / "seed_data.py",
            ),
        ],
        # Apps
        "apps": [api_app],
    },
)

# Add tools to the workspace
workspace.add_tools(
    [
        llm_app,
    ]
)
