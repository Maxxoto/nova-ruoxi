"""
title: Long Term Memory Filter
author:
date: 2024-08-23
version: 1.0
license: MIT
description: A filter that processes user messages and stores them as long term memory by utilizing the mem0 framework together with qdrant
requirements: pydantic==2.7.4,langfuse,mem0ai,langchain-groq,langchain_neo4j,rank_bm25
"""

import os
import threading
import logging
import json

from typing import List, Literal, Optional, Self
from pydantic import BaseModel, Field, model_validator
from langchain_groq import ChatGroq
from mem0 import Memory
from langfuse.callback import CallbackHandler


logger = logging.getLogger(__name__)

# TODO: ADD MEMORY RETRIEVAL ONLY WHEN FIRST MESSAGE IN CONVERSATION
# TODO: ADD MEMORY RETRIEVAL FROM INTENT BASED ON USER INPUT USING LLM AS JUDGE
# TODO: SEPARATE PIPELINE BETWEEN MEMORY RETRIEVAL AND MEMORY STORE

DEFAULT_FOLLOW_UP_GENERATION_PROMPT_TEMPLATE = "<chat_history>"


class Pipeline:
    class Valves(BaseModel):
        pipelines: List[str] = Field(default_factory=list, description="List of pipelines to connect to")
        priority: int = Field(default=0, ge=0, description="Priority of the filter")
        store_cycles: Optional[int] = Field(default=10, ge=1, description="Number of messages from the user before the data is processed and added to the memory")

        vector_store_qdrant_name: Optional[str] = Field(default="nova", min_length=1, description="Name of the Qdrant collection")
        vector_store_qdrant_url: Optional[str] = Field(default="host.docker.internal", min_length=1, description="URL for the Qdrant vector store")
        vector_store_qdrant_port: Optional[int] = Field(default=6333, ge=1, description="Port for the Qdrant vector store")
        API_KEY: Optional[str] = Field(default="", min_length=1, alias="API_KEY", description="API key for OpenAI or other services")
        groq_api_key: Optional[str] = Field(default="", description="API key for ChatGroq service")
        groq_model_name: Optional[str] = Field(default="llama-3.1-8b-instant", description="Model name for ChatGroq")
        use_llm_memory_judgment: bool = Field(default=False, description="Whether to use LLM for memory judgment")

        # Langfuse configuration
        langfuse_secret_key: Optional[str] = Field(default="", description="Langfuse secret key")
        langfuse_public_key: Optional[str] = Field(default="", description="Langfuse public key")
        langfuse_host: Optional[str] = Field(default="https://cloud.langfuse.com", description="Langfuse host URL")

        use_knowledge_graph: bool = Field(default=False, description="Use knowledge graph to store memories")
        if use_knowledge_graph:
            graph_url: Optional[str] = Field(default="", description="URL for the Neo4j graph database. Required if use_knowledge_graph is True and for Neo4j provider")
            graph_username: Optional[str] = Field(default="", description="Username for the Neo4j graph database. Required if use_knowledge_graph is True and for Neo4j provider")
            graph_password: Optional[str] = Field(default="", description="Password for the Neo4j graph database. Required if use_knowledge_graph is True and for Neo4j provider")

        force_user_id: Optional[str] = Field(default="", description="The user ID to force, if force_user is True")

        embedder_provider: Literal["openai", "ollama"] = Field(
            default="openai", description="Provider for the embedder, either 'openai' or 'ollama'. Ollama requires a local server to be running.", required=True
        )
        embedder_model: Optional[str] = Field(default="text-embedding-3-small", min_length=1, description="Model for the embedder")
        embedder_api_key: Optional[str] = Field(default="", description="API key for the embedder (e.g., OpenAI API key). Required if embedder_provider is 'openai'")
        embedder_dims: Optional[int] = Field(default=1536, ge=1, description="Embedding dimensions for the embedder model")

        @model_validator(mode="after")
        def check_graph_credentials(self) -> Self:
            if self.use_knowledge_graph:
                if not self.graph_url:
                    raise ValueError("WARN: graph_url is required when use_knowledge_graph is True")
                if not self.graph_username:
                    raise ValueError("WARN: graph_username is required when use_knowledge_graph is True")
                if not self.graph_password:
                    raise ValueError("WARN: graph_password is required when use_knowledge_graph is True")
            return self

    def __init__(self):
        self.type = "filter"
        self.name = "Memory Filter"
        self.user_messages = []
        self.thread = None
        self.groq_llm = None  # Initialize ChatGroq LLM
        self.langfuse = None  # Initialize Langfuse client

        self.mem_zero = None
        self.valves = self.Valves(
            **{
                "pipelines": ["*"],  # Connect to all pipelines
                "vector_store_qdrant_name": os.getenv("VECTOR_STORE_QDRANT_NAME", "nova"),
                "vector_store_qdrant_url": os.getenv("VECTOR_STORE_QDRANT_URL", "172.17.0.1"),
                "vector_store_qdrant_port": os.getenv("VECTOR_STORE_QDRANT_PORT", 6333),
                "API_KEY": os.getenv("API_KEY", "your-openai-api-key"),
                "store_cycles": os.getenv("STORE_CYCLES", 10),
                "graph_url": os.getenv("GRAPH_URL", ""),
                "graph_username": os.getenv("GRAPH_USERNAME", ""),
                "graph_password": os.getenv("GRAPH_PASSWORD", ""),
                "use_knowledge_graph": os.getenv("USE_KNOWLEDGE_GRAPH", "False").lower() == "true",
                "force_user_id": os.getenv("FORCE_USER_ID", ""),
                "embedder_provider": os.getenv("EMBEDDER_PROVIDER", "openai"),
                "embedder_model": os.getenv("EMBEDDER_MODEL", "text-embedding-3-small"),
                "embedder_api_key": os.getenv("EMBEDDER_API_KEY", ""),
                "embedder_dims": os.getenv("EMBEDDER_DIMS", 1536),
                "groq_api_key": os.getenv("GROQ_API_KEY", ""),
                "groq_model_name": os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant"),
                "use_llm_memory_judgment": os.getenv("USE_LLM_MEMORY_JUDGMENT", "False").lower() == "true",
                "langfuse_secret_key": os.getenv("LANGFUSE_SECRET_KEY", ""),
                "langfuse_public_key": os.getenv("LANGFUSE_PUBLIC_KEY", ""),
                "langfuse_host": os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            }
        )

    async def on_startup(self):
        logger.info(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        logger.info(f"on_shutdown:{__name__}")
        pass

    async def on_valves_updated(self):
        logger.info(f"on_valves_updated:{__name__}")
        if not self.mem_zero:
            self.mem_zero = self.init_mem_zero()

        if self.valves.use_llm_memory_judgment and not self.groq_llm:
            self.initialize_groq_llm()
        pass

    async def summarize_conversation(self, conversation_history: str) -> str:
        """Summarize conversation history using Groq LLM."""
        if not self.groq_llm:
            self.initialize_groq_llm()

        prompt = f"""
        Summarize this conversation history into key points while preserving important details.
        Focus on the user's main points and the assistant's responses.

        Conversation:
        {conversation_history}

        Summary:
        """
        try:
            response = await self.groq_llm.ainvoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error summarizing conversation: {e}")
            return conversation_history  # Fallback to original text if summarization fails

    async def _process_memory_storage(self, conversation_text: str, mem0_user: str) -> None:
        """Process and store summarized memory."""
        summarized_text = await self.summarize_conversation(conversation_text)

        if self.thread and self.thread.is_alive():
            logger.info("Waiting for previous memory to be done")
            self.thread.join()

        self.thread = threading.Thread(
            target=self.mem_zero.add,
            kwargs={"messages": summarized_text, "user_id": mem0_user, "agent_id": "ruo_agent"},
        )

        logger.info("Text to be processed into memory:")
        logger.info(f"{summarized_text[:30]}...{summarized_text[-30:]}")

        self.thread.start()

    async def _handle_llm_judgment(self, all_messages: List[dict], mem0_user: str) -> bool:
        """Handle LLM memory judgment flow."""
        full_conversation = " ".join([msg["content"] for msg in all_messages if isinstance(msg["content"], str)])
        try:
            judgment_prompt = f"""
            You are a helpful memory assistant.

            Your task is to decide whether this conversation should be saved as long-term memory.

            Answer with a single word: "yes" or "no".

            Save it if:
            - The user shares personal information (name, birthday, preferences, locations)
            - They express a long-term goal, plan, or decision
            - They give you instructions, corrections, or feedback
            - They explicitly say to remember or save

            Conversation:
            {full_conversation}

            Answer:
            """
            logger.info(f"Asking LLM for memory judgment: {judgment_prompt[:100]}...")
            llm_response = await self.groq_llm.ainvoke(judgment_prompt)
            response_content = llm_response.content.strip().lower()
            logger.info(f"LLM judgment response: {response_content}")

            if "yes" in response_content:
                await self._process_memory_storage(full_conversation, mem0_user)
                return True
            return False
        except Exception as e:
            logger.error(f"Error during LLM memory judgment: {e}")
            return False

    async def inlet(
        self,
        body: dict,
        user: Optional[dict] = None,
    ) -> dict:
        logger.info(f"Initiating memory calling... {__name__}")
        if self.valves.use_llm_memory_judgment and not self.groq_llm:
            self.initialize_groq_llm()

        store_cycles = self.valves.store_cycles

        logger.info(f"store_cycles: {store_cycles}")

        if self.valves.force_user_id != "":
            mem0_user = self.valves.force_user_id
        else:
            try:
                mem0_user = user.get("id")
            except (TypeError, KeyError):
                logger.info("Could not retrieve user ID. Using default user.")
                raise ValueError("User ID is not set")

        if self.valves.API_KEY == "":
            raise ValueError("API key is not set")

        if not self.mem_zero:
            self.mem_zero = self.init_mem_zero()

        logger.info(f"mem0_user: {mem0_user}")

        if isinstance(body, str):
            body = json.loads(body)

        all_messages = body["messages"]
        last_message = self.get_last_user_message(body["messages"])

        # If follow-up generation prompt is present, skip memory processing
        if DEFAULT_FOLLOW_UP_GENERATION_PROMPT_TEMPLATE in last_message:
            return body

        self.user_messages.append(last_message)

        # Filter out follow-up generation prompts before processing
        filtered_messages = [msg for msg in all_messages if isinstance(msg.get("content", ""), str) and DEFAULT_FOLLOW_UP_GENERATION_PROMPT_TEMPLATE not in msg["content"]]
        logger.info("========= FILTERED MESSAGES =========")
        logger.info(f"Filtered messages: {filtered_messages}")

        full_conversation = " ".join([msg["content"] for msg in filtered_messages])

        if self.valves.use_llm_memory_judgment:
            should_store = await self._handle_llm_judgment(filtered_messages, mem0_user)
            if not should_store:
                logger.info("LLM judgment decided not to store this conversation.")
        else:
            if len(self.user_messages) >= self.valves.store_cycles:
                await self._process_memory_storage(full_conversation, mem0_user)
                self.user_messages.clear()

        memories = self.mem_zero.search(last_message, user_id=mem0_user)

        if memories:
            fetched_memory = "\n".join(f"- {entry['memory']}" for entry in memories["results"])
        else:
            fetched_memory = ""

        if fetched_memory:
            logger.info("Memory added to the context")
            logger.info(fetched_memory[:10])
            all_messages.insert(
                0,
                {
                    "role": "system",
                    "content": "This is your inner voice talking, you remember this about the person you chatting with " + str(fetched_memory),
                },
            )

        return body

    def init_mem_zero(self):
        logger.info("Initializing Mem0")
        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": self.valves.vector_store_qdrant_name,
                    "host": self.valves.vector_store_qdrant_url,
                    "port": self.valves.vector_store_qdrant_port,
                    "embedding_model_dims": 1536,
                },
            },
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.2,
                    "max_tokens": 2000,
                    "api_key": self.valves.API_KEY,
                },
            },
            "embedder": {
                "provider": self.valves.embedder_provider,
                "config": {
                    "model": self.valves.embedder_model,
                    "api_key": self.valves.embedder_api_key if self.valves.embedder_provider == "openai" else "",
                    "embedding_dims": self.valves.embedder_dims,
                },
            },
        }

        if self.valves.use_knowledge_graph:
            config["graph_store"] = {
                "provider": "neo4j",
                "config": {
                    "url": self.valves.graph_url,
                    "username": self.valves.graph_username,
                    "password": self.valves.graph_password,
                },
            }

        return Memory.from_config(config)

    def get_last_user_message(self, messages: List[dict]) -> str:
        for message in reversed(messages):
            if message["role"] == "user":
                if isinstance(message["content"], list):
                    for item in message["content"]:
                        if item["type"] == "text":
                            return item["text"]
                return message["content"]
        return None

    def initialize_groq_llm(self):
        logger.info("Initializing ChatGroq LLM for memory judgment...")
        if not self.valves.groq_api_key:
            raise ValueError("Groq API key is not set for LLM memory judgment.")

        # Initialize Langfuse callback handler if credentials are provided
        langfuse_handler = None
        if self.valves.langfuse_secret_key:
            langfuse_handler = CallbackHandler(secret_key=self.valves.langfuse_secret_key, public_key=self.valves.langfuse_public_key, host=self.valves.langfuse_host)

        self.groq_llm = ChatGroq(temperature=0, model_name=self.valves.groq_model_name, groq_api_key=self.valves.groq_api_key, callbacks=[langfuse_handler] if langfuse_handler else None)
