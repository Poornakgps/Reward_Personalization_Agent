#!/usr/bin/env python3
"""
Script to seed the database with initial data for development and testing.
"""
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
import argparse

def generate_customers(count: int) -> List[Dict[str, Any]]:
    """Generate sample customer data."""
    interests = ["fashion", "technology", "sports", "beauty", "home", "travel", "food", "entertainment"]
    locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio"]
    genders = ["male", "female", "non-binary", "prefer not to say"]
    
    customers = []
    for i in range(1, count + 1):
        customer_id = f"cust{i:04d}"
        customer = {
            "id": customer_id,
            "email": f"customer{i}@example.com",
            "name": f"Customer {i}",
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
            "attributes": {
                "age": random.randint(18, 80),
                "gender": random.choice(genders),
                "location": random.choice(locations),
                "interests": random.sample(interests, random.randint(1, 4))
            }
        }
        customers.append(customer)
    
    return customers

def generate_rewards(count: int) -> List[Dict[str, Any]]:
    """Generate sample reward data."""
    reward_types = ["discount", "voucher", "free_item", "loyalty_points", "gift_card"]
    
    rewards = []
    for i in range(1, count + 1):
        reward_id = f"reward{i:04d}"
        reward_type = random.choice(reward_types)
        
        if reward_type == "discount":
            value = random.choice([5, 10, 15, 20, 25, 30, 50])
            name = f"{value}% Discount"
            description = f"{value}% off your next purchase"
        elif reward_type == "voucher":
            value = random.choice([5, 10, 15, 20, 25, 50, 100])
            name = f"${value} Voucher"
            description = f"${value} off your next purchase"
        elif reward_type == "free_item":
            items = ["product", "shipping", "gift", "accessory"]
            item = random.choice(items)
            value = random.randint(5, 30)
            name = f"Free {item.title()}"
            description = f"Get a free {item} with your next purchase"
        elif reward_type == "loyalty_points":
            value = random.choice([50, 100, 200, 500, 1000])
            name = f"{value} Bonus Points"
            description = f"Earn {value} extra points on your next purchase"
        else:  # gift_card
            value = random.choice([10, 25, 50, 100])
            name = f"${value} Gift Card"
            description = f"${value} gift card for any purchase"
        
        reward = {
            "id": reward_id,
            "name": name,
            "description": description,
            "value": float(value),
            "type": reward_type,
            "conditions": {},
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 180))).isoformat()
        }
        
        # Add conditions to some rewards
        if random.random() < 0.3:
            reward["conditions"]["min_purchase"] = float(random.choice([25, 50, 75, 100]))
        
        rewards.append(reward)
    
    return rewards

def generate_engagement_events(customer_count: int, days: int) -> List[Dict[str, Any]]:
    """Generate sample engagement events."""
    event_types = ["email_open", "email_click", "reward_claim", "purchase", "profile_update"]
    campaigns = ["welcome_series", "loyalty_program", "promotional", "abandoned_cart", "re-engagement"]
    
    events = []
    for i in range(1, customer_count + 1):
        customer_id = f"cust{i:04d}"
        
        # Generate random number of events for this customer
        num_events = random.randint(0, days // 2)  # average one event every 2 days at most
        
        for j in range(num_events):
            event_type = random.choice(event_types)
            campaign = random.choice(campaigns)
            
            # Generate timestamp within the specified days
            days_ago = random.randint(0, days)
            timestamp = (datetime.now() - timedelta(days=days_ago)).isoformat()
            
            event = {
                "id": f"event{len(events) + 1:06d}",
                "customer_id": customer_id,
                "event_type": event_type,
                "timestamp": timestamp,
                "metadata": {
                    "campaign_id": campaign,
                    "source": "email" if event_type in ["email_open", "email_click"] else "app"
                }
            }
            
            # Add specific metadata based on event type
            if event_type == "email_click":
                event["metadata"]["link"] = random.choice(["product", "category", "reward", "profile"])
            elif event_type == "reward_claim":
                event["metadata"]["reward_id"] = f"reward{random.randint(1, 20):04d}"
            elif event_type == "purchase":
                event["metadata"]["amount"] = round(random.uniform(10, 200), 2)
                event["metadata"]["items"] = random.randint(1, 5)
            
            events.append(event)
    
    return events

def main():
    parser = argparse.ArgumentParser(description="Seed database with sample data")
    parser.add_argument("--customers", type=int, default=100, help="Number of customers to generate")
    parser.add_argument("--rewards", type=int, default=20, help="Number of rewards to generate")
    parser.add_argument("--days", type=int, default=90, help="Days of history to generate")
    parser.add_argument("--output", type=str, default="../data/", help="Output directory")
    args = parser.parse_args()
    
    # Generate data
    customers = generate_customers(args.customers)
    rewards = generate_rewards(args.rewards)
    events = generate_engagement_events(args.customers, args.days)
    
    # Write to files
    with open(f"{args.output}/customers.json", "w") as f:
        json.dump(customers, f, indent=2)
    
    with open(f"{args.output}/rewards.json", "w") as f:
        json.dump(rewards, f, indent=2)
    
    with open(f"{args.output}/events.json", "w") as f:
        json.dump(events, f, indent=2)
    
    print(f"Generated {len(customers)} customers, {len(rewards)} rewards, and {len(events)} events")
    print(f"Data written to {args.output}")

if __name__ == "__main__":
    main()
