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
    IP_ADDRESS: str = os.getenv("IP_ADDRESS", "")
    PORT: int = int(os.getenv("PORT", 8000))

    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_TOKEN_EXPIRE_IN_DAYS: int = int(os.getenv("JWT_TOKEN_EXPIRE_IN_DAYS", 7))

    # Redis Settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis").strip()
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379").strip())

    def __init__(self):
        # Fail-fast validation: Ensure key configuration is present
        if not self.DATABASE_URL:
            raise ValueError(
                f"DATABASE_URL is not set for ENV='{self.ENV}'. "
                f"Please check your {env_file.name} file."
            )


# Create a global settings instance
settings = Settings()

# Diagnostic logging for startup
print(f"DEBUG: Loaded DATABASE_URL: {settings.DATABASE_URL[:20]}...")
print(f"DEBUG: Loaded REDIS_HOST: '{settings.REDIS_HOST}'")
print(f"DEBUG: Loaded REDIS_PORT: {settings.REDIS_PORT}")
