"""
Tests for the Email service.
"""
import pytest
from typing import Dict, Any
from unittest.mock import patch, AsyncMock
from workspace.services.email_service import EmailService

def test_initialization():
    """Test that the service initializes correctly."""
    service = EmailService()
    assert service is not None
    assert hasattr(service, "api_key")

@pytest.mark.asyncio
async def test_send_email():
    """Test that sending an email works."""
    service = EmailService()
    
    # Mock response since we don't want to call actual API in tests
    with patch.object(service, "send_email", new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {
            "email_id": "test_email_123",
            "status": "sent",
            "recipient": "test@example.com",
            "subject": "Test Subject",
            "timestamp": "2023-06-15T10:30:00Z"
        }
        
        # Call the method
        response = await service.send_email(
            recipient="test@example.com",
            subject="Test Subject",
            content="Test Content",
            metadata={"campaign_id": "test_campaign"}
        )
        
        # Check that the response is returned
        assert isinstance(response, dict)
        assert response["email_id"] == "test_email_123"
        assert response["status"] == "sent"
        assert response["recipient"] == "test@example.com"
        
        # Check that the method was called with the correct arguments
        mock_send.assert_called_once_with(
            recipient="test@example.com",
            subject="Test Subject",
            content="Test Content",
            metadata={"campaign_id": "test_campaign"}
        )

@pytest.mark.asyncio
async def test_send_personalized_campaign():
    """Test that sending a personalized campaign works."""
    service = EmailService()
    
    # Mock internal send_email method
    with patch.object(service, "send_email", new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {
            "email_id": "test_email_456",
            "status": "sent",
            "recipient": "customer_test@example.com",
            "subject": "Your personalized rewards",
            "timestamp": "2023-06-15T10:30:00Z"
        }
        
        # Call the method
        response = await service.send_personalized_campaign(
            customer_id="test",
            email_data={
                "subject": "Your personalized rewards",
                "content": "Campaign content",
                "campaign_id": "personalized_campaign"
            }
        )
        
        # Check that the response is returned
        assert isinstance(response, dict)
        assert response["email_id"] == "test_email_456"
        assert response["status"] == "sent"
        
        # Check that the method was called with appropriate arguments
        mock_send.assert_called_once()
        call_args = mock_send.call_args[1]
        assert call_args["subject"] == "Your personalized rewards"
        assert call_args["metadata"]["customer_id"] == "test"
        assert call_args["metadata"]["campaign_id"] == "personalized_campaign"

@pytest.mark.asyncio
async def test_track_engagement():
    """Test that tracking engagement works."""
    service = EmailService()
    
    # Mock response since we don't want to call actual API in tests
    with patch.object(service, "track_engagement", new_callable=AsyncMock) as mock_track:
        mock_track.return_value = {
            "event_id": "event_123",
            "email_id": "email_123",
            "event_type": "open",
            "timestamp": "2023-06-15T10:35:00Z",
            "status": "recorded"
        }
        
        # Call the method
        response = await service.track_engagement(
            email_id="email_123",
            event_type="open",
            metadata={"user_agent": "test-browser"}
        )
        
        # Check that the response is returned
        assert isinstance(response, dict)
        assert response["event_id"] == "event_123"
        assert response["email_id"] == "email_123"
        assert response["event_type"] == "open"
        assert response["status"] == "recorded"
        
        # Check that the method was called with the correct arguments
        mock_track.assert_called_once_with(
            email_id="email_123",
            event_type="open",
            metadata={"user_agent": "test-browser"}
        )
