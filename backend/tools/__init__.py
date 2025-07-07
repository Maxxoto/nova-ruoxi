from backend.tools import ask_follow_up_question, summarize_chat


def initiate_tools(agent, langfuse_handler=None):
    """Initiate tools

    Args:
        agent: The agent to use for tool execution
        langfuse_handler: Optional Langfuse callback handler for tracing
    """
    summarize_chat_tool = summarize_chat.summarize_chat_factory(agent)
    follow_up_tool = ask_follow_up_question.ask_follow_up_question_factory(agent)

    tools = [summarize_chat_tool, follow_up_tool]
    return tools
