Reward Personalization Agent
An AI-powered system for personalizing customer rewards and optimizing engagement using PhiData.
Overview
This project implements an intelligent agent system that matches customers with the most relevant incentives and creates dynamic, personalized engagement journeys. The system optimizes reward matching, content selection, timing, and frequency based on customer behavior and preferences.
Features

Reward Matching: Intelligently pairs customers with the most appealing incentives
Dynamic Engagement: Generates personalized email content including questions, games, vouchers, and newsletters
Timing Optimization: Determines the optimal send times and frequency for each customer
Engagement Analysis: Monitors customer behavior and adapts strategies accordingly
Segmentation: Automatically segments customers based on behavior and engagement patterns

Architecture
The system is built around specialized AI agents orchestrated through PhiData:

Reward Matching Agent: Determines optimal rewards for each customer
Content Selection Agent: Selects ideal content mix for communications
Timing Optimization Agent: Optimizes delivery timing and frequency
Engagement Analysis Agent: Analyzes behavior and predicts churn risk

Quick Start
bashCopy# Setup and dependencies
make setup

# Generate sample data
make seed-data

# Start the API server
make start

# Using PhiData
make phi-init
make phi-start
Installation
bashCopy# Clone the repository
git clone https://github.com/yourusername/reward-personalization-agent.git
cd reward-personalization-agent

# Set up environment and install dependencies
make setup

# Generate sample data
make seed-data
Configuration
Copy .env.example to .env and configure environment variables:
bashCopycp .env.example .env
# Edit .env with your API keys and configuration
Usage Examples
Recommend rewards for a customer
pythonCopyimport requests

response = requests.get(
    "http://localhost:8000/api/customers/cust001/recommended_rewards",
    params={"limit": 3}
)
recommendations = response.json()
Trigger a personalized engagement
pythonCopyimport requests

response = requests.post(
    "http://localhost:8000/api/customers/cust001/engagement",
    json={
        "engagement_type": "email",
        "context": {"journey_stage": "onboarding"}
    }
)
result = response.json()
Generate analytics report
pythonCopyimport requests

response = requests.get(
    "http://localhost:8000/api/analytics/report",
    params={
        "start_date": "2023-05-01",
        "end_date": "2023-06-01"
    }
)
analytics = response.json()
API Endpoints
Customers

GET /api/customers - List all customers
GET /api/customers/{customer_id} - Get customer details
GET /api/customers/{customer_id}/recommended_rewards - Get personalized reward recommendations
POST /api/customers/{customer_id}/engagement - Trigger engagement workflow for customer
GET /api/customers/{customer_id}/engagement_history - Get customer engagement history

Rewards

GET /api/rewards - List all rewards
POST /api/rewards - Create a new reward
GET /api/rewards/{reward_id} - Get reward details
PUT /api/rewards/{reward_id} - Update a reward
DELETE /api/rewards/{reward_id} - Delete a reward

Analytics

GET /api/analytics/report - Generate analytics report
GET /api/analytics/optimization - Get optimization opportunities
GET /api/analytics/segments - Get customer segment distribution
GET /api/analytics/rewards/performance - Get reward performance metrics

Directory Structure
Copyreward_personalization_agent/
├── workspace/             # Main application code
│   ├── agents/            # AI agent implementations
│   ├── api/               # FastAPI endpoints
│   ├── data/              # Data handling and schemas
│   ├── models/            # ML model implementations
│   ├── services/          # External service integrations
│   ├── utils/             # Utility functions
│   ├── workflows/         # Business process orchestration
│   └── phi/               # PhiData configuration
├── notebooks/             # Jupyter notebooks for exploration
├── tests/                 # Unit and integration tests
├── scripts/               # Utility scripts
└── data/                  # Data storage
Development
bashCopy# Run tests
make test

# Format code
make format

# Lint code
make lint

# Deploy
make deploy
Environment Variables

OPENAI_API_KEY - API key for LLM service
DATABASE_URL - Connection string for database
PORT - Port to run the API server (default: 8000)
DEBUG - Enable debug mode (default: false)
LLM_MODEL - LLM model to use (default: llama3-70b)
EMAIL_API_KEY - API key for email service

Contributing

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request