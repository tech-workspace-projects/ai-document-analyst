#!/usr/bin/env python3
"""
Script to run DeepEval tests and generate HTML reports.
This provides a cross-platform way to run tests with proper reporting.
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    print("Running QA Evaluation Tests with HTML Report Generation...")
    print("=" * 60)

    # Get the project root directory
    script_dir = Path(__file__).parent

    # Detect if we're in tests/ or project root
    if script_dir.name == "tests":
        project_root = script_dir.parent
    else:
        project_root = script_dir

    # Change to project root
    os.chdir(project_root)
    print(f"📁 Working directory: {project_root}")

    # Verify test file exists
    test_file = project_root / "tests" / "test_qa_evaluation.py"
    if not test_file.exists():
        print(f"❌ ERROR: Test file not found at: {test_file}")
        print(f"   Current directory: {os.getcwd()}")
        return 1

    print(f"✓ Test file found: {test_file}")

    # Create reports directory if it doesn't exist
    reports_dir = project_root / "tests" / "logs"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Define the pytest command with absolute paths
    cmd = [
        "uv", "run", "pytest",
        str(test_file),
        "-v",
        f"--html={reports_dir / 'test_report.html'}",
        "--self-contained-html",
        "--log-cli-level=INFO",
        "--capture=tee-sys",
    ]

    # Run the tests
    try:
        result = subprocess.run(cmd, check=False)

        print()
        if result.returncode == 0:
            print("✓ Tests completed successfully!")
        else:
            print("✗ Some tests failed. Check the report for details.")

        print()
        print(f"📊 HTML Report generated at: {reports_dir / 'test_report.html'}")
        print(f"📝 Execution log saved at: {reports_dir / 'test_execution.log'}")
        print()
        print("To view the HTML report, run:")
        print(f"  open {reports_dir / 'test_report.html'}")

        return result.returncode

    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        return 130
    except Exception as e:
        print(f"\n✗ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

