-> python scripts/seed_data.py --output "./data/" for generation random data

Reward Personalization Agent: Project Workflow Guide
1. Project Overview: Where to Start
To understand the project workflow, start with these files in the following order:
First: Project Configuration & Entry Points

README.md - Overview of the project and its capabilities
.env.example - Environment variables needed for configuration
workspace/settings.py - Application settings and configuration options
workspace/app.py - Main entry point for the application

Second: Core Business Logic

workspace/workflows/ - These files orchestrate the business processes:

customer_onboarding.py - How new customers are processed
engagement_cycle.py - The ongoing customer engagement loop
analytics.py - How data is analyzed for insights



2. Understanding Component Relationships
Agent Architecture
The system is built around specialized AI agents, each handling different aspects:

workspace/agents/

reward_matching_agent.py - Matches customers with rewards
content_selection_agent.py - Selects optimal content mix
timing_optimization_agent.py - Determines best send times
engagement_analysis_agent.py - Analyzes behavior patterns



Data Pipeline

workspace/data/

schemas.py - Data models for the system
loaders.py - Loads data from storage
processors.py - Processes and transforms data



Models

workspace/models/

recommendation.py - Core recommendation logic
engagement_prediction.py - Predicts engagement likelihood
churn_prediction.py - Predicts customer churn probability
embeddings.py - Generates vector representations



External Services

workspace/services/

email_service.py - Handles email delivery
llm_service.py - Interfaces with Groq/LLM APIs
storage_service.py - Manages data persistence



3. API & Request Flow
API Structure

workspace/api/main.py - Defines the main API router
workspace/api/endpoints/ - Endpoint implementations

customers.py - Customer-related endpoints
rewards.py - Reward-related endpoints



Request Flow Example: Customer Reward Recommendation
When a request comes in for customer recommendations:

Request enters through app.py → FastAPI router
Router directs to api/endpoints/customers.py → get_recommended_rewards endpoint
Endpoint calls agents/reward_matching_agent.py → get_recommendations method
Agent uses:

data/loaders.py to fetch customer and reward data
models/recommendation.py to rank rewards for the customer


Results flow back through the same path to the client

Example Request/Response Flow:
CopyGET /api/customers/{customer_id}/recommended_rewards
Internally processes as:

api/endpoints/customers.py handles the request
Calls agents/reward_matching_agent.py for recommendations
Agent uses models/recommendation.py for scoring logic
Returns ranked recommendations to the endpoint
Endpoint formats and returns the API response

4. Key Workflows In Detail
New Customer Onboarding

workflows/customer_onboarding.py orchestrates the process
Calls agents/reward_matching_agent.py to get initial recommendations
Calls agents/content_selection_agent.py to create welcome content
Uses services/email_service.py to send welcome email
Schedules follow-up engagements

Engagement Cycle

workflows/engagement_cycle.py handles ongoing engagement
Uses agents/engagement_analysis_agent.py to analyze behavior
Calls agents/reward_matching_agent.py for updated recommendations
Uses agents/timing_optimization_agent.py for optimal send times
Sends personalized communications via services/email_service.py

5. PhiData Integration
The PhiData framework integration is defined in:

workspace/phi/workspace.py - Defines workspace configuration
workspace/phi/agents.py - Configures LLM-powered agents

6. Development & Testing Workflow

Start with docker-compose.yml to understand service dependencies
Use Makefile commands for common operations
Examine tests/ directory for how components are tested
Explore notebooks/ to see data analysis and prototype implementations

7. Example API Usage
Here's how you'd use the main APIs:
Recommend rewards for a customer:
pythonCopyresponse = requests.get(
    "http://localhost:8000/api/customers/cust001/recommended_rewards",
    params={"limit": 3}
)
Trigger an engagement for a customer:
pythonCopyresponse = requests.post(
    "http://localhost:8000/api/customers/cust001/engagement",
    json={
        "engagement_type": "email",
        "context": {"journey_stage": "onboarding"}
    }
)
Generate an analytics report:
pythonCopyresponse = requests.get(
    "http://localhost:8000/api/analytics/report",
    params={
        "start_date": "2023-05-01",
        "end_date": "2023-06-01"
    }
)