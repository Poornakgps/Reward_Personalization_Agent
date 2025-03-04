"""
Agent responsible for matching customers with the most appropriate rewards.
"""
from typing import List, Dict, Any
from workspace.utils.logger import setup_logger
from workspace.services.llm_service import LLMService
from workspace.models.recommendation import RewardRecommender

logger = setup_logger(__name__)

class RewardMatchingAgent:
    """Agent that determines the best rewards for a given customer."""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.recommender = RewardRecommender()
        logger.info("Reward Matching Agent initialized")
    
    def get_recommendations(self, customer_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get reward recommendations for a specific customer.
        
        Args:
            customer_id: The ID of the customer
            limit: Maximum number of recommendations to return
            
        Returns:
            List of recommended rewards with scores and rationale
        """
        logger.info(f"Generating reward recommendations for customer {customer_id}")
        
        # In a real implementation:
        # 1. Fetch customer data
        # 2. Fetch available rewards
        # 3. Use recommender model to rank rewards
        # 4. Use LLM to generate rationale for top recommendations
        
        # Mock implementation
        recommendations = [
            {
                "customer_id": customer_id,
                "reward_id": "reward1",
                "reward_name": "10% Discount",
                "score": 0.92,
                "rationale": "Based on customer demographics and past engagement with similar offers"
            },
            {
                "customer_id": customer_id,
                "reward_id": "reward2",
                "reward_name": "Free Shipping",
                "score": 0.85,
                "rationale": "Customer has abandoned cart multiple times, possibly due to shipping costs"
            }
        ]
        
        return recommendations[:limit]
        
    def train(self, historical_data: List[Dict[str, Any]]) -> None:
        """
        Train the recommendation model using historical data.
        
        Args:
            historical_data: List of customer-reward interactions with outcomes
        """
        logger.info(f"Training reward matching model with {len(historical_data)} records")
        self.recommender.train(historical_data)
