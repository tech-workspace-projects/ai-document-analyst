"""Quick test script to verify Gemini API connection and list available models."""
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path to access project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in environment")
    exit(1)

genai.configure(api_key=api_key)

# List available models
print("Available Gemini models:")
print("-" * 60)
flash_models = []
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Supported methods: {model.supported_generation_methods}")
        print()
        if 'flash' in model.name.lower():
            flash_models.append(model.name)

# Test available flash models
if flash_models:
    print(f"\n\nFound {len(flash_models)} Flash model(s). Testing the first one...")
    test_model_name = flash_models[0]
    print(f"Testing {test_model_name}...")
    try:
        model = genai.GenerativeModel(test_model_name)
        response = model.generate_content("Say 'Hello, I am working!'")
        print(f"✓ Success! Response: {response.text}")
        print(f"\n✓✓ USE THIS MODEL NAME: {test_model_name}")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("\n✗ No Flash models found. Trying common model names...")

    # Try common model name variations
    test_names = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-latest",
        "gemini-pro",
        "gemini-1.5-pro",
    ]

    for name in test_names:
        print(f"\nTrying '{name}'...")
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content("Say 'Hello, I am working!'")
            print(f"✓ Success with '{name}'! Response: {response.text}")
            print(f"\n✓✓ USE THIS MODEL NAME: {name}")
            break
        except Exception as e:
            print(f"✗ Failed: {e}")

