import json
import streamlit as st
import sys
import re
from pathlib import Path

from backend.utils.response_formatter import format_response, format_chat_history_for_display


# Add project root to path to enable backend imports
sys.path.append(str(Path(__file__).parent.parent))


from backend.nova import RuoAgent

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
else:
    # Ensure all existing messages are in the correct format for display
    # by re-processing them through format_chat_history_for_display
    # This handles any legacy or incorrectly formatted messages from previous sessions
    current_messages = st.session_state.messages
    st.session_state.messages = []  # Clear and rebuild

    # Iterate and format
    # The format_chat_history_for_display expects BaseMessage objects, or similar objects with .content and .type
    # We must ensure that what's passed into it is either a BaseMessage object or a dict that contains it's content and type.
    # For now, we assume that any existing messages being iterated through are either already Streamlit-compatible dicts
    # or BaseMessage objects.
    for msg in current_messages:
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            # Already in expected format
            st.session_state.messages.append(msg)
        elif hasattr(msg, "type") and hasattr(msg, "content"):
            # LangChain BaseMessage - convert using our utility
            formatted = format_chat_history_for_display([msg])
            st.session_state.messages.extend(formatted)
        elif isinstance(msg, dict) and "messages" in msg and isinstance(msg["messages"], list):
            # This handles the case where the full graph response was stored directly
            formatted = format_chat_history_for_display(msg["messages"])
            st.session_state.messages.extend(formatted)
        else:
            # Fallback for unexpected types - treat as unknown role
            st.session_state.messages.append({"role": "unknown", "content": str(msg)})


# Set page configuration
st.set_page_config(page_title="Nova Chat Interface", page_icon="💬", layout="wide")

# App title
st.title("Nova 若曦")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message to Nova..."):
    # Add user message to chat history
    # Format the user's message correctly for storage
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Initiate agent (or retrieve from session state)
    if "ruo_agent_instance" not in st.session_state:
        st.session_state.ruo_agent_instance = RuoAgent()
    ruo_agent_instance = st.session_state.ruo_agent_instance
    agent = ruo_agent_instance.agent

    # Display assistant response
    with st.chat_message("assistant"):
        try:
            response = None
            if prompt.strip().lower() == "summarize chat":
                with st.spinner("Summarizing chat history..."):
                    summarize_tool = next((t for t in ruo_agent_instance.tools if t.name == "summarize_chat"), None)
                    if summarize_tool:
                        # Direct tool invocation
                        response = summarize_tool.invoke(st.session_state.messages)
                    else:
                        st.error("Summarize tool not found.")
                        response = {"messages": [{"content": "Summarize tool not found."}]}
            else:
                with st.spinner("Nova is thinking..."):
                    # Get response from backend service
                    # Using a fixed thread_id for now, can be made dynamic if multiple threads are needed
                    response = agent.invoke({"messages": prompt}, config={"configurable": {"thread_id": "default_thread"}})

            # If response is a direct tool output (like from summarize_chat)
            if isinstance(response, str):
                try:
                    response_data = json.loads(response)
                    if isinstance(response_data, dict) and response_data.get("action") == "summarize_and_clear":
                        st.session_state.messages = []
                        st.session_state.messages.append({"role": "assistant", "content": response_data["summary"]})
                        with st.chat_message("assistant"):
                            st.markdown(response_data["summary"])
                        st.stop()  # Stop further execution to prevent normal message processing
                except json.JSONDecodeError:
                    pass  # Not a JSON response, proceed to normal handling below

            # Initialize thinking_content
            thinking_content = None

            # Retrieve the last message from the response, which should be the AIMessage
            last_message = None
            if isinstance(response, dict) and "messages" in response and response["messages"]:
                last_message = response["messages"][-1]

            # Check for thinking content in additional_kwargs of the last message
            if last_message and hasattr(last_message, "additional_kwargs") and "reasoning_content" in last_message.additional_kwargs:
                thinking_content = last_message.additional_kwargs["reasoning_content"]

            # If not found in additional_kwargs, then process the main content for <think> tags
            # Directly pass the full response object to format_response
            content = format_response(response)

            thinking_match = re.search(r"<think>(.*?)</think>", content, re.DOTALL)
            if thinking_match:
                thinking_content += "\n" + thinking_match.group(1).strip() if thinking_match else None

            second_thinking_match = re.search(r"<thinking>(.*?)</thinking>", content, re.DOTALL)
            if second_thinking_match:
                thinking_content += "\n" + second_thinking_match.group(1).strip() if second_thinking_match else None

            # For tool use agent (and other non-tool responses)
            main_answer = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

            if thinking_content:
                with st.expander("🧠 Thinking"):
                    st.markdown(thinking_content)

            st.markdown(main_answer)  # Display the cleaned AI response
            # Add to chat history in the correct format
            st.session_state.messages.append({"role": "assistant", "content": main_answer})

        except Exception as e:
            st.error(f"Error getting response: {str(e)}")

