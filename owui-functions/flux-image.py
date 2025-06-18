"""
title: Replicate.ai Image Gen
description: Generate images with Replicate.
author: Maxxoto
author_url:
version: 1.1.1
license: MIT
"""

from typing import (
    Literal,
)
import requests
import os
import json
from pydantic import BaseModel, Field


ImageAspectRatioType = Literal[
    "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16", "9:21"
]


class Tools:
    class Valves(BaseModel):
        REPLICATE_API_TOKEN: str = Field(
            default="", description="Your Replicate API token"
        )

    def __init__(self):
        self.valves = self.Valves(
            REPLICATE_API_TOKEN=os.getenv("REPLICATE_API_TOKEN", ""),
        )

    async def generate_image(
        self,
        image_prompt: str,
        image_aspect_ratio: ImageAspectRatioType,
        __event_emitter__=None,
    ) -> str:
        """
        Generate an image given a prompt

        Whenever a description of an image is given, use this tool to create the image from a prompt.
        You do not need to ask for permission to generate, just do it!
        DO NOT write out the prompt before OR after generating the images. The prompt should ONLY ever be written out ONCE, in the `"image_prompt"` field of the request.

        The image_prompt sent to this tool must abide by the following policies:
        1. The prompt should be in English. If the image description was not in English, then translate it.
        2. Always mention the image type (photo, oil painting, watercolor painting, illustration, cartoon, drawing, vector, render, etc.) in the beginning of the prompt. Unless the description suggests otherwise.
        3. The prompt must intricately describe every part of the image in concrete, objective detail. THINK about what the end goal of the description is, and extrapolate that to what would make satisfying images.
        4. The prompt should be a paragraph of text that is extremely descriptive and detailed. It should be more than 3 sentences long.
        5. If the user requested modifications to a previous image, the prompt should not simply be longer, but rather it should be refactored to integrate the suggestions.

        The image_aspect_ratio should be selected by picking the most suitable one for the image.
        - If the user suggests or implies an aspect ratio, then use that, or the closest valid one.
        - "3:4" should be used for upper body shots and similar.
        - "2:3" should be used for full body portraits and similar.
        - "21:9" for panoramas or ultra wide images.
        - "16:9" is otherwise the default recommended aspect ratio.

        :param image_prompt: Text prompt for image generation.
        :param image_aspect_ratio: Aspect ratio for the generated image.
        """

        try:
            # I don't know why, but emitting the event twice is required for it to appear in the UI.
            for _ in range(2):
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": "Generating image ...", "done": False},
                    }
                )

            replicate_api_token = self.valves.REPLICATE_API_TOKEN
            if not replicate_api_token:
                raise ValueError("REPLICATE_API_TOKEN is not set")

            image = generate_image_with_replicate_flux_pro_ultra(
                replicate_api_token,
                image_prompt,
                image_aspect_ratio,
            )

            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": "Generated image:", "done": True},
                }
            )

            await __event_emitter__(
                {
                    "type": "message",
                    "data": {
                        "content": f"![{image_prompt}]({image})  \n**Aspect Ratio:** `{image_aspect_ratio}`  **Prompt:** `{image_prompt}`  \n"
                    },
                }
            )

            # This aims to work around an LLM "temporal confusion" problem.
            # It gets confused when we invisibly speak on it's behalf.
            return f"""
The image generation completed successfully!

Note that the generated image ALREADY HAS been automatically sent and displayed to the user by the tool.
You don't need to do anything to show the image to the user.

When you answer now - simply tell the user the image was successfully generated.
Answer with text only, NO IMAGES, NO ASPECT RATIO, NO IMAGE PROMPT.
Just tell the user that the image was successfully generated.

At the end of your answer you might ask the user if they want anything changed to the image.
Should they later come back and ask for changes - just generate a new image with potentially modified parameters based on their feedback.

Keep your answer short and concise.
"""

        except Exception as e:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"An error occurred: {e}", "done": True},
                }
            )

            return f"Tell the user: {e}"


def generate_image_with_replicate_flux_pro_ultra(
    replicate_api_token: str,
    prompt: str,
    aspect_ratio: ImageAspectRatioType,
) -> str:
    url = "https://api.replicate.com/v1/predictions"

    headers = {
        "Authorization": f"Bearer {replicate_api_token}",
        "Content-Type": "application/json",
        "Prefer": "wait",
    }

    payload = {
        "version": "xlabs-ai/flux-dev-realism:39b3434f194f87a900d1bc2b6d4b983e90f0dde1d5022c27b52c143d670758fa",
        "input": {
            "raw": False,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "guidance": 5.0,
            "output_format": "jpg",
            "num_outputs": 1,
            "lora_strength": 1.0,
            "output_format": "jpg",
            "output_quality": 100,
            "num_inference_steps": 30,
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    response_json = response.json()
    remote_image_url = response_json.get("output", [])

    return remote_image_url[0]
