import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Configs:
    """Container for API keys used by the MoMo assistant"""
    def __init__(self):
        """Initialize API keys from environment variables"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.serper_api_key = os.getenv("SERPSEARCH_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model_to_use = os.getenv("MODEL_TO_USE", "gpt-4o-mini")

        self._validate_keys()

    def _validate_keys(self):
        """Validate that required API keys are present"""
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")

# Create a singleton instance
CONFIGS = Configs()
