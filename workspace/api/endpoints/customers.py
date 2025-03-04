"""
Customers API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from workspace.data.schemas import Customer, CustomerCreate
from workspace.agents.reward_matching_agent import RewardMatchingAgent
from workspace.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

class CustomerResponse(BaseModel):
    id: str
    email: str
    name: str
    
    class Config:
        from_attributes = True  # Updated from orm_mode
    
class RecommendedRewardResponse(BaseModel):
    customer_id: str
    reward_id: str
    reward_name: str
    score: float
    rationale: str
    
    class Config:
        from_attributes = True  # Updated from orm_mode

@router.get("/", response_model=List[CustomerResponse])
async def get_customers(skip: int = 0, limit: int = 100):
    """Get all customers."""
    logger.info(f"Fetching customers with params: skip={skip}, limit={limit}")
    # Implementation would retrieve customers from database
    return []

@router.get("/{customer_id}/recommended_rewards", response_model=List[RecommendedRewardResponse])
async def get_recommended_rewards(customer_id: str, limit: int = 5):
    """Get recommended rewards for a specific customer."""
    logger.info(f"Getting recommended rewards for customer {customer_id}")
    
    # Use the reward matching agent to get recommendations
    # In a real implementation, this would be properly instantiated and managed
    agent = RewardMatchingAgent()
    recommendations = agent.get_recommendations(customer_id, limit)
    
    return recommendations