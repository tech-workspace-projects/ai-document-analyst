# Testing Guide

This document explains how to run the QA evaluation tests and generate HTML reports.

## Prerequisites

Make sure you have:
1. Set up your `.env` file with `GOOGLE_API_KEY`
2. Installed all dependencies with `uv sync`

## Testing API Connection

Before running the full test suite, you can verify your Gemini API connection and see available models:

```bash
uv run python tests/test_gemini.py
```

This utility script will:
- List all available Gemini models for your API key
- Test which models work with your configuration
- Show you the correct model name to use

## Running Tests with HTML Reports

### Option 1: Using the Python Script (Recommended)

```bash
uv run python tests/run_tests.py
```

Or from within the tests directory:
```bash
cd tests
uv run python run_tests.py
```

### Option 2: Using the Shell Script

```bash
chmod +x tests/run_tests.sh
./tests/run_tests.sh
```

Or from within the tests directory:
```bash
cd tests
chmod +x run_tests.sh
./run_tests.sh
```

### Option 3: Direct pytest Command

```bash
uv run pytest tests/test_qa_evaluation.py -v --html=tests/reports/test_report.html --self-contained-html
```

## Output Files

After running tests, you'll find:

- **HTML Report**: `tests/reports/test_report.html` - Interactive HTML report with test results
- **Execution Log**: `tests/reports/test_execution.log` - Detailed log file with timestamps

## Viewing the HTML Report

### On macOS:
```bash
open tests/reports/test_report.html
```

### On Linux:
```bash
xdg-open tests/reports/test_report.html
```

### On Windows:
```bash
start tests/reports/test_report.html
```

Or simply open the file in your browser.

## HTML Report Features

The HTML report includes:
- ✅ Test pass/fail status for each test case
- 📊 Summary statistics (passed, failed, skipped)
- ⏱️ Execution time for each test
- 📝 Detailed error messages and stack traces for failed tests
- 🔍 Expandable sections for test details
- 📈 Visual indicators for test results

## 🎯 DeepEval Metrics Tracked

The tests evaluate three key metrics using **Gemini as the LLM judge**:

1. **Answer Relevancy** (threshold: 0.7)
   - Measures how relevant the answer is to the question
   
2. **Faithfulness** (threshold: 0.8)
   - Ensures the answer is faithful to the provided context
   
3. **Contextual Relevancy** (threshold: 0.6)
   - Evaluates if the retrieved context is relevant to the question

### Gemini Integration

The test suite uses a custom `GeminiModelWrapper` class to integrate Gemini with DeepEval:
- Model: `models/gemini-2.5-flash-preview-05-20`
- Configured automatically from your `GOOGLE_API_KEY`
- No need to run `deepeval set-gemini` - everything is handled in code
- The wrapper implements DeepEval's `DeepEvalBaseLLM` interface

## Test Data

Test cases are loaded from:
- `tests/data/golden_qa_dataset.jsonl`

Each line in the file contains a JSON object with:
- `input`: The question
- `retrieval_context`: The document context
- `expected_output`: The expected answer

## Troubleshooting

### File or directory not found: tests/test_qa_evaluation.py

This error occurs when running from the wrong directory. **Solutions:**

1. **Always run from project root:**
   ```bash
   cd /Users/prabhpan/Prabhu/projects/ai-document-analyst
   uv run python tests/run_tests.py
   ```

2. **Or use absolute paths:**
   ```bash
   uv run pytest /Users/prabhpan/Prabhu/projects/ai-document-analyst/tests/test_qa_evaluation.py -v
   ```

3. **Verify file exists:**
   ```bash
   ls -la tests/test_qa_evaluation.py
   ```

The updated `run_tests.py` script now automatically detects and changes to the project root, so this should work from any directory.

### No tests collected
- Check that `tests/data/golden_qa_dataset.jsonl` exists and contains valid JSON

### API Key errors
- Ensure `GOOGLE_API_KEY` is set in your `.env` file
- Verify the API key has access to Gemini models

### Model initialization errors
- The system will try multiple model names automatically
- Check the logs to see which model was used

## CI/CD Integration

To integrate with CI/CD pipelines:

```bash
uv run pytest tests/test_qa_evaluation.py \
    --html=test-report.html \
    --self-contained-html \
    --junitxml=test-results.xml
```

The JUnit XML format can be consumed by CI systems like Jenkins, GitLab CI, GitHub Actions, etc.

