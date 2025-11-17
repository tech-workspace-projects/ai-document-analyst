#!/usr/bin/env python3
"""
Quick diagnostic script to check test setup and run tests.
Run this if you encounter any issues.
"""
import os
import sys
from pathlib import Path

def main():
    print("=" * 70)
    print("🔍 TEST SETUP DIAGNOSTIC")
    print("=" * 70)

    # Find project root
    current_dir = Path.cwd()
    script_dir = Path(__file__).parent

    print(f"\n📂 Current working directory: {current_dir}")
    print(f"📂 Script location: {script_dir}")

    # Determine project root
    if script_dir.name == "tests":
        project_root = script_dir.parent
    else:
        project_root = script_dir

    print(f"📂 Project root: {project_root}")

    # Check critical files
    print("\n" + "=" * 70)
    print("📋 CHECKING FILES")
    print("=" * 70)

    checks = []

    files_to_check = [
        (project_root / "tests" / "test_qa_evaluation.py", "Main test file"),
        (project_root / "tests" / "test_gemini.py", "API test script"),
        (project_root / "tests" / "run_tests.py", "Test runner"),
        (project_root / "tests" / "conftest.py", "Pytest config (path setup)"),
        (project_root / "tests" / "data" / "golden_qa_dataset.jsonl", "Test dataset"),
        (project_root / "tests" / "pytest.ini", "Pytest config"),
        (project_root / ".env", "Environment file"),
        (project_root / "core" / "gemini_client.py", "Gemini client"),
        (project_root / "core" / "qa_logic.py", "QA logic"),
        (project_root / "helpers" / "logger.py", "Logger helper"),
    ]

    all_good = True
    for filepath, description in files_to_check:
        exists = filepath.exists()
        checks.append(exists)
        status = "✅" if exists else "❌"
        print(f"{status} {description}: {filepath.relative_to(project_root)}")
        if not exists:
            all_good = False

    # Check environment
    print("\n" + "=" * 70)
    print("🔐 CHECKING ENVIRONMENT")
    print("=" * 70)

    env_file = project_root / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)

        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            masked_key = api_key[:10] + "..." if len(api_key) > 10 else "***"
            print(f"✅ GOOGLE_API_KEY found: {masked_key}")
        else:
            print("❌ GOOGLE_API_KEY not found in .env file")
            all_good = False
    else:
        print("❌ .env file not found")
        all_good = False

    # Provide recommendations
    print("\n" + "=" * 70)
    print("📝 RECOMMENDATIONS")
    print("=" * 70)

    if all_good:
        print("✅ All checks passed! You're ready to run tests.")
        print("\n🚀 To run tests, use one of these commands:")
        print(f"\n   From anywhere:")
        print(f"   cd {project_root}")
        print(f"   uv run python tests/run_tests.py")
        print(f"\n   Direct pytest:")
        print(f"   cd {project_root}")
        print(f"   uv run pytest tests/test_qa_evaluation.py -v")
    else:
        print("⚠️  Some files are missing. Please check the errors above.")

        if not (project_root / ".env").exists():
            print("\n💡 Create .env file:")
            print(f"   echo 'GOOGLE_API_KEY=your_key_here' > {project_root}/.env")

        if not (project_root / "tests" / "test_qa_evaluation.py").exists():
            print("\n⚠️  Main test file is missing. You may need to check your installation.")

    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())

