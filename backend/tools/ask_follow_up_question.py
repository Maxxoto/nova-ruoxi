import json
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, AnyMessage
from backend.utils.logger_config import logger
from backend.tools.summarize_chat import summarize_chat_factory


def ask_follow_up_question_factory(agent):
    @tool
    def ask_follow_up_question(messages: list[AnyMessage]):
        """_summary_
            This tool is used to ask follow up question if you feel that the previous question was not answered properly.
        Args:
            messages (list[AnyMessage]): The list of chat messages to ask follow up question.
        Returns:
            A follow up question based on the chat history.
        """
        follow_up_agent_chain = agent
        summarize_chat_tool = summarize_chat_factory(agent)

        logger.info("\n=== ASK_FOLLOW_UP_QUESTION TOOL CALLED ===")
        logger.info(f"{len(messages)} messages to ask follow up question")
        for i, msg in enumerate(messages):
            logger.debug(f"{i + 1}. [{msg.type}] {msg.content[:50]}...")

        # First, summarize the chat history using invoke() instead of __call__
        summary_result = summarize_chat_tool.invoke(messages)
        summary_data = json.loads(summary_result)
        chat_summary = summary_data.get("summary", "No summary available.")

        processed_chat_history = []
        for msg in messages:
            if hasattr(msg, "type") and hasattr(msg, "content"):
                processed_chat_history.append({"type": msg.type, "content": msg.content})
            else:
                logger.warning(f"Invalid message format - {msg}")

        prompt = f"""
            Based on the chat history and its summary, please ask a follow up question if you feel that the previous question was not answered properly.

            Chat Summary:
            {chat_summary}

            Chat History:
            {json.dumps([str(msg) for msg in processed_chat_history], indent=2)}
        """

        response = follow_up_agent_chain.invoke([SystemMessage(content=prompt)])

        follow_up_question = ""
        if isinstance(response, dict) and "messages" in response:
            last_message = response["messages"][-1] if response["messages"] else None
            follow_up_question = last_message.content if hasattr(last_message, "content") else str(last_message)
        else:
            follow_up_question = str(response)

        return json.dumps({"action": "ask_follow_up_question", "question": follow_up_question})

    return ask_follow_up_question
