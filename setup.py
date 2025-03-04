from setuptools import setup, find_packages

setup(
    name="reward_personalization_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "phidata>=2.0.0",
        "llama-index>=0.8.0",
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0",
    ],
    python_requires=">=3.10",
    author="Your Name",
    author_email="your.email@example.com",
    description="Reward Personalization Agent using PhiData",
)
