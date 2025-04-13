# app/config.py
import os
from dotenv import load_dotenv


# Load environment variables from a .env file if present.
load_dotenv()


class Config:
    """
    Base configuration for the Caelum ADHD Assistant.
    Loads environment variables and sets default values.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = False
    TESTING = False

    # API Keys & Service Credentials
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

    # Paths & Directories
    
    AUDIO_OUTPUT_DIR = os.getenv("AUDIO_OUTPUT_DIR", "app/static/audio")
    
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

    # Voice Mapping (for future extensibility; fixed in simplified branch)
    VOICE_MAP = {
        "Beau": "21m00Tcm4TlvDq8ikWAM",
        "Fox": "TxGEqnHWrfWFTfGW9XjX",
        "Jasper": "AZnzlk1XvdvUeBnXmlld",
        "Orion": "EXAVITQu4vr4xnSDxMaL",
        "Theo": "MF3mGyEYCl7XYWbV9V6O"
    }

    # Optional Celery configuration.
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

class DevelopmentConfig(Config):
    """Configuration for development."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration for production."""
    DEBUG = False
