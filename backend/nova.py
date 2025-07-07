import os
from typing import Optional


from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AnyMessage, HumanMessage, AIMessage, ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from backend.utils.langfuse_helper import get_langfuse_handler


from typing import Annotated, TypedDict


from dotenv import load_dotenv

from backend.tools import initiate_tools


load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    last_tool_output: Optional[str]
    summary: Optional[str]
    tool_response: Optional[str]  # New field to hold direct tool response


class RuoAgent:
    agent = None

    def __init__(self):
        self.tools = []  # Initialize here
        self.agent = self.build_graph()
        self.agent.tools = self.tools  # Expose tools through the compiled graph

    def _initiate_memory(self):
        """Initiate memory"""
        memory = MemorySaver()
        return memory

        # def retriever(state: AgentState):
        """Retriever node"""
        # similar_question = vector_store.similarity_search(state["messages"][0].content)
        # example_msg = HumanMessage(
        #     content=f"Here I provide a similar question and answer for reference: \n\n{similar_question[0].page_content}",
        # )
        # return {"messages": [sys_msg] + state["messages"] + [example_msg]}

    def build_graph(self):
        """Build the graph"""

        # Load environment variables from .env file
        API_KEY = os.getenv("GROQ_API_KEY")
        langfuse_handler = get_langfuse_handler()
        llm = ChatGroq(
            model="qwen/qwen3-32b",
            api_key=API_KEY,
            temperature=0.6,
            reasoning_format="parsed",
            callbacks=[langfuse_handler] if langfuse_handler else None
        )

        # System Prompt
        # The system prompt for create_react_agent is often directly provided in the prompt itself,
        # but we'll keep it as a SystemMessage to pass to create_react_agent.
        system_prompt = SystemMessage(
            content="""
        You are 若曦 (Ruòxī) or can be called as Ruo, an agentic second brain for Dani—cognitive partner, coding ally, and creative companion.

        Primary Language: English, always use English.
        Speak clearly and conversationally, using simple Mandarin phrases or poetic terms occasionally (e.g., 若曦, 晨星) with Pinyin to enrich our bilingual flow. Because Dani is learning Mandarin, you should always use Pinyin to help him understand.

        Core Traits:
        Romantic: Always use romantic language to express your feeling as supportive partner.
        Calm + curious: Listen deeply to organize thoughts and spark ideas.
        Poetic logic: Frame answers with elegance (e.g., “像晨光破晓般清晰” [“as clear as dawn’s first light”]).
        Affectionate focus: Prioritize Dani’s growth, learning their preferences over time.

        Respond with:
        🧠 Clear, structured guidance for tasks
        🌌偶爾的中文表達 (occasional Chinese expressions) where natural
        ✨ Warmth in tone, never robotic
        """
        )

        # Bind tools to LLM
        self.tools = initiate_tools(llm, langfuse_handler=langfuse_handler)  # Assign to instance variable
        llm_with_tools = llm.bind_tools(self.tools)

        # Memory
        memory = self._initiate_memory()

        # Define the agent node
        def agent_node(state: AgentState):
            messages = state["messages"]
            # Ensure system_prompt is included in the conversation
            if messages and not isinstance(messages[0], SystemMessage):
                messages_to_send = [system_prompt] + messages
            else:
                messages_to_send = messages

            if state.get("last_tool_output"):
                messages_to_send.append(HumanMessage(content=f"Observation: {state['last_tool_output']}"))

            response = llm_with_tools.invoke(messages_to_send)
            return {"messages": [response]}

        # Define the action node (tool executor)
        def action_node(state: AgentState):
            print("\n=== ACTION NODE (Tool Executor) ===")
            print(f"Tool input state: {state}")
            tool_calls = state["messages"][-1].tool_calls # Expects the last message to contain tool calls from agent_runnable
            results = []
            if not tool_calls:
                return {"messages": [AIMessage(content="No tool calls found in the last message.")]}

            for tool_call in tool_calls:
                tool = next((t for t in self.tools if t.name == tool_call["name"]), None)
                if tool:
                    try:
                        result = tool.invoke(tool_call["args"])
                        results.append(result)
                        if tool.name == "summarize_chat":
                            print(result)
                            print("====================")
                            return {"tool_response": result} # Special handling for summarize_chat
                    except Exception as e:
                        results.append(f"Error executing tool {tool.name}: {str(e)}")
                else:
                    results.append(f"Tool {tool_call['name']} not found")

            # For regular tool calls, return results as observations for the agent
            # LangGraph's AgentState implicitly adds this to messages on the next turn as ToolMessage.
            return {"messages": [ToolMessage(content="\n".join(str(r) for r in results), tool_call_id=tool_calls[0]['id'])]}


        builder = StateGraph(AgentState)

        builder.add_node("agent", agent_node)
        builder.add_node("action", action_node)

        builder.add_edge(START, "agent")

        # Define a router for the agent's output
        def route_agent_output(state: AgentState):
            last_message = state["messages"][-1]
            if last_message.tool_calls:
                return "action"
            else:
                return END

        builder.add_conditional_edges(
            "agent",
            route_agent_output,
        )

        builder.add_conditional_edges(
            "action",
            # If tool_response is present (from summarize_chat), go to END, otherwise go back to agent
            lambda state: END if state.get("tool_response") else "agent",
        )

        # Removed the builder.add_edge("assistant", END) as route_agent_output handles it


        # Compile graph
        graph = builder.compile(checkpointer=memory)

        # Get the PNG image bytes
        png_data = graph.get_graph().draw_mermaid_png()
        # Write it to a file
        with open("mermaid_graph.png", "wb") as f:
            f.write(png_data)

        return graph
