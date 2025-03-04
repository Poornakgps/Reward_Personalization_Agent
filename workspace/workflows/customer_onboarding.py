"""
Workflow for onboarding new customers.
"""
from typing import Dict, Any
from workspace.utils.logger import setup_logger
from workspace.agents.reward_matching_agent import RewardMatchingAgent
from workspace.agents.content_selection_agent import ContentSelectionAgent
from workspace.services.email_service import EmailService

logger = setup_logger(__name__)

class CustomerOnboardingWorkflow:
    """Workflow for onboarding new customers."""
    
    def __init__(self):
        self.reward_agent = RewardMatchingAgent()
        self.content_agent = ContentSelectionAgent()
        self.email_service = EmailService()
        logger.info("CustomerOnboardingWorkflow initialized")
    
    async def execute(self, customer_id: str) -> Dict[str, Any]:
        """
        Execute the onboarding workflow for a new customer.
        
        Args:
            customer_id: ID of the customer to onboard
            
        Returns:
            Results of the workflow execution
        """
        logger.info(f"Executing onboarding workflow for customer {customer_id}")
        
        # Step 1: Get initial reward recommendations
        rewards = self.reward_agent.get_recommendations(customer_id, limit=3)
        
        # Step 2: Select content for welcome email
        content_plan = self.content_agent.select_content(
            customer_id, 
            context={
                "journey_stage": "onboarding",
                "profile_completion": 0.2,  # New customer has minimal profile
                "days_since_signup": 0,
                "recommended_rewards": rewards
            }
        )
        
        # Step 3: Send welcome email
        email_data = {
            "subject": "Welcome to Our Rewards Program",
            "campaign_id": "welcome_series",
            "content": "Welcome email content would be generated here",
            "rewards": rewards
        }
        
        email_result = await self.email_service.send_personalized_campaign(
            customer_id, email_data
        )
        
        # Step 4: Schedule follow-up engagement
        # In a real implementation, would create entries in a task queue/scheduler
        
        return {
            "workflow_id": f"onboarding_{customer_id}",
            "customer_id": customer_id,
            "status": "completed",
            "email_sent": email_result,
            "next_engagement_scheduled": True,
            "next_engagement_date": "2023-06-22T10:00:00Z"  # 7 days later
        }
