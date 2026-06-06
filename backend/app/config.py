import os
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()

class Config:
    WEATHER_AI_API_KEY: str = os.getenv("WEATHER_AI_API_KEY")
    WEATHER_AI_BASE_URL: str = os.getenv("WEATHER_AI_BASE_URL", "https://api.weather-ai.co/v1")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

config = Config()