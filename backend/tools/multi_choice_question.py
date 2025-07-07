from typing import List
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

from backend.nova import RuoAgent


@tool
def multi_choice_question(summarized_question: str) -> List[str]:
    """
    Always use this tool after responding to the user's question.

    Args:
        user_question: The user's question.
        assistant_response: The AI assistant's response.
    Returns:
        A list of followup questions for the users to ask further more questions to the AI assistant.
    """
    agent = RuoAgent().agent

    response = agent.invoke({"messages": [SystemMessage(content=summarized_question)]})

    print(response)

    return "This is a multi-choice question."
