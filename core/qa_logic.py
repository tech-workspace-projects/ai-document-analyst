def format_prompt(context: str, query: str) -> str:
    """
    Constructs the final prompt string to be sent to the Gemini API.

    Uses clear XML-like tags to delineate the context and the query,
    which improves the model's ability to differentiate between the two
    and adhere to the system instructions.

    Args:
        context: The full text of the uploaded document.
        query: The user's question.

    Returns:
        str: The fully formatted prompt.
    """

    # Structured prompting is crucial for accuracy [7, 8]
    prompt = f"""

{context}



{query}


Answer:
"""
    return prompt