"""
Data processing utilities.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from workspace.utils.logger import setup_logger

logger = setup_logger(__name__)

class CustomerDataProcessor:
    """
    Process and transform customer data for analysis and modeling.
    """
    
    def __init__(self):
        logger.info("CustomerDataProcessor initialized")
    
    def extract_features(self, customer_data: Dict[str, Any], 
                        engagement_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract features from customer data and engagement history.
        
        Args:
            customer_data: Raw customer data
            engagement_history: List of engagement events
            
        Returns:
            Dictionary of extracted features
        """
        logger.info(f"Extracting features for customer {customer_data.get('id', 'unknown')}")
        
        features = {}
        
        # Basic customer attributes
        features["customer_id"] = customer_data.get("id", "unknown")
        
        # Extract demographic features
        attributes = customer_data.get("attributes", {})
        features["age"] = attributes.get("age", 0)
        features["gender"] = attributes.get("gender", "unknown")
        features["location"] = attributes.get("location", "unknown")
        features["interest_count"] = len(attributes.get("interests", []))
        
        # Calculate days since signup
        created_at = customer_data.get("created_at", datetime.now().isoformat())
        try:
            signup_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            features["days_since_signup"] = (datetime.now() - signup_date).days
        except (ValueError, TypeError):
            features["days_since_signup"] = 0
        
        # Process engagement history
        if engagement_history:
            # Count events by type
            event_types = {}
            for event in engagement_history:
                event_type = event.get("event_type", "unknown")
                event_types[event_type] = event_types.get(event_type, 0) + 1
                
            features["total_events"] = len(engagement_history)
            for event_type, count in event_types.items():
                features[f"{event_type}_count"] = count
                
            # Calculate engagement rate
            if "email_open_count" in features and "email_click_count" in features:
                opens = features.get("email_open_count", 0)
                clicks = features.get("email_click_count", 0)
                if opens > 0:
                    features["click_to_open_rate"] = clicks / opens
                else:
                    features["click_to_open_rate"] = 0.0
            
            # Calculate recency (days since last engagement)
            try:
                timestamps = [datetime.fromisoformat(event.get("timestamp", "").replace("Z", "+00:00")) 
                             for event in engagement_history 
                             if "timestamp" in event]
                
                if timestamps:
                    latest_timestamp = max(timestamps)
                    features["days_since_last_engagement"] = (datetime.now() - latest_timestamp).days
                else:
                    features["days_since_last_engagement"] = features["days_since_signup"]
            except (ValueError, TypeError):
                features["days_since_last_engagement"] = features["days_since_signup"]
        else:
            # No engagement history
            features["total_events"] = 0
            features["days_since_last_engagement"] = features["days_since_signup"]
            
        return features
    
    def segment_customer(self, features: Dict[str, Any]) -> str:
        """
        Assign a segment to a customer based on extracted features.
        
        Args:
            features: Extracted customer features
            
        Returns:
            Segment name
        """
        logger.info(f"Segmenting customer {features.get('customer_id', 'unknown')}")
        
        # Simple rule-based segmentation
        
        # VIP segment: High engagement, frequent purchases
        if (features.get("total_events", 0) > 20 and 
            features.get("purchase_count", 0) > 3 and
            features.get("days_since_last_engagement", 999) < 7):
            return "VIP"
            
        # Active segment: Regular engagement
        if (features.get("total_events", 0) > 10 and 
            features.get("days_since_last_engagement", 999) < 14):
            return "Active"
            
        # Recent segment: New customers with some engagement
        if (features.get("days_since_signup", 0) < 30 and 
            features.get("total_events", 0) > 0):
            return "Recent"
            
        # At Risk segment: Declining engagement
        if (features.get("days_since_last_engagement", 0) > 30 and 
            features.get("total_events", 0) > 5):
            return "At Risk"
            
        # Standard segment: Default
        return "Standard"
    
    def normalize_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize numerical features for machine learning models.
        
        Args:
            features: Raw features
            
        Returns:
            Normalized features
        """
        logger.info(f"Normalizing features for customer {features.get('customer_id', 'unknown')}")
        
        normalized = features.copy()
        
        # Normalization values (these would come from training data in a real implementation)
        # Here using simple heuristics
        normalization_params = {
            "age": {"mean": 35, "std": 12},
            "days_since_signup": {"mean": 180, "std": 90},
            "total_events": {"mean": 15, "std": 10},
            "days_since_last_engagement": {"mean": 14, "std": 10}
        }
        
        # Apply z-score normalization
        for feature, params in normalization_params.items():
            if feature in normalized and isinstance(normalized[feature], (int, float)):
                normalized[f"{feature}_normalized"] = (normalized[feature] - params["mean"]) / params["std"]
                
        return normalized

class RewardDataProcessor:
    """
    Process and transform reward data for analysis and matching.
    """
    
    def __init__(self):
        logger.info("RewardDataProcessor initialized")
    
    def extract_features(self, reward_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract features from reward data.
        
        Args:
            reward_data: Raw reward data
            
        Returns:
            Dictionary of extracted features
        """
        logger.info(f"Extracting features for reward {reward_data.get('id', 'unknown')}")
        
        features = {}
        
        # Basic reward attributes
        features["reward_id"] = reward_data.get("id", "unknown")
        features["reward_type"] = reward_data.get("type", "unknown")
        features["value"] = float(reward_data.get("value", 0))
        
        # Extract conditions
        conditions = reward_data.get("conditions", {})
        features["has_min_purchase"] = "min_purchase" in conditions
        if features["has_min_purchase"]:
            features["min_purchase_value"] = float(conditions["min_purchase"])
        else:
            features["min_purchase_value"] = 0.0
        
        # Calculate reward appeal score (simplified)
        appeal_score = features["value"]
        if features["has_min_purchase"]:
            # Discount appeal score for rewards with conditions
            appeal_score = appeal_score * 0.8
            
        features["appeal_score"] = appeal_score
        
        return features
    
    def calculate_relevance_score(self, reward_features: Dict[str, Any], 
                                 customer_features: Dict[str, Any]) -> float:
        """
        Calculate relevance score between a reward and a customer.
        
        Args:
            reward_features: Extracted reward features
            customer_features: Extracted customer features
            
        Returns:
            Relevance score from 0 to 1
        """
        logger.info(f"Calculating relevance score between reward {reward_features.get('reward_id', 'unknown')} "
                  f"and customer {customer_features.get('customer_id', 'unknown')}")
        
        # Base score
        score = 0.5
        
        # Reward type preferences by segment
        segment = customer_features.get("segment", "Standard")
        reward_type = reward_features.get("reward_type", "unknown")
        
        # Segment-based adjustments
        segment_preferences = {
            "VIP": {"discount": 0.7, "gift_card": 0.9, "free_item": 0.8, "loyalty_points": 0.9},
            "Active": {"discount": 0.8, "gift_card": 0.7, "free_item": 0.8, "loyalty_points": 0.9},
            "Recent": {"discount": 0.9, "gift_card": 0.7, "free_item": 0.8, "loyalty_points": 0.6},
            "At Risk": {"discount": 0.9, "gift_card": 0.8, "free_item": 0.9, "loyalty_points": 0.5},
            "Standard": {"discount": 0.8, "gift_card": 0.7, "free_item": 0.7, "loyalty_points": 0.7}
        }
        
        # Apply segment preference
        if segment in segment_preferences and reward_type in segment_preferences[segment]:
            segment_factor = segment_preferences[segment][reward_type]
            score = score * segment_factor
            
        # Consider minimum purchase requirement
        if reward_features.get("has_min_purchase", False):
            min_purchase = reward_features.get("min_purchase_value", 0)
            
            # Adjust score based on purchase history (if available)
            avg_purchase = customer_features.get("average_purchase_value", 0)
            if avg_purchase > 0:
                if avg_purchase >= min_purchase * 1.5:
                    # Customer typically spends more than required
                    score = score * 1.2
                elif avg_purchase < min_purchase:
                    # Customer typically spends less than required
                    score = score * 0.7
            else:
                # No purchase history, slightly discount rewards with minimums
                score = score * 0.9
                
        # Consider recency
        days_since_engagement = customer_features.get("days_since_last_engagement", 0)
        if days_since_engagement > 30:
            # For disengaged customers, higher value rewards are more appealing
            value_factor = min(1.0, reward_features.get("value", 0) / 50.0)
            score = score * (1.0 + value_factor * 0.3)
            
        # Ensure score is between 0 and 1
        score = max(0.0, min(1.0, score))
        
        return score
