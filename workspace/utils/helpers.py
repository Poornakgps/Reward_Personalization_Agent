"""
Miscellaneous helper functions.
"""
import json
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from workspace.utils.logger import setup_logger

logger = setup_logger(__name__)

def generate_id(prefix: str, data: Dict[str, Any]) -> str:
    """
    Generate a deterministic ID based on a prefix and data.
    
    Args:
        prefix: Prefix for the ID
        data: Data to use for generating the ID
        
    Returns:
        Generated ID string
    """
    data_str = json.dumps(data, sort_keys=True)
    hash_obj = hashlib.md5(data_str.encode())
    return f"{prefix}_{hash_obj.hexdigest()[:10]}"

def calculate_next_engagement_date(base_date: datetime, 
                                 frequency_days: int, 
                                 optimal_hour: int = 10) -> datetime:
    """
    Calculate the next engagement date based on frequency and optimal hour.
    
    Args:
        base_date: Base date to calculate from
        frequency_days: Number of days between engagements
        optimal_hour: Optimal hour of the day for engagement
        
    Returns:
        Next engagement datetime
    """
    next_date = base_date + timedelta(days=frequency_days)
    return next_date.replace(hour=optimal_hour, minute=0, second=0, microsecond=0)

def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    if currency == "USD":
        return f"${amount:.2f}"
    elif currency == "EUR":
        return f"€{amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"

def segment_customer(engagement_score: float, 
                   purchase_recency: int, 
                   purchase_frequency: int, 
                   purchase_value: float) -> str:
    """
    Segment a customer based on engagement and purchasing behavior.
    
    Args:
        engagement_score: Score from 0-1 representing engagement level
        purchase_recency: Days since last purchase
        purchase_frequency: Number of purchases in last 90 days
        purchase_value: Average purchase value
        
    Returns:
        Customer segment label
    """
    # RFM (Recency, Frequency, Monetary) inspired segmentation
    if engagement_score > 0.7 and purchase_frequency > 5 and purchase_value > 100:
        return "VIP"
    elif engagement_score > 0.5 and purchase_frequency > 2:
        return "Active"
    elif purchase_recency < 30:
        return "Recent"
    elif purchase_recency > 90 and engagement_score < 0.2:
        return "At Risk"
    else:
        return "Standard"
