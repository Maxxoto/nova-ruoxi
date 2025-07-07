from typing import Any, List, Dict
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage


def format_response(response_obj: Any) -> str:
    """
    Formats an agent's response object into a readable string for the UI.

    Args:
        response_obj (Any): The response object received from the agent.
                            Can be a dict (from graph.invoke), a BaseMessage, or a string.

    Returns:
        str: A formatted string for display in the UI.
    """
    if isinstance(response_obj, dict) and "messages" in response_obj:
        if response_obj["messages"]:
            # Get content from the last message in the list
            return str(response_obj["messages"][-1].content)
        else:
            return ""  # No messages in the response dict
    elif hasattr(response_obj, "content"):  # BaseMessage or similar
        return str(response_obj.content)
    elif isinstance(response_obj, str):  # Direct string response
        return response_obj
    elif response_obj is None:
        return ""
    else:
        # Fallback for unexpected types, try to convert to string
        return str(response_obj)


def format_chat_history_for_display(messages: List[AnyMessage]) -> List[Dict[str, str]]:
    """
    Formats a list of LangChain messages into a display-friendly list of dictionaries.

    Args:
        messages (List[AnyMessage]): A list of LangChain message objects (e.g., HumanMessage, AIMessage).

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each with 'content' and 'type' keys.
                              Example: [{"content": "Hello", "type": "human"}, ...]
    """
    formatted_messages = []
    for msg in messages:
        msg_role = ""
        if isinstance(msg, HumanMessage):
            msg_role = "user"  # Streamlit uses 'user' for Human messages
        elif isinstance(msg, AIMessage):
            msg_role = "assistant"  # Streamlit uses 'assistant' for AI messages
        elif isinstance(msg, SystemMessage):
            msg_role = "assistant"  # System messages can be displayed as assistant messages
        elif isinstance(msg, ToolMessage):
            msg_role = "assistant"  # Tool messages can be displayed as assistant messages
        else:
            msg_role = "assistant"  # Fallback for other message types, assume assistant (or 'unknown' if desired)

        formatted_messages.append({"content": str(msg.content), "role": msg_role})
    return formatted_messages
