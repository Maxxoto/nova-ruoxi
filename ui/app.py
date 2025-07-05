from backend.nova import get_nova_response
import streamlit as st
import sys
import re
from pathlib import Path

# Add project root to path to enable backend imports
sys.path.append(str(Path(__file__).parent.parent))


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "global_thinking" not in st.session_state:
    st.session_state.global_thinking = None

# Create global info placeholder at top-left
global_info = st.empty()

# Set page configuration
st.set_page_config(
    page_title="Nova Chat Interface",
    page_icon="💬",
    layout="wide"
)

# App title
st.title("Nova Chat Interface")

# Display global thinking content if exists
if st.session_state.global_thinking:
    with global_info.container():
        with st.expander("Show Reasoning"):
            st.markdown(st.session_state.global_thinking)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message to Nova..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        try:
            # Show loading spinner in global info area
            with global_info.container():
                with st.spinner("Nova is thinking..."):
                    # Get response from backend service
                    response = get_nova_response(
                        user_query=prompt,
                        groq_api_key=st.secrets["GROQ_API_KEY"]
                    )

            # Parse response to separate thinking from main answer
            thinking_match = re.search(
                r'<think>(.*?)</think>', response, re.DOTALL)
            thinking_content = thinking_match.group(
                1).strip() if thinking_match else None
            main_answer = re.sub(r'<think>.*?</think>', '',
                                 response, flags=re.DOTALL).strip()

            # Update global thinking content
            st.session_state.global_thinking = thinking_content

            # Display main answer
            st.markdown(main_answer)

            # Add to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": main_answer})

        except Exception as e:
            st.error(f"Error getting response: {str(e)}")
