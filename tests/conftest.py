"""
Pytest configuration file for test discovery and setup.
This file is automatically loaded by pytest and configures the test environment.
"""
import sys
import os
from pathlib import Path

# Add the project root directory to Python path
# This allows tests to import from core, helpers, etc.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set up environment variables for testing
from dotenv import load_dotenv
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    print("Warning: .env file not found. Some tests may fail without GOOGLE_API_KEY.")

