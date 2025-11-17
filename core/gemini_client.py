import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from helpers.logger import Logger


# Global singleton instance
logger = Logger().get_logger()

class GeminiClient:
    """
    A client class for interacting with the Google Gemini API.

    This class encapsulates API configuration, model initialization,
    and response generation, including a critical system prompt
    to ensure the model adheres to its role as a QA analyst.
    """

    def __init__(self):
        """
        Initializes the Gemini client.

        Loads the API key, configures the 'genai' module, defines
        the system instruction, and initializes the GenerativeModel.
        """
        try:
            # Load the API key from environment variables [2, 30]
            self.api_key = os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError("GOOGLE_API_KEY not found in.env file.")

            genai.configure(api_key=self.api_key)

        except Exception as e:
            logger.info(f"Error configuring Gemini: {e}")
            raise

        # This is the core reliability layer for the QA bot.
        # It instructs the model to be faithful to the context.
        # Gemini 1.5+ models support this 'system_instruction' [35]
        system_prompt = (
            "You are an expert Question-Answering Analyst. You will be given a Document "
            "Context followed by a Question. Your task is to answer the Question "
            "based *only* on the information provided in the Document Context. "
            "Do not use any outside knowledge. If the answer is not found in the "
            "Document Context, you must state: 'I am sorry, but the provided "
            "document does not contain the answer to this question.'"
        )

        # Safety settings to block harmful content
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        # Initialize the model with fallback mechanism
        # Try different model names as some may not be available on all API keys
        model_names_to_try = [
            "models/gemini-2.5-flash-preview-05-20",
            "gemini-1.5-flash",
            "gemini-1.5-flash-002",
            "gemini-1.5-flash-latest",
            "gemini-pro",
        ]

        self.model = None
        last_error = None

        for model_name in model_names_to_try:
            try:
                logger.info(f"Trying to initialize model: {model_name}")
                self.model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_prompt,
                    safety_settings=self.safety_settings
                )
                # Test the model with a simple query
                test_response = self.model.generate_content("Hello")
                logger.info(f"Successfully initialized model: {model_name}")
                break
            except Exception as e:
                last_error = e
                logger.info(f"Failed to initialize {model_name}: {e}")
                continue

        if self.model is None:
            raise ValueError(f"Could not initialize any Gemini model. Last error: {last_error}")

    def get_streaming_response(self, prompt_content: str):
        """
        Generates a response from the Gemini model in a streaming fashion.

        Args:
            prompt_content: The formatted prompt (context + query).

        Yields:
            str: Chunks of the response text as they are generated.
        """
        try:
            # Call the model, 'stream=True' is key for the interactive UI [2]
            response_stream = self.model.generate_content(
                prompt_content,
                stream=True
            )

            # Yield each text chunk
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.info(f"Error generating streaming response: {e}")
            yield "An error occurred while processing your request. Please check the logs."
