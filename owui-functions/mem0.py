"""
title: Long Term Memory Filter
author:
date: 2024-08-23
version: 1.0
license: MIT
description: A filter that processes user messages and stores them as long term memory by utilizing the mem0 framework together with qdrant
requirements: pydantic==2.7.4,mem0ai,langchain_neo4j,rank_bm25
"""

import os
from typing import List, Optional
from pydantic import BaseModel
import json
from mem0 import Memory
import threading
import logging

logger = logging.getLogger(__name__)


class Pipeline:
    class Valves(BaseModel):
        pipelines: List[str] = []
        priority: int = 0
        # Number of messages from the user before the data is processed and added to the memory
        store_cycles: Optional[int] = 10

        vector_store_qdrant_name: Optional[str] = "nova"
        vector_store_qdrant_url: Optional[str] = "host.docker.internal"
        vector_store_qdrant_port: Optional[int] = 6333
        API_KEY: Optional[str] = ""  # API key

        use_knowledge_graph: Optional[bool] = False
        graph_url: Optional[str] = ""
        graph_username: Optional[str] = ""
        graph_password: Optional[str] = ""

        force_user: Optional[bool] = False
        force_user_id: Optional[str] = ""
        embedder_provider: Optional[str] = "openai"
        embedder_model: Optional[str] = "text-embedding-3-small"
        embedder_api_key: Optional[str] = ""
        embedder_dims: Optional[int] = 1536

    def __init__(self):
        self.type = "filter"
        self.name = "Memory Filter"
        self.user_messages = []
        self.thread = None

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
                "force_user": os.getenv("FORCE_USER", "False").lower() == "true",
                "force_user_id": os.getenv("FORCE_USER_ID", ""),
                "embedder_provider": os.getenv("EMBEDDER_PROVIDER", "openai"),
                "embedder_model": os.getenv("EMBEDDER_MODEL", "text-embedding-3-small"),
                "embedder_api_key": os.getenv("EMBEDDER_API_KEY", ""),
                "embedder_dims": os.getenv("EMBEDDER_DIMS", 1536),
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
        pass

    async def inlet(
        self,
        body: dict,
        user: Optional[dict] = None,
    ) -> dict:
        logger.info(f"Initiating memory calling... {__name__}")

        store_cycles = self.valves.store_cycles

        logger.info(f"store_cycles: {store_cycles}")

        if self.valves.force_user:
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
        last_message = all_messages[-1]["content"]

        # Check if last_message contain </chat_history> if yes then dont append it to the user_messages
        if "</chat_history>" not in last_message:
            # Handle for followup question (new openwebui features)
            self.user_messages.append(last_message)

        logger.info(f"Current messages length : {len(self.user_messages)}")
        logger.info(f"Last message : {last_message[:30]}...{last_message[-30:]}")

        if len(self.user_messages) == store_cycles:
            message_text = ""
            for message in self.user_messages:
                message_text += message + " "

            if self.thread and self.thread.is_alive():
                logger.info("Waiting for previous memory to be done")
                self.thread.join()

            self.thread = threading.Thread(
                target=self.mem_zero.add,
                kwargs={"messages": message_text, "user_id": mem0_user},
            )

            logger.info("Text to be processed in to a memory:")
            logger.info(f"{message_text[:30]}...{message_text[-30:]}")

            self.thread.start()
            self.user_messages.clear()

        memories = self.mem_zero.search(last_message, user_id=mem0_user)

        if memories:
            fetched_memory = "\n".join(f"- {entry['memory']}" for entry in memories["results"])
        else:
            fetched_memory = ""

        logger.info("Memory added to the context")
        logger.info(fetched_memory[:10])

        if fetched_memory:
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
