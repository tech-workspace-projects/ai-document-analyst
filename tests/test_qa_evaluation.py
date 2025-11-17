import pytest
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import Generator

# Add project root to Python path so we can import core modules
# This allows the test to find core.gemini_client, core.qa_logic, etc.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import DeepEval components
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric
)  # [9, 12, 13, 32]
from deepeval.models.base_model import DeepEvalBaseLLM

# Import the application's core logic
from core.gemini_client import GeminiClient
from core.qa_logic import format_prompt
from helpers.logger import Logger


# Global singleton instance
logger = Logger().get_logger()


# --- Custom Gemini Model Wrapper for DeepEval ---
# DeepEval requires a model wrapper that implements DeepEvalBaseLLM
class GeminiModelWrapper(DeepEvalBaseLLM):
    """Wrapper to use Gemini with DeepEval metrics."""

    def __init__(self, model_name: str = "models/gemini-2.5-flash-preview-05-20"):
        self.model_name = model_name
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)

    def load_model(self):
        """Load the model (already loaded in __init__)."""
        return self.model

    def generate(self, prompt: str) -> str:
        """Generate response from the model."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.info(f"Error in Gemini model generation: {e}")
            return f"Error: {e}"

    async def a_generate(self, prompt: str) -> str:
        """Async generate (DeepEval may use this)."""
        return self.generate(prompt)

    def get_model_name(self) -> str:
        """Return the model name."""
        return self.model_name


# Load environment variables
load_dotenv()

# Create Gemini model wrapper for DeepEval metrics
gemini_model = GeminiModelWrapper()

# Set thresholds for pass/fail [26, 36]
answer_relevancy_metric = AnswerRelevancyMetric(
    threshold=0.7,
    model=gemini_model,
    include_reason=True
)
faithfulness_metric = FaithfulnessMetric(
    threshold=0.8,
    model=gemini_model,
    include_reason=True
)  # [12, 13]
contextual_relevancy_metric = ContextualRelevancyMetric(
    threshold=0.6,
    model=gemini_model,
    include_reason=True
)


def load_test_cases() -> Generator:
    """
    Loads the golden dataset, runs the app logic to get 'actual_output',
    and yields a fully formed LLMTestCase for pytest.
    """

    # Initialize the *actual* application client
    # This makes it an end-to-end test
    try:
        client = GeminiClient()
    except ValueError as e:
        logger.info(f"Failed to initialize GeminiClient in test: {e}")
        pytest.skip(f"Skipping tests, API key issue: {e}")
        return

    # Path to the golden dataset - use absolute path based on test file location
    test_dir = Path(__file__).parent
    dataset_path = test_dir / "data" / "golden_qa_dataset.jsonl"

    # Verify dataset exists
    if not dataset_path.exists():
        pytest.fail(f"Golden dataset not found: {dataset_path}")
        return

    try:
        with open(dataset_path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue

                golden = json.loads(line)

                # --- 1. Prepare Inputs ---
                input_query = golden["input"]
                retrieval_context = golden["retrieval_context"]
                expected_output = golden["expected_output"]

                # --- 2. Run App Logic to get Actual Output ---
                # This is the "end-to-end" part. We are testing the
                # *actual* response from the live model.

                # Format the prompt just like the app does
                formatted_prompt = format_prompt(retrieval_context, input_query)

                # Get the streaming response and collect it
                response_stream = client.get_streaming_response(formatted_prompt)

                # Collect the full string from the generator
                actual_output_chunks = []
                try:
                    for chunk in response_stream:
                        actual_output_chunks.append(chunk)
                except Exception as e:
                    logger.info(f"Error during model generation for test '{input_query}': {e}")
                    actual_output = f"Error: {e}"

                if not actual_output_chunks:
                    actual_output = "Error: No output from model"
                else:
                    actual_output = "".join(actual_output_chunks)

                # --- 3. Create the DeepEval Test Case ---
                # This object contains all data needed for evaluation [9, 11]
                test_case = LLMTestCase(
                    input=input_query,
                    actual_output=actual_output,
                    expected_output=expected_output,
                    retrieval_context=[retrieval_context]  # Must be a list
                )

                # Yield the test case for pytest to consume
                yield test_case

    except FileNotFoundError:
        logger.info(f"Golden dataset not found at: {dataset_path}")
        pytest.fail(f"Golden dataset not found: {dataset_path}")
    except Exception as e:
        logger.info(f"Error loading test cases: {e}")
        pytest.fail(f"Error loading test cases: {e}")


# --- The Pytest Test Function ---
# This single function *is* the 20+ test suite.
# Pytest's 'parametrize' decorator calls this function
# once for each test case yielded by 'load_test_cases'.
# [9, 20, 25]
@pytest.mark.parametrize("test_case", load_test_cases())
def test_qa_agent_evaluation(test_case: LLMTestCase):
    """
    Runs the DeepEval assertion on the generated test case.
    """
    # assert_test runs all specified metrics and validates them
    # against their internal thresholds. [9, 10, 26]
    assert_test(
        test_case,
        [
            answer_relevancy_metric,
            faithfulness_metric,
            contextual_relevancy_metric
        ]
    )