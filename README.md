# AI Document Analyst

An intelligent document question-answering system powered by Google Gemini AI.

## Features

- 📄 Upload and analyze text documents
- 💬 Interactive chat interface using Streamlit
- 🤖 Powered by Google Gemini 2.5 Flash
- 🎯 Context-aware answers based solely on document content
- ✅ Comprehensive test suite with DeepEval metrics

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the Application

```bash
uv run streamlit run app.py
```

### 4. Run Tests

```bash
uv run python tests/run_tests.py
```

For detailed testing instructions, see [tests/TESTING.md](tests/TESTING.md)

## Project Structure

```
ai-document-analyst/
├── app.py                 # Main Streamlit application
├── core/                  # Core business logic
│   ├── gemini_client.py  # Gemini API client
│   └── qa_logic.py       # Q&A logic
├── helpers/              # Helper utilities
│   └── logger.py         # Logging configuration
├── css/                  # Stylesheets
│   └── style.css
├── tests/                # Test suite
│   ├── test_qa_evaluation.py  # Main evaluation tests
│   ├── test_gemini.py         # API connection test
│   ├── run_tests.py           # Test runner script
│   ├── run_tests.sh           # Test runner (bash)
│   ├── data/                  # Test data
│   ├── reports/               # Test reports (generated)
│   └── TESTING.md             # Testing documentation
└── pyproject.toml        # Project dependencies
```

## Testing

The project includes a comprehensive test suite using DeepEval to evaluate:
- Answer Relevancy
- Faithfulness to context
- Contextual Relevancy

See [tests/TESTING.md](tests/TESTING.md) for complete testing documentation.

## License

[Your License Here]


