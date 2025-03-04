"""
Main API router configuration.
"""
from fastapi import APIRouter
from workspace.api.endpoints import rewards, customers

router = APIRouter()

router.include_router(rewards.router, prefix="/rewards", tags=["Rewards"])
router.include_router(customers.router, prefix="/customers", tags=["Customers"])
