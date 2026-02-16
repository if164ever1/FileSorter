
import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiClient:
    """A client for interacting with the Gemini API."""

    def __init__(self):
        """Initializes the Gemini client.

        Loads the API key from the .env file and configures the genai library.
        """
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def check_connection(self) -> bool:
        """Checks the connection to the Gemini API.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        if not self.api_key:
            return False
        try:
            # Perform a lightweight operation to check the connection
            genai.list_models()
            return True
        except Exception as e:
            print(f"An error occurred while checking the Gemini API connection: {e}")
            return False
