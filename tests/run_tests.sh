#!/usr/bin/env bash
# Script to run DeepEval tests and generate HTML reports

echo "Running QA Evaluation Tests with HTML Report Generation..."
echo "============================================================"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Determine project root
if [[ "$SCRIPT_DIR" == */tests ]]; then
    # Script is in tests/ directory
    PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
else
    # Script is in project root
    PROJECT_ROOT="$SCRIPT_DIR"
fi

# Change to project root
cd "$PROJECT_ROOT"
echo "📁 Working directory: $PROJECT_ROOT"

# Check if test file exists
TEST_FILE="$PROJECT_ROOT/tests/test_qa_evaluation.py"
if [ ! -f "$TEST_FILE" ]; then
    echo "❌ ERROR: Test file not found at: $TEST_FILE"
    echo "   Current directory: $(pwd)"
    exit 1
fi

echo "✓ Test file found: $TEST_FILE"

# Create reports directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/tests/reports"

# Run pytest with HTML report generation
uv run pytest "$TEST_FILE" \
    -v \
    --html="$PROJECT_ROOT/tests/reports/test_report.html" \
    --self-contained-html \
    --log-cli-level=INFO \
    --capture=tee-sys

# Check if the test run was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Tests completed successfully!"
else
    echo ""
    echo "✗ Some tests failed. Check the report for details."
fi

echo ""
echo "📊 HTML Report generated at: tests/reports/test_report.html"
echo "📝 Execution log saved at: tests/reports/test_execution.log"
echo ""
echo "To view the HTML report, run:"
echo "  open tests/reports/test_report.html"

