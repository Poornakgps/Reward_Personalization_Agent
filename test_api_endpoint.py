from fastapi.testclient import TestClient
from workspace.app import app

# Create test client
client = TestClient(app)

# Test the recommendations endpoint
def test_recommendations():
    response = client.get("/api/customers/cust001/recommended_rewards")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

# Run the test
if __name__ == "__main__":
    test_recommendations()
