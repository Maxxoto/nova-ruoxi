"""
title: Qwen No-Think Simple Toggle
author:
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 1.0
description: If self.toggle is True in the code, prepends /no-think to the system prompt. Otherwise, makes no changes related to /no-think.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Callable, Awaitable
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set to info for more verbose output
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = True


class Filter:
    """
    A simple filter that, if its internal `self.toggle` is True,
    prepends '/no-think' to the system prompt.
    If `self.toggle` is False, it makes no changes to the prompt.
    This toggle is set in the code and not via UI Valves.
    """

    class Valves(BaseModel):
        priority: int = 2
        pass  # No user-configurable valves as per the requested structure

    def __init__(self):
        logger.info("✅ QwenToggle filter is loaded!")
        self.valves = self.Valves()

        # This is the "toggle" state for the filter's action.
        # Set to True: remove "/no-think".
        # Set to False: the filter does nothing regarding /no-think.
        # To change the behavior, modify this line and restart Open WebUI.
        self.toggle: bool = True

        self.icon = """data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9Im5vbmUiIHZpZXdCb3g9IjAgMCAyNCAyNCIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZT0iY3VycmVudENvbG9yIiBjbGFzcz0ic2l6ZS02Ij4KICA8cGF0aCBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGQ9Ik0xMiAxOHYtNS4yNW0wIDBhNi4wMSA2LjAxIDAgMCAwIDEuNS0uMTg5bS0xLjUuMTg5YTYuMDEgNi4wMSAwIDAgMS0xLjUtLjE4OW0zLjc1IDcuNDc4YTEyLjA2IDEyLjA2IDAgMCAxLTQuNSAwbTMuNzUgMi4zODNhMTQuNDA2IDE0LjQwNiAwIDAgMS0zIDBNMTQuMjUgMTh2LS4xOTJjMC0uOTgzLjY1OC0xLjgyMyAxLjUwOC0yLjMxNmE3LjUgNy41IDAgMSAwLTcuNTE3IDBjLjg1LjQ5MyAxLjUwOSAxLjMzMyAxLjUwOSAyLjMxNlYxOCIgLz4KPC9zdmc+Cg=="""

        active_action_for_log = (
            "removes /no-think" if self.toggle else "filter inactive, no changes made"
        )
        logger.info(
            f"Qwen Think Simple Toggle filter initialized. Default behavior: {active_action_for_log} (based on self.toggle = {self.toggle})"
        )

    async def inlet(
        self,
        body: Dict[str, Any],
        __event_emitter__: Callable[[Dict[str, Any]], Awaitable[None]],
        __user__: Optional[Dict[str, Any]] = None,
        __model__: Optional[Dict[str, Any]] = None,
        __request__: Optional[Any] = None,
    ) -> Dict[str, Any]:

        messages: List[Dict[str, str]] = body.get("messages", [])
        if not messages:
            logger.warning("No messages found in body, skipping modification.")
            return body

        # removes it /no_think everywhere
        if self.toggle:
            logger.info(
                "✅ self.toggle is True -> removing /no_think to the last user message"
            )
            # remove /no_think
            for i in range(len(messages)):
                if messages[i].get("role") == "user":
                    content = messages[i].get("content", "")
                    new_content = content.replace("/no_think", "")
                    messages[i]["content"] = new_content
            body["messages"] = messages

        return body

    async def outlet(
        self,
        body: Dict[str, Any],
        __event_emitter__: Callable[[Dict[str, Any]], Awaitable[None]],
        __user__: Optional[Dict[str, Any]] = None,
        __model__: Optional[Dict[str, Any]] = None,
        __request__: Optional[Any] = None,
    ) -> Dict[str, Any]:
        logger.info("Qwen No-Think Simple Toggle outlet called, passing through.")
        return body

