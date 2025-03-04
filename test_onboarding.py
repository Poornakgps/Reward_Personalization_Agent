import asyncio
from workspace.workflows.customer_onboarding import CustomerOnboardingWorkflow

async def test_workflow():
    # Create the workflow
    workflow = CustomerOnboardingWorkflow()
    
    # Execute for a test customer
    customer_id = "new_customer"
    result = await workflow.execute(customer_id)
    
    # Print the results
    print(f"Onboarding result for {customer_id}:")
    print(f"Status: {result['status']}")
    print(f"Email sent: {result['email_sent']['status']}")
    print(f"Next engagement scheduled: {result['next_engagement_scheduled']}")
    print(f"Next engagement date: {result['next_engagement_date']}")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_workflow())
