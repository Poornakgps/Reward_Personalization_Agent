"""
Application settings and configuration.
"""
import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # API Configuration
    PORT: int = Field(default=8000, env="PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Database Configuration
    DATABASE_URL: str = Field(default="", env="DATABASE_URL")
    
    # LLM Configuration
    GROQ_API_KEY: str = Field(default="", env="GROQ_API_KEY")
    LLM_MODEL: str = Field(default="llama3-70b", env="LLM_MODEL")
    
    # Email Service
    EMAIL_API_KEY: str = Field(default="", env="EMAIL_API_KEY")
    
    # Reward Personalization Settings
    DEFAULT_EMAIL_FREQUENCY: int = Field(default=7, description="Default email frequency in days")
    MIN_ENGAGEMENT_THRESHOLD: float = Field(default=0.1, description="Minimum engagement rate to continue journey")
    MAX_EMAILS_BEFORE_DOWNGRADE: int = Field(default=5, description="Max number of emails before reducing frequency")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()