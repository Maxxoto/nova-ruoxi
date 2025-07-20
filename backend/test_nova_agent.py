import os
import dotenv
import sys
from pathlib import Path
import asyncio

# Add project root to path to enable backend imports
sys.path.append(str(Path(__file__).parent.parent))

from langchain_core.messages import HumanMessage
from backend.nova import RuoAgent
import asyncio


THREAD_ID = "test_thread"
CHECKPOINT_NS = "test_ns"
CHECKPOINT_ID = "test_id"

dotenv.load_dotenv()


async def main():
    llm = RuoAgent()

    # Example conversation turns
    messages = [
        HumanMessage(content="Hey Nova, I have a quick question."),
        HumanMessage(content="What's the tallest mountain in the world?"),
        HumanMessage(content="How tall is it?"),  # ← follow-up
        HumanMessage(content="And how does it compare to Mount Kilimanjaro?"),  # ← deeper follow-up
        HumanMessage(content="Switching topics—can you tell me about Ada Lovelace?"),  # ← new topic
        HumanMessage(content="What did she invent?"),  # ← follow-up on Ada
        HumanMessage(content="Summarize what we've talked about so far. (use summarize tools)"),  # ← summarize request
    ]

    conversation_history = []
    for message in messages:
        print(f"User: {message.content}")
        conversation_history.append(message)
        response = await llm.agent.ainvoke({"messages": message}, config={"configurable": {"thread_id": "default_thread"}})

        print(f"Ruo: {response['messages'][-1].content if response['messages'] else 'No messages'}")

        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())
