"""
Tests for the RewardRecommender model.
"""
import pytest
from typing import List, Dict, Any
import numpy as np
from workspace.models.recommendation import RewardRecommender

def test_initialization():
    """Test that the model initializes correctly."""
    model = RewardRecommender()
    assert model is not None
    assert model.model_ready is False

def test_train():
    """Test that training works."""
    model = RewardRecommender()
    
    # Sample training data
    historical_data = [
        {"customer_id": "cust1", "reward_id": "reward1", "outcome": "claimed", "score": 0.8},
        {"customer_id": "cust1", "reward_id": "reward2", "outcome": "ignored", "score": 0.2},
        {"customer_id": "cust2", "reward_id": "reward1", "outcome": "ignored", "score": 0.3},
        {"customer_id": "cust2", "reward_id": "reward2", "outcome": "claimed", "score": 0.9}
    ]
    
    # Train the model
    model.train(historical_data)
    
    # Check that the model is marked as ready
    assert model.model_ready is True

def test_recommend():
    """Test that recommendations are generated correctly."""
    model = RewardRecommender()
    
    # Sample customer and rewards
    customer_data = {
        "id": "cust1",
        "name": "Test Customer",
        "attributes": {"age": 35, "gender": "female"}
    }
    
    available_rewards = [
        {"id": "reward1", "name": "10% Discount", "type": "discount", "value": 10},
        {"id": "reward2", "name": "Free Shipping", "type": "shipping", "value": 5}
    ]
    
    # Get recommendations without training (should use rule-based fallback)
    recommendations = model.recommend(customer_data, available_rewards, top_n=2)
    
    # Check that recommendations are returned
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 2
    
    # Check recommendation structure
    for rec in recommendations:
        assert "reward_id" in rec
        assert "reward_name" in rec
        assert "score" in rec
        assert "rank" in rec
        
        # Check that score is a float between 0 and 1
        assert isinstance(rec["score"], float)
        assert 0 <= rec["score"] <= 1
        
        # Check that rank starts at 1
        assert rec["rank"] >= 1

def test_rule_based_recommend():
    """Test that rule-based recommendations work correctly."""
    model = RewardRecommender()
    
    # Sample customer and rewards
    customer_data = {
        "id": "cust1",
        "name": "Test Customer",
        "attributes": {"age": 35, "gender": "female"}
    }
    
    available_rewards = [
        {"id": "reward1", "name": "10% Discount", "type": "discount", "value": 10},
        {"id": "reward2", "name": "Free Shipping", "type": "shipping", "value": 5},
        {"id": "reward3", "name": "Signup Bonus", "type": "bonus", "value": 20}
    ]
    
    # Call rule-based recommendation directly
    recommendations = model._rule_based_recommend(customer_data, available_rewards, top_n=3)
    
    # Check that recommendations are returned and sorted
    assert isinstance(recommendations, list)
    assert len(recommendations) == 3
    assert recommendations[0]["score"] >= recommendations[1]["score"]
    assert recommendations[1]["score"] >= recommendations[2]["score"]
    
    # Check that ranks are assigned correctly
    assert recommendations[0]["rank"] == 1
    assert recommendations[1]["rank"] == 2
    assert recommendations[2]["rank"] == 3
