"""
Model for predicting customer churn.
"""
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
from workspace.utils.logger import setup_logger

logger = setup_logger(__name__)

class ChurnPredictor:
    """Model for predicting customer churn probability."""
    
    def __init__(self):
        self.model_ready = False
        logger.info("ChurnPredictor initialized")
    
    def train(self, historical_data: List[Dict[str, Any]]) -> None:
        """
        Train the churn prediction model.
        
        Args:
            historical_data: List of customer engagement histories with churn outcomes
        """
        logger.info(f"Training churn prediction model with {len(historical_data)} records")
        
        # In a real implementation:
        # 1. Extract features from engagement histories
        # 2. Create target variable (churned or not)
        # 3. Train a classification model
        
        self.model_ready = True
        logger.info("Churn prediction model training completed")
    
    def predict_churn_probability(self, customer_id: str, 
                                 engagement_history: List[Dict[str, Any]]) -> float:
        """
        Predict the probability of a customer churning.
        
        Args:
            customer_id: The ID of the customer
            engagement_history: Customer's engagement history
            
        Returns:
            Probability of churn (0-1)
        """
        logger.info(f"Predicting churn probability for customer {customer_id}")
        
        # If no engagement history, use default risk
        if not engagement_history:
            return 0.5
        
        # Extract basic features from engagement history
        now = datetime.now()
        
        # Parse timestamps in engagement history
        events_with_dt = []
        for event in engagement_history:
            try:
                dt = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
                events_with_dt.append((event, dt))
            except (ValueError, KeyError):
                logger.warning(f"Invalid timestamp in event: {event}")
                continue
        
        if not events_with_dt:
            return 0.5
            
        # Get most recent event
        most_recent_event, most_recent_dt = max(events_with_dt, key=lambda x: x[1])
        days_since_last_engagement = (now - most_recent_dt).days
        
        # Calculate engagement frequency
        event_count = len(events_with_dt)
        oldest_event, oldest_dt = min(events_with_dt, key=lambda x: x[1])
        days_in_history = (most_recent_dt - oldest_dt).days + 1
        engagement_frequency = event_count / max(days_in_history, 1)
        
        # Calculate engagement types distribution
        event_types = {}
        for event, _ in events_with_dt:
            event_type = event.get("event_type", "unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        # Simple heuristic model
        # High risk factors: inactivity, low engagement frequency
        risk = 0.0
        
        # Risk from inactivity
        if days_since_last_engagement > 60:
            risk += 0.7
        elif days_since_last_engagement > 30:
            risk += 0.4
        elif days_since_last_engagement > 14:
            risk += 0.2
            
        # Risk from low engagement frequency
        if engagement_frequency < 0.05:  # Less than once per 20 days
            risk += 0.3
        elif engagement_frequency < 0.1:  # Less than once per 10 days
            risk += 0.15
            
        # Risk from limited engagement types
        if len(event_types) == 1:
            risk += 0.1
            
        # Reduce risk for high-value engagement
        if event_types.get("purchase", 0) > 0:
            risk -= 0.2
        if event_types.get("reward_claim", 0) > 0:
            risk -= 0.1
            
        # Ensure risk is between 0 and 1
        risk = max(0.0, min(0.99, risk))
        
        return risk
