"""
title: Long Term Memory Filter
author:
date: 2024-08-23
version: 1.0
license: MIT
description: A filter that processes user messages and stores them as long term memory by utilizing the mem0 framework together with qdrant
requirements: pydantic,mem0ai
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
        store_cycles: Optional[int] = (
            10  # Number of messages from the user before the data is processed and added to the memory
        )

        vector_store_qdrant_name: Optional[str] = "nova"
        vector_store_qdrant_url: Optional[str] = "host.docker.internal"
        vector_store_qdrant_port: Optional[int] = 6333
        API_KEY: Optional[str] = ""  # API key

    def __init__(self):
        self.type = "filter"
        self.name = "Memory Filter"
        self.user_messages = []
        self.thread = None

        self.mem_zero = None
        self.valves = self.Valves(
            **{
                "pipelines": ["*"],  # Connect to all pipelines
                "vector_store_qdrant_name": os.getenv(
                    "VECTOR_STORE_QDRANT_NAME", "memories"
                ),
                "vector_store_qdrant_url": os.getenv(
                    "VECTOR_STORE_QDRANT_URL", "172.17.0.1"
                ),
                "vector_store_qdrant_port": os.getenv("VECTOR_STORE_QDRANT_PORT", 6333),
                "API_KEY": os.getenv("API_KEY", "your-openai-api-key"),
                "store_cycles": os.getenv("STORE_CYCLES", 10),
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
        if self.mem_zero:
            self.mem_zero = None  # Reset the memory to force reinitialization
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

        try:
            mem0_user = user.get("id")
        except (TypeError, KeyError):
            logger.info("Could not retrieve user ID. Using default user.")
            raise ValueError("User ID is not set")

        if self.valves.API_KEY == "":
            raise ValueError("API key is not set")

        if self.mem_zero is None:
            self.mem_zero = self.init_mem_zero()

        logger.info(f"mem0_user: {mem0_user}")

        if isinstance(body, str):
            body = json.loads(body)

        all_messages = body["messages"]
        last_message = all_messages[-1]["content"]

        self.user_messages.append(last_message)

        # user_messages = [msg for msg in all_messages if msg["role"] == "user"]

        if len(self.user_messages) == store_cycles:
            message_text = ""
            for message in self.user_messages:
                message_text += message + " "

            if self.thread and self.thread.is_alive():
                logger.info("Waiting for previous memory to be done")
                self.thread.join()

            self.thread = threading.Thread(
                target=self.mem_zero.add,
                kwargs={"data": message_text, "user_id": mem0_user},
            )

            logger.info("Text to be processed in to a memory:")
            logger.info(message_text)

            self.thread.start()
            self.user_messages.clear()

        memories = self.mem_zero.search(last_message, user_id=mem0_user)

        if memories:
            fetched_memory = "\n".join(
                f"- {entry['memory']}" for entry in memories["results"]
            )
        else:
            fetched_memory = ""

        logger.info("Memory added to the context")
        logger.info(fetched_memory[:10])

        if fetched_memory:
            all_messages.insert(
                0,
                {
                    "role": "system",
                    "content": "This is your inner voice talking, you remember this about the person you chatting with "
                    + str(fetched_memory),
                },
            )

        logger.info("Final body to send to the LLM:")
        # logger.info(body)

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
                    "embedding_model_dims": 3072,  # Default dimension for text-embedding-3-large
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
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-large",
                    "api_key": self.valves.API_KEY,
                    "embedding_dims": 3072,
                },
            },
        }

        return Memory.from_config(config)
