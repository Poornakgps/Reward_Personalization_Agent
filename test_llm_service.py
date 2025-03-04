import asyncio
from workspace.services.llm_service import LLMService

async def test_llm():
    # Create the service
    service = LLMService()
    
    # Generate a response
    prompt = "Suggest a reward for a customer who loves technology products."
    response = await service.generate_response(prompt)
    
    # Print the result
    print(f"LLM Response to prompt: '{prompt}'")
    print("-" * 40)
    print(response)

# Run the test
if __name__ == "__main__":
    asyncio.run(test_llm())
