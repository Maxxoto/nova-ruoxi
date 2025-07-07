import json
from typing import Any
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, AnyMessage


def summarize_chat_factory(agent):
    @tool
    def summarize_chat(messages: list[AnyMessage]) -> str:
        """
        This tool is used to summarize the chat history.

        Args:
            messages: The list of chat messages to summarize.
        Returns:
            A concise summarized version of the chat history.
        """
        summarizer_agent_chain = agent

        print("\n=== SUMMARIZE_CHAT TOOL CALLED ===")
        print(f"Received {len(messages)} messages to summarize:")
        for i, msg in enumerate(messages):
            print(f"{i + 1}. [{msg.type}] {msg.content[:50]}...")

        processed_chat_history = []
        for msg in messages:
            if hasattr(msg, "type") and hasattr(msg, "content"):
                processed_chat_history.append({"type": msg.type, "content": msg.content})
            else:
                print(f"Warning: Invalid message format - {msg}")

        prompt = f"""
            Based on the chat history, please summarize the chat history in a concise way.
            The chat history contains messages from Human and AI.

            Chat history:
            {json.dumps([str(msg) for msg in processed_chat_history], indent=2)}
        """

        response = summarizer_agent_chain.invoke([SystemMessage(content=prompt)])

        summary_text = ""
        if isinstance(response, dict) and "messages" in response:
            last_message = response["messages"][-1] if response["messages"] else None
            summary_text = last_message.content if hasattr(last_message, "content") else str(last_message)
        else:
            summary_text = str(response)

        return json.dumps({"action": "summarize_and_clear", "summary": summary_text})

    return summarize_chat
