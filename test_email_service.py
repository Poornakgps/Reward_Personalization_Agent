import asyncio
from workspace.services.email_service import EmailService

async def test_email():
    # Create the service
    service = EmailService()
    
    # Send a test email
    response = await service.send_email(
        recipient="test@example.com",
        subject="Test Email",
        content="This is a test email from the Reward Personalization Agent."
    )
    
    # Print the result
    print(f"Email send result:")
    print(f"Email ID: {response['email_id']}")
    print(f"Status: {response['status']}")
    print(f"Timestamp: {response['timestamp']}")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_email())
