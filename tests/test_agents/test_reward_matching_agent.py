"""
Tests for the RewardMatchingAgent.
"""
import pytest
from typing import List, Dict, Any
from workspace.agents.reward_matching_agent import RewardMatchingAgent

def test_initialization():
    """Test that the agent initializes correctly."""
    agent = RewardMatchingAgent()
    assert agent is not None

def test_get_recommendations():
    """Test that recommendations are generated correctly."""
    agent = RewardMatchingAgent()
    recommendations = agent.get_recommendations("test_customer", limit=3)
    
    # Check recommendations structure
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 3
    
    # Check that each recommendation has the required fields
    for rec in recommendations:
        assert "customer_id" in rec
        assert "reward_id" in rec
        assert "reward_name" in rec
        assert "score" in rec
        assert "rationale" in rec
        
        # Check that customer_id matches input
        assert rec["customer_id"] == "test_customer"
        
        # Check that score is a float between 0 and 1
        assert isinstance(rec["score"], float)
        assert 0 <= rec["score"] <= 1

@pytest.mark.parametrize("limit", [1, 2, 5])
def test_recommendation_limits(limit):
    """Test that the limit parameter works correctly."""
    agent = RewardMatchingAgent()
    recommendations = agent.get_recommendations("test_customer", limit=limit)
    
    # Check that the number of recommendations does not exceed the limit
    assert len(recommendations) <= limit
