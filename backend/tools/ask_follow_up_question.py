import json
from typing import List
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, AnyMessage
from backend.utils.logger_config import logger

from backend.tools.summarize_chat import summarize_chat_factory


class MessagesInput(BaseModel):
    messages: List[AnyMessage] = Field(..., description="List of chat messages to evaluate")


def ask_follow_up_question_factory(agent):
    @tool()
    def ask_follow_up_question(messages: List[AnyMessage]) -> str:
        """
        This tool is used to ask a follow-up question instead answering the user query.

        Args:
            messages: The list of chat messages to summarize.
         Returns:
            A concise follow-up question based on the user query.
        """
        logger.info("ASK_FOLLOW_UP_QUESTION tool called with %d messages", len(messages))
        for i, msg in enumerate(messages, 1):
            logger.debug("%d. [%s] %.50s", i, getattr(msg, "type", "?"), getattr(msg, "content", "")[:50])

        processed_chat_history = []
        for msg in messages:
            if hasattr(msg, "type") and hasattr(msg, "content"):
                processed_chat_history.append({"type": msg.type, "content": msg.content})
            else:
                logger.warning(f"Invalid message format - {msg}")

        # Summarize chat history
        summarize_tool = summarize_chat_factory(agent, False)
        summary_result = summarize_tool.invoke({"messages": messages})
        summary = json.loads(summary_result).get("summary", "")

        # Create prompt
        prompt = f"""
            You are a helpful assistant. Based on the following chat history, ask a follow-up question to the user.
            Chat history: {summary}
            Follow-up question:
        """
        logger.debug("Prompt: %s", prompt)

        # Query agent
        response = agent.invoke([SystemMessage(content=prompt)])
        # Parse last AI message
        if hasattr(response, "messages"):
            follow_up = next((m.content for m in reversed(response.messages) if hasattr(m, "content")), "")
        else:
            follow_up = str(response)

        return json.dumps({"action": "ask_follow_up_question", "question": follow_up})

    return ask_follow_up_question
