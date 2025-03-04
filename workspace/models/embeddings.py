"""
Models for generating and using embeddings for customers and rewards.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from workspace.utils.logger import setup_logger

logger = setup_logger(__name__)

class EmbeddingModel:
    """Model for generating embeddings for customers and rewards."""
    
    def __init__(self, embedding_dim: int = 32):
        self.embedding_dim = embedding_dim
        self.customer_embeddings = {}
        self.reward_embeddings = {}
        logger.info(f"EmbeddingModel initialized with dimension {embedding_dim}")
    
    def generate_customer_embedding(self, customer_data: Dict[str, Any]) -> np.ndarray:
        """
        Generate an embedding vector for a customer.
        
        Args:
            customer_data: Customer attributes and history
            
        Returns:
            Embedding vector for the customer
        """
        customer_id = customer_data.get("id", "unknown")
        logger.info(f"Generating embedding for customer {customer_id}")
        
        # In a real implementation:
        # 1. Extract features from customer data
        # 2. Use a pre-trained embedding model or neural network
        
        # Mock implementation - generate random embedding
        embedding = np.random.normal(0, 1, self.embedding_dim)
        embedding = embedding / np.linalg.norm(embedding)  # Normalize
        
        # Cache the embedding
        self.customer_embeddings[customer_id] = embedding
        
        return embedding
    
    def generate_reward_embedding(self, reward_data: Dict[str, Any]) -> np.ndarray:
        """
        Generate an embedding vector for a reward.
        
        Args:
            reward_data: Reward attributes
            
        Returns:
            Embedding vector for the reward
        """
        reward_id = reward_data.get("id", "unknown")
        logger.info(f"Generating embedding for reward {reward_id}")
        
        # In a real implementation:
        # 1. Extract features from reward data
        # 2. Use a pre-trained embedding model or neural network
        
        # Mock implementation - generate random embedding
        embedding = np.random.normal(0, 1, self.embedding_dim)
        embedding = embedding / np.linalg.norm(embedding)  # Normalize
        
        # Cache the embedding
        self.reward_embeddings[reward_id] = embedding
        
        return embedding
    
    def get_customer_embedding(self, customer_id: str, 
                              customer_data: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Get the embedding for a customer, generating it if needed.
        
        Args:
            customer_id: ID of the customer
            customer_data: Optional customer data if embedding needs to be generated
            
        Returns:
            Embedding vector for the customer
        """
        if customer_id in self.customer_embeddings:
            return self.customer_embeddings[customer_id]
            
        if customer_data is None:
            raise ValueError(f"No embedding found for customer {customer_id} and no data provided to generate one")
            
        return self.generate_customer_embedding(customer_data)
    
    def get_reward_embedding(self, reward_id: str, 
                            reward_data: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Get the embedding for a reward, generating it if needed.
        
        Args:
            reward_id: ID of the reward
            reward_data: Optional reward data if embedding needs to be generated
            
        Returns:
            Embedding vector for the reward
        """
        if reward_id in self.reward_embeddings:
            return self.reward_embeddings[reward_id]
            
        if reward_data is None:
            raise ValueError(f"No embedding found for reward {reward_id} and no data provided to generate one")
            
        return self.generate_reward_embedding(reward_data)
    
    def calculate_similarity(self, embedding1: np.ndarray, 
                            embedding2: np.ndarray) -> float:
        """
        Calculate the cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1)
        """
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return (dot_product / (norm1 * norm2) + 1) / 2  # Scale from [-1, 1] to [0, 1]
