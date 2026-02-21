from pathlib import Path
from dotenv import load_dotenv
import os

# Define the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Get the environment setting (default to 'development')
ENV = os.getenv("ENV", "development")

# Load the appropriate environment variables based on the current ENV
if ENV == "development":
    env_file = BASE_DIR / ".env.development"
elif ENV == "production":
    env_file = BASE_DIR / ".env.production"
else:
    env_file = BASE_DIR / ".env"

if env_file.exists():
    load_dotenv(env_file)
else:
    # Log a warning or handle missing env files as needed
    pass


class Settings:
    """
    Centralized settings for the application.
    Supports environment-based configuration.
    """

    ENV: str = ENV
    # Ensure DATABASE_URL is always a string to avoid Pyright/type errors
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")


# Create a global settings instance
settings = Settings()
