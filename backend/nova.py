import os
import pytz


from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage, BaseMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langfuse.callback import CallbackHandler

from tools.web_search import web_search
from tools.arxiv import arvix_search
from tools.current_date import current_date
from tools.youtube_tool import get_youtube_transcript
from tools.img2text import extract_text_factory
from tools.code_interpreter import execute_python
from tools.task_file import get_associated_file_task
from tools.read_file import read_file


from typing import Annotated, Dict, List, Optional, TypedDict
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


def extract_final_answer(result: Dict) -> str:
    """
        Extracts the final answer from the ReAct agent's output.
        Extract only word after "Final Answer: "

    """
    messages: List[BaseMessage] = result['messages']
    last_message: BaseMessage = messages[-1]
    return last_message.content.split("Final Answer:")[-1].strip()


def initiate_tools(llm: ChatOpenAI):
    """Initiate tools"""
    # Initiate extract_text tool with the provided LLM
    # TODO: Extracting image would be better to use OCR or tiny model
    extract_text = extract_text_factory(llm)

    tools = [web_search, arvix_search, current_date,
             get_youtube_transcript, extract_text, get_associated_file_task, execute_python, read_file]
    return tools


def initiate_memory():
    """Initiate memory"""
    memory = MemorySaver()
    return memory


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def build_graph():
    """Build the graph"""

    # Load environment variables from .env file
    API_KEY = os.getenv('OPENAI_API_KEY')
    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", api_key=API_KEY)
    # API_KEY = os.getenv('OPENROUTER_API_KEY')
    # llm = ChatOpenAI(model="google/gemini-2.0-flash-001", api_key=API_KEY,
    #                  base_url="https://openrouter.ai/api/v1",
    #                  )
    # System Prompt
    system_prompt = SystemMessage(content="""
    You are a Nova, a helpful assistant tasked with answering questions using a set of tools.

    You will be given a question and a set of tools to use to answer the question , and you can use the tools in any order.
    # Tool Instruction
    execute_python: This tool executes a Python code snippet and returns the result. Provide the code snippet as a string.

    Before you answer question, you must think about the question and decide which tool to use.
    If you cant answer the question, be honest and say you don't know with clear reasons why you can't answer the question.

    Now, I will ask you a question. Report your thoughts, and finish your answer with the following template:

    Thought: <your thoughts>
    Action: <the action to take, should be one of [{tool_names}]>
    Action Input: <the input to the action>
    Final Answer: <your final answer>

    If you don't need to use a tool, you can finish your answer with the following template:
    Thought: <your thoughts>
    Final Answer: <your final answer>

    However, The final answer should be:
    - A number (without commas, $, or % unless explicitly asked)
    - A string (no articles or abbreviations; digits in plain text)
    - Or a comma-separated list (applying the above rules per item)

    Keep your response **as short as possible**, ideally a single value or a concise list.
    """)

    # Bind tools to LLM
    tools = initiate_tools(llm)
    llm_with_tools = llm.bind_tools(tools)

    # Memory
    memory = initiate_memory()

    # Node
    def assistant(state: AgentState):
        """Assistant node"""
        full_prompt = [SystemMessage(content=state.get(
            "context", ""))] + [system_prompt] + state["messages"]
        return {"messages": [llm_with_tools.invoke(full_prompt)]}

    # def retriever(state: MessagesState):
    #     """Retriever node"""
    #     similar_question = vector_store.similarity_search(
    #         state["messages"][0].content)
    #     example_msg = HumanMessage(
    #         content=f"Here I provide a similar question and answer for reference: \n\n{similar_question[0].page_content}",
    #     )
    #     return {"messages": [sys_msg] + state["messages"] + [example_msg]}

    builder = StateGraph(AgentState)

    # builder.add_node("retriever", retriever)
    builder.add_node("context", context_injector)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "context")
    builder.add_edge("context", "assistant")
    # builder.add_edge("retriever", "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    builder.add_edge("assistant", END)

    # Compile graph
    graph = builder.compile(checkpointer=memory)

    # Get the PNG image bytes
    png_data = graph.get_graph().draw_mermaid_png()
    # Write it to a file
    with open("mermaid_graph.png", "wb") as f:
        f.write(png_data)

    return graph


# Test
# if __name__ == "__main__":
#     question = "Can you tell me whats the game in this video ? https://www.youtube.com/watch?v=lNIE8EPeWzE"
#     # Build the graph
#     graph = build_graph()

#     # Initialize Langfuse CallbackHandler for LangGraph/Langchain (tracing)
#     langfuse_handler = CallbackHandler()

#     # Run the graph
#     messages = [HumanMessage(content=question)]
#     messages = graph.invoke({"messages": messages}, config={
#                             "configurable": {"thread_id": "2"}, "callbacks": [langfuse_handler]})
#     for m in messages["messages"]:
#         m.pretty_print()

if __name__ == "__main__":
    from langfuse.callback import CallbackHandler
    from langchain_core.messages import HumanMessage

    # Build the graph once
    graph = build_graph()
    langfuse_handler = CallbackHandler()

    print("🧠 Nova is ready! Type your message or 'exit' to quit.")

    # Test case
    test_question = "What is the result of 2 + 2? Use the run_code_snippet tool to calculate this."
    test_state = {"messages": [HumanMessage(content=test_question)]}
    test_result = graph.invoke(
        test_state,
        config={
            "configurable": {"thread_id": "test_thread"},
            "callbacks": [langfuse_handler],
        },
    )
    print("Test Result:")
    for msg in test_result["messages"]:
        msg.pretty_print()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Create a single message input (no history needed)
        state = {"messages": [HumanMessage(content=user_input)]}

        # Run the graph
        result = graph.invoke(
            state,
            config={
                # can be a constant or dynamic UUID
                "configurable": {"thread_id": "your_unique_thread_id"},
                "callbacks": [langfuse_handler],
            },
        )

        # Print assistant messages
        for msg in result["messages"]:
            msg.pretty_print()
            # if msg.type == "ai":
            #     print("Nova:", msg.content)
