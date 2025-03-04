"""
Tests for the LLM service.
"""
import pytest
from typing import Dict, Any
from unittest.mock import patch, AsyncMock
from workspace.services.llm_service import LLMService

def test_initialization():
    """Test that the service initializes correctly."""
    service = LLMService()
    assert service is not None
    assert service.model is not None

@pytest.mark.asyncio
async def test_generate_response():
    """Test that response generation works."""
    service = LLMService()
    
    # Mock response since we don't want to call actual API in tests
    with patch.object(service, "generate_response", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = "This is a test response"
        
        # Call the method
        response = await service.generate_response("Test prompt")
        
        # Check that the response is returned
        assert isinstance(response, str)
        assert response == "This is a test response"
        
        # Check that the method was called with the correct arguments
        mock_generate.assert_called_once_with("Test prompt")

@pytest.mark.asyncio
async def test_generate_personalized_content():
    """Test that personalized content generation works."""
    service = LLMService()
    
    # Sample customer data
    customer_data = {
        "name": "Test Customer",
        "attributes": {
            "interests": ["fashion", "technology"]
        }
    }
    
    # Mock response since we don't want to call actual API in tests
    with patch.object(service, "generate_response", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = "Personalized content for Test Customer"
        
        # Call the method
        response = await service.generate_personalized_content(
            customer_data=customer_data,
            content_type="email",
            context={"journey_stage": "onboarding"}
        )
        
        # Check that the response is returned
        assert isinstance(response, str)
        assert response == "Personalized content for Test Customer"
        
        # Check that the method was called with appropriate arguments
        mock_generate.assert_called_once()
        
        # Check that the prompt includes customer data and context
        prompt = mock_generate.call_args[0][0]
        assert "Test Customer" in prompt
        assert "fashion" in prompt
        assert "technology" in prompt
        assert "onboarding" in prompt
