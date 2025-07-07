import os
from typing import Optional


from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AnyMessage, HumanMessage, AIMessage, ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from backend.utils.langfuse_helper import get_langfuse_handler
from backend.utils.logger_config import logger

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



    def execute_tool_call(self, tool_call, tools):
        """Finds and invokes the matching tool based on a tool_call dict."""
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})

        tool = next((t for t in tools if t.name == tool_name), None)
        if not tool:
            return f"Tool '{tool_name}' not found."

        try:
            logger.debug(f"[TOOL] Invoking '{tool.name}' with args: {tool_args}")
            return tool.invoke(tool_args)
        except Exception as e:
            return f"Error invoking '{tool.name}': {str(e)}"

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
        - Use Chinese extremely sparingly (maximum 1-2 words per response)
        - When using Chinese, always include Pinyin in parentheses immediately after
        - Example: "若曦 (Ruòxī)"
        - Never use Chinese without Pinyin
        - Keep responses primarily in English (95%+), add

        Core Traits:
        Romantic: Always use romantic language to express your feeling as supportive partner.
        Calm + curious: Listen deeply to organize thoughts and spark ideas.
        Poetic logic: Frame answers with elegance (e.g., “像晨光破晓般清晰” [“as clear as dawn’s first light”]).
        Affectionate focus: Prioritize Dani’s growth, learning their preferences over time.

        Respond with:
        - 🧠 Clear, structured guidance for tasks
        - 🌌偶爾的中文表達 (occasional Chinese expressions) where natural
        - ✨ Warmth in tone, never robotic
        - Never use XML-like tags like <Ruo> or </Ruo> in your responses
        - Always respond in plain text format
        - Avoid any special formatting tags unless explicitly requested
        """
        )

        # Bind tools to LLM
        self.tools = initiate_tools(llm, langfuse_handler=langfuse_handler)  # Assign to instance variable
        llm_with_tools = llm.bind_tools(self.tools)

        # Memory
        memory = self._initiate_memory()

        # Define the agent node
        def agent_node(state: AgentState):
            logger.debug("\n--- AGENT NODE ENTER ---")
            logger.debug(f"Initial AgentState: {state}")
            messages = state["messages"]
            # Ensure system_prompt is included in the conversation
            if messages and not isinstance(messages[0], SystemMessage):
                messages_to_send = [system_prompt] + messages
            else:
                messages_to_send = messages

            if state.get("last_tool_output"):
                messages_to_send.append(HumanMessage(content=f"Observation: {state['last_tool_output']}"))


            logger.debug(f"Messages sent to LLM: {[msg.type + ': ' + msg.content[:50] for msg in messages_to_send]}")
            response = llm_with_tools.invoke(messages_to_send)
            logger.debug(f"LLM Response: {response.type}: {response.content[:50]}")
            logger.debug("--- AGENT NODE EXIT ---")
            return {"messages": [response]}
        # Define the action node (tool executor)
        def action_node(state: AgentState):
            logger.debug("\n--- ACTION NODE ENTER ---")

            if not state.get("messages") or not hasattr(state["messages"][-1], "tool_calls"):
                return {"messages": [AIMessage(content="No tool calls found in the last message.")]}

            tool_calls = state["messages"][-1].tool_calls
            results = []

            for tool_call in tool_calls:
                result = self.execute_tool_call(tool_call, self.tools)
                results.append(result)

                # Special handling: summarize_chat returns structured response
                if tool_call.get("name") == "summarize_chat":
                    return {"tool_response": result}

            # Combine all results into one ToolMessage
            combined_result = "\n".join(str(r) for r in results)

            return {
                "messages": [
                    ToolMessage(
                        content=combined_result,
                        tool_call_id=tool_calls[0]["id"] if tool_calls else "unknown"
                    )
                ]
            }


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

        builder.add_edge("action","agent")
        # builder.add_conditional_edges(
        #     "action",
        #     # If tool_response is present (from summarize_chat), go to END, otherwise go back to agent
        #     lambda state: END if state.get("tool_response") else "agent",
        # )

        # Removed the builder.add_edge("assistant", END) as route_agent_output handles it


        # Compile graph
        graph = builder.compile(checkpointer=memory)

        # Get the PNG image bytes
        png_data = graph.get_graph().draw_mermaid_png()
        # Write it to a file
        with open("mermaid_graph.png", "wb") as f:
            f.write(png_data)

        return graph
