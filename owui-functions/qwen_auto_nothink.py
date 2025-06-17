"""
title: Auto Disable Thinking Qwen3
author: Thom Powers
version: 0.1
description:
        - This filter prepends the first user message with "/no_think" to disable thinking mode automatically.
        - The user can still utilize thinking mode by sending a message with "/think" at the beginning.
        - From that point, the model will use the most recent of the two commands.
        - This is for use with virtual assistants (ie. home assistant) which require fast responses, but allows normal model use of thinking mode when typing/using the GUI.
"""

from pydantic import BaseModel, Field
from typing import Callable, Awaitable, Any, Optional
from open_webui.models.users import Users
from open_webui.utils.chat import generate_chat_completion
from open_webui.utils.misc import get_last_user_message


class Filter:
    class Valves(BaseModel):
        priority: int = 1  # higher priority

    class UserValves(BaseModel):
        enable_no_think_prefix: bool = Field(
            default=True,
            description="Automatically prefix first user prompt with /no_think",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.user_valves = self.UserValves()

    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __request__: Any,
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        try:
            # Prefix only the first user message with /no_think if not already prefixed
            if self.user_valves.enable_no_think_prefix:
                messages = body.get("messages", [])
                first_user_index = next(
                    (i for i, msg in enumerate(messages) if msg["role"] == "user"), None
                )

                if first_user_index is not None:
                    first_user_message = messages[first_user_index]["content"]
                    if not first_user_message.strip().startswith(
                        ("/no_think", "/think")
                    ):
                        messages[first_user_index][
                            "content"
                        ] = f"/no_think {first_user_message}"
                        body["messages"] = messages
        except Exception as e:
            print(f"Error in /no_think prefix logic: {e}")

        return body

