"""
Service for interacting with LLM models using Groq.
"""
import os
import json
import httpx
from typing import Dict, Any, List, Optional
from workspace.utils.logger import setup_logger
from workspace.settings import settings

logger = setup_logger(__name__)

class LLMService:
    """Service for interacting with LLM models using Groq API."""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model = settings.LLM_MODEL
        self.provider = "groq"
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        logger.info(f"LLMService initialized with model: {self.model} provider: {self.provider}")
    
    async def generate_response(self, prompt: str, 
                              max_tokens: int = 500) -> str:
        """
        Generate a response from the LLM using Groq API.
        
        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text response
        """
        logger.info(f"Generating LLM response with {len(prompt)} chars prompt")
        
        # Check if API key is available
        if not self.api_key:
            logger.warning("No Groq API key found. Using mock response.")
            return f"This is a mock response from the LLM service using {self.model}"
        
        try:
            # Prepare request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            # Make request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
            
            # Process response
            if response.status_code == 200:
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"]
            else:
                logger.error(f"Error from Groq API: {response.status_code}, {response.text}")
                return f"Error generating response: {response.status_code}"
                
        except Exception as e:
            logger.exception(f"Exception when calling Groq API: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    async def generate_personalized_content(self, 
                                         customer_data: Dict[str, Any], 
                                         content_type: str, 
                                         context: Dict[str, Any]) -> str:
        """
        Generate personalized content for a customer.
        
        Args:
            customer_data: Customer attributes and history
            content_type: Type of content to generate (email, question, etc.)
            context: Additional context for generation
            
        Returns:
            Generated personalized content
        """
        logger.info(f"Generating personalized {content_type} content")
        
        # Construct a detailed prompt
        prompt = f"""Generate personalized {content_type} content for a customer with the following attributes:
        Name: {customer_data.get('name', 'Customer')}
        Interests: {', '.join(customer_data.get('attributes', {}).get('interests', []))}
        
        Additional context:
        """
        for key, value in context.items():
            prompt += f"{key}: {value}\n"
        
        # Generate content
        response = await self.generate_response(prompt)
        return response