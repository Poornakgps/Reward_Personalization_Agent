from workspace.agents.reward_matching_agent import RewardMatchingAgent

# Create the agent
agent = RewardMatchingAgent()

# Test with a sample customer ID
customer_id = "test_customer"
recommendations = agent.get_recommendations(customer_id, limit=3)

# Print the results
print(f"Recommendations for {customer_id}:")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec['reward_name']} (score: {rec['score']})")
    print(f"   Rationale: {rec['rationale']}")
