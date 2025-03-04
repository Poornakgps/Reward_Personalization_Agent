"""
Pydantic models for data schemas.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class RewardType(str, Enum):
    DISCOUNT = "discount"
    VOUCHER = "voucher"
    FREE_ITEM = "free_item"
    LOYALTY_POINTS = "loyalty_points"
    GIFT_CARD = "gift_card"
    OTHER = "other"

class ContentType(str, Enum):
    QUESTION = "question"
    GAME = "game"
    VOUCHER = "voucher"
    NEWSLETTER = "newsletter"
    SURVEY = "survey"

# Reward Models
class RewardBase(BaseModel):
    name: str
    description: str
    value: float
    type: RewardType
    conditions: Optional[Dict[str, Any]] = None
    expiry_days: Optional[int] = None

class RewardCreate(RewardBase):
    pass

class RewardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    type: Optional[RewardType] = None
    conditions: Optional[Dict[str, Any]] = None
    expiry_days: Optional[int] = None

class Reward(RewardBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Customer Models
class CustomerBase(BaseModel):
    email: EmailStr
    name: str
    
class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: str
    created_at: datetime
    attributes: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True

# Engagement Models
class EngagementEvent(BaseModel):
    customer_id: str
    event_type: str
    timestamp: datetime
    metadata: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True

# Campaign Models
class Campaign(BaseModel):
    id: str
    name: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    rewards: List[str]  # List of reward IDs
    rules: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True
