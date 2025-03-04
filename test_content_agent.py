from workspace.agents.content_selection_agent import ContentSelectionAgent

# Create the agent
agent = ContentSelectionAgent()

# Test with sample data
customer_id = "test_customer"
context = {
    "profile_completion": 0.7,
    "engagement_rate": 0.5,
    "days_since_last_purchase": 15
}

# Get content plan
content_plan = agent.select_content(customer_id, context)

# Print the results
print(f"Content plan for {customer_id}:")
print(f"Include questions: {content_plan['include_questions']}")
print(f"Include game: {content_plan['include_game']}")
print(f"Include voucher: {content_plan['include_voucher']}")
print(f"Recommended game: {content_plan['recommended_game']}")
print(f"Newsletter focus: {content_plan['newsletter_focus']}")
