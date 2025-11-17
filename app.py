import streamlit as st
from dotenv import load_dotenv
import os

# Import the core logic modules
from core.gemini_client import GeminiClient
from core.qa_logic import format_prompt


def load_css(file_name: str):
    """
    Injects custom CSS to style the Streamlit app for a "good UI".
    [33, 34]
    """
    try:
        with open(file_name) as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")


@st.cache_resource
def get_gemini_client():
    """
    Cached factory function for the GeminiClient.
    Using @st.cache_resource ensures we initialize the client
    only once per session.
    """
    return GeminiClient()


def main():
    """
    The main function to run the Streamlit application.
    """
    # Load environment variables from.env file [30]
    load_dotenv()

    # Set page configuration [2]
    st.set_page_config(page_title="AI Document Analyst", layout="wide")

    # Load the custom CSS for a professional look [34]
    load_css("css/style.css")

    # App title
    st.title("📄 AI Document Analyst")
    st.markdown("Upload a document and ask questions about its content.")

    # Get the cached Gemini client
    try:
        client = get_gemini_client()
    except ValueError as e:
        st.error(f"Failed to initialize AI Client: {e}")
        return

    # Initialize session state for chat history and document context
    # [2]
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "doc_context" not in st.session_state:
        st.session_state.doc_context = None

    # --- Sidebar for File Upload ---
    with st.sidebar:
        st.header("Document Upload")
        uploaded_file = st.file_uploader(
            "Upload your text document",
            type=["txt"],
            accept_multiple_files=False
        )

        if uploaded_file is not None:
            try:
                # Read and decode the file content
                doc_bytes = uploaded_file.getvalue()
                st.session_state.doc_context = doc_bytes.decode("utf-8")

                # Clear chat and notify user
                st.session_state.messages = []
                st.success("Document loaded successfully!")
            except Exception as e:
                st.error(f"Error reading file: {e}")
                st.session_state.doc_context = None

    # --- Main Chat Interface ---

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input [5]
    if prompt := st.chat_input("Ask a question about your document..."):

        # 1. Check if a document has been uploaded
        if st.session_state.doc_context is None:
            st.error("Please upload a document first before asking questions.")
        else:
            # 2. Add user message to history and display it
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # 3. Generate and display the assistant's response
            with st.chat_message("assistant"):
                try:
                    # Format the prompt using our logic [7, 8]
                    full_prompt = format_prompt(
                        context=st.session_state.doc_context,
                        query=prompt
                    )

                    # Get the streaming response from the client [2]
                    response_stream = client.get_streaming_response(full_prompt)

                    # Use st.write_stream to display the response in real-time
                    full_response = st.write_stream(response_stream)

                    # 4. Add the full assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response
                    })

                except Exception as e:
                    error_message = f"An error occurred: {e}"
                    st.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })


if __name__ == "__main__":
    main()