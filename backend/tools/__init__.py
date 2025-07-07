# from tools.web_search import web_search
# from tools.arxiv import arvix_search
# from tools.current_date import current_date
# from tools.youtube_tool import get_youtube_transcript
# from tools.img2text import extract_text_factory
# from tools.code_interpreter import execute_python
# from tools.task_file import get_associated_file_task
# from tools.read_file import read_file


from backend.tools import summarize_chat


def initiate_tools(agent, langfuse_handler=None):
    """Initiate tools

    Args:
        agent: The agent to use for tool execution
        langfuse_handler: Optional Langfuse callback handler for tracing
    """
    summarize_chat_tool = summarize_chat.summarize_chat_factory(agent)

    tools = [summarize_chat_tool]
    return tools


#     extract_text = extract_text_factory(llm)

#     tools = [web_search, arvix_search, current_date,
#              get_youtube_transcript, extract_text, get_associated_file_task, execute_python, read_file]
#     return tools
