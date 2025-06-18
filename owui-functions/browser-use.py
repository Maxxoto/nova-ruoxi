"""
title: Browser Agent Pipe
author: 
version: 0.1.0
requirements: playwright,langchain-openai,browser-use
Visit https://github.com/open-webui/open-webui/discussions/10384 for error installing browser-use
"""
from typing import Optional, Callable, Awaitable, List, Dict
from pydantic import BaseModel, Field
import os
import asyncio
import time
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI

@dataclass
class ActionResult:
    is_done: bool
    extracted_content: Optional[str]
    error: Optional[str]
    include_in_memory: bool

@dataclass
class AgentHistoryList:
    all_results: List[ActionResult]
    all_model_outputs: List[Dict]

class Pipe:
    class Valves(BaseModel):
        openai_api_key: str = Field(
            default="",
            description="OpenAI API key for the browser agent",
        )
        model: str = Field(
            default="deepseek/deepseek-r1-0528",
            description="Model to use (e.g., 'deepseek/deepseek-r1-0528', 'gpt-4.1')",
        )
        headless: bool = Field(
            default=True,
            description="Run browser in headless mode",
        )
        emit_interval: float = Field(
            default=2.0,
            description="Interval between status updates in seconds",
        )
        enable_status_indicator: bool = Field(
            default=True,
            description="Enable status indicator",
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "browser_agent"
        self.name = "Browser Agent"
        self.valves = self.Valves()
        self.last_emit_time = 0
        self.current_task: Optional[asyncio.Task] = None

    async def emit_status(
        self,
        emitter: Callable[[dict], Awaitable[None]],
        level: str,
        message: str,
        done: bool,
    ):
        current_time = time.time()
        if (
            emitter
            and self.valves.enable_status_indicator
            and (
                current_time - self.last_emit_time >= self.valves.emit_interval or done
            )
        ):
            await emitter(
                {
                    "type": "status",
                    "data": {
                        "status": "complete" if done else "in_progress",
                        "level": level,
                        "description": message,
                        "done": done,
                    },
                }
            )
            self.last_emit_time = current_time

    async def run_browser_task(self, task: str) -> str:
        """Execute task in background with error handling"""
        if not self.valves.openai_api_key.strip():
            return "❌ Error: OpenAI API key required"
        os.environ["OPENAI_API_KEY"] = self.valves.openai_api_key
        try:
            browser = Browser(
                config=BrowserConfig(
                    headless=False,
                )
            )
            agent = Agent(
                task=task,
                llm=ChatGoogleGenerativeAI(
                    model=self.valves.model, api_key=self.valves.openai_api_key
                ),  # ChatOpenAI(model=self.valves.model),
                browser=browser,
            )
            return await agent.run()
            await browser.close()
        except Exception as e:
            return f"❌ Critical error: {str(e)}"

    def _parse_results(self, result) -> str:
        parsed = []
        process_steps = []
        final_result = None
        # Debug: Print result type
        print(f"Received result type: {type(result)}")
        if isinstance(result, AgentHistoryList):
            print(f"Number of actions in history: {len(result.all_results)}")
            for i, action_result in enumerate(result.all_results, 1):
                # Debug: Print action metadata
                print(f"Action {i}:")
                print(f"Done: {action_result.is_done}")
                print(
                    f"Content: {action_result.extracted_content[:50] if action_result.extracted_content else None}"
                )
                print(f"Error: {action_result.error}")
                # Capture final result
                if action_result.is_done:
                    final_result = action_result.extracted_content
                    print(f"Final result detected in action {i}")
                # Build process steps
                step_content = []
                if action_result.extracted_content:
                    step_content.append(
                        f"**Step {i}:** {action_result.extracted_content}"
                    )
                if action_result.error and action_result.error != "None":
                    step_content.append(f"❌ _Error: {action_result.error}_")
                if step_content:
                    process_steps.append("\n".join(step_content))
        # Fallback for string representation
        else:
            str_result = str(result)
            print("Result in string format:")
            print(str_result[:500])  # First 500 characters for debug
            sections = str_result.split("ActionResult(")
            for i, section in enumerate(sections[1:], 1):
                # Extract done status
                is_done = "is_done=True" in section
                content = error = None
                if "extracted_content=" in section:
                    content = (
                        section.split("extracted_content=")[1].split(",")[0].strip("'")
                    )
                if "error=" in section:
                    error = section.split("error=")[1].split(",")[0].strip("'")
                if is_done:
                    final_result = content
                    print(f"Final result detected in action {i} (string fallback)")
                step_content = []
                if content:
                    step_content.append(f"**Step {i}:** {content}")
                if error and error != "None":
                    step_content.append(f"❌ _Error: {error}_")
                if step_content:
                    process_steps.append("\n".join(step_content))
        # Build final response
        output = []
        if final_result:
            output.append(f"## 🔍 Final Result\n\n{final_result}")
        if process_steps:
            output.append(
                "\n\n## 📋 Process Details\n\n" + "\n\n".join(process_steps)
            )
        return (
            "\n\n".join(output)
            if output
            else "✅ Task completed with no visible results"
        )

    async def pipe(
        self,
        body: dict,
        user: Optional[dict] = None,
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
        __event_call__: Callable[[dict], Awaitable[dict]] = None,
    ) -> Optional[dict]:
        messages = body.get("messages", [])
        if not messages:
            error = "No messages found"
            await self.emit_status(__event_emitter__, "error", error, True)
            body["messages"].append({"role": "assistant", "content": error})
            return body
        try:
            user_message = messages[-1]["content"]
            # Debug: Process start
            print(f"\n{'='*50}\nStarting task with message: {user_message}")
            print(f"Model: {self.valves.model}")
            print(
                f"API Key: {'configured' if self.valves.openai_api_key else 'missing'}"
            )
            await self.emit_status(
                __event_emitter__,
                "info",
                "🚀 Starting browser...",
                False,
            )
            self.current_task = asyncio.create_task(self.run_browser_task(user_message))
            raw_result = await self.current_task
            # Debug: Raw result
            print("\nRaw result received:")
            print(f"Type: {type(raw_result)}")
            print(f"Content: {str(raw_result)[:500]}...")  # First 500 characters
            parsed_result = self._parse_results(raw_result)
            # Debug: Parsed result
            print("\nParsed result:")
            print(parsed_result[:1000])  # First 1000 characters
            formatted_output = f"{parsed_result}"
            await self.emit_status(
                __event_emitter__, "success", "🏁 Task completed", True
            )
            body["messages"].append({"role": "assistant", "content": formatted_output})
            return formatted_output
        except Exception as e:
            error = f"## ❌ Pipe error\n\n{str(e)}"
            print(f"\nError in pipe: {str(e)}")
            await self.emit_status(__event_emitter__, "error", error, True)
            body["messages"].append({"role": "assistant", "content": error})
            return body
        finally:
            self.current_task = None
