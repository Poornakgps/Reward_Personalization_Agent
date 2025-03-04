from workspace.data.loaders import CustomerDataLoader, RewardDataLoader

# Create loaders
customer_loader = CustomerDataLoader()
reward_loader = RewardDataLoader()

# Test loading a customer
customer_id = "cust001"
customer_data = customer_loader.load_customer(customer_id)
print(f"Customer data for {customer_id}:")
print(customer_data)

# Test loading customer engagement
engagement_data = customer_loader.load_customer_engagement(customer_id)
print(f"\nEngagement history for {customer_id}:")
print(f"Found {len(engagement_data)} engagement events")

# Test loading rewards
rewards = reward_loader.load_rewards()
print(f"\nLoaded {len(rewards)} rewards")
print("First reward:", rewards[0] if rewards else "None")
