"""Callback handler for beautiful console output in the demo agent.

This module provides rich console output for tool calls, streaming events,
and agent responses, following the research-agent pattern with halo spinners.
"""

import time
from typing import Any

from colorama import Fore, Style, init
from halo import Halo
from rich.console import Console

# Initialize colorama
init(autoreset=True)

# Configure spinner
SPINNERS = {
    "dots": {
        "interval": 80,
        "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    }
}

# Tool state colors
TOOL_COLORS = {
    "running": Fore.GREEN,
    "success": Fore.GREEN,
    "error": Fore.RED,
    "info": Fore.CYAN,
}


class ToolSpinner:
    """Spinner for tool execution with status updates."""

    def __init__(self, text: str = "", color: str = TOOL_COLORS["running"]):
        self.spinner = Halo(
            text=text,
            spinner=SPINNERS["dots"],
            color="green",
            text_color="green",
            interval=80,
        )
        self.color = color
        self.current_text = text

    def start(self, text: str = None):
        if text:
            self.current_text = text
        print()  # Move to new line
        self.spinner.start(f"{self.color}{self.current_text}{Style.RESET_ALL}")

    def update(self, text: str):
        self.current_text = text
        self.spinner.text = f"{self.color}{text}{Style.RESET_ALL}"

    def succeed(self, text: str = None):
        if text:
            self.current_text = text
        self.spinner.succeed(
            f"{TOOL_COLORS['success']}{self.current_text}{Style.RESET_ALL}"
        )

    def fail(self, text: str = None):
        if text:
            self.current_text = text
        self.spinner.fail(f"{TOOL_COLORS['error']}{self.current_text}{Style.RESET_ALL}")

    def info(self, text: str = None):
        if text:
            self.current_text = text
        self.spinner.info(f"{TOOL_COLORS['info']}{self.current_text}{Style.RESET_ALL}")

    def stop(self):
        self.spinner.stop()


class CallbackHandler:
    """Callback handler matching research-agent pattern."""

    def __init__(self):
        self.console = Console()
        self.thinking_spinner = None
        self.current_spinner = None
        self.current_tool = None
        self.tool_histories = {}

    def callback_handler(self, **kwargs: Any) -> None:
        """Main callback handler following research-agent pattern."""
        data = kwargs.get("data", "")
        complete = kwargs.get("complete", False)
        message = kwargs.get("message", {})
        current_tool_use = kwargs.get("current_tool_use", {})

        # Handle regular output
        if data:
            if complete:
                print(f"{Fore.WHITE}{data}{Style.RESET_ALL}")
            else:
                print(f"{Fore.WHITE}{data}{Style.RESET_ALL}", end="")

        # Handle tool input streaming
        if current_tool_use and current_tool_use.get("input"):
            tool_id = current_tool_use.get("toolUseId")
            tool_name = current_tool_use.get("name")
            tool_input = current_tool_use.get("input", "")

            # Check if this is a new tool execution
            if tool_id != self.current_tool:
                # Stop previous spinner if exists
                if self.current_spinner:
                    self.current_spinner.stop()

                self.current_tool = tool_id

                self.current_spinner = ToolSpinner(
                    f"🛠️  {tool_name}: Preparing...", TOOL_COLORS["running"]
                )
                self.current_spinner.start()

                # Record tool start
                self.tool_histories[tool_id] = {
                    "name": tool_name,
                    "start_time": time.time(),
                    "input_size": 0,
                }

            # Update tool progress
            if tool_id in self.tool_histories:
                current_size = len(tool_input)
                if current_size > self.tool_histories[tool_id]["input_size"]:
                    self.tool_histories[tool_id]["input_size"] = current_size
                    if self.current_spinner:
                        self.current_spinner.update(
                            f"🛠️  {tool_name}: {current_size} chars"
                        )

        # Process messages
        if isinstance(message, dict):
            # Handle assistant messages (tool starts)
            if message.get("role") == "assistant":
                for content in message.get("content", []):
                    if isinstance(content, dict):
                        tool_use = content.get("toolUse")
                        if tool_use:
                            tool_name = tool_use.get("name")
                            if self.current_spinner:
                                self.current_spinner.info(f"🔧 Starting {tool_name}...")

            # Handle user messages (tool results)
            elif message.get("role") == "user":
                for content in message.get("content", []):
                    if isinstance(content, dict):
                        tool_result = content.get("toolResult")
                        if tool_result:
                            tool_id = tool_result.get("toolUseId")
                            status = tool_result.get("status")

                            if tool_id in self.tool_histories:
                                tool_info = self.tool_histories[tool_id]
                                duration = round(
                                    time.time() - tool_info["start_time"], 2
                                )

                                # Prepare message
                                if status == "success":
                                    msg = f"{tool_info['name']} completed in {duration}s"
                                else:
                                    msg = f"{tool_info['name']} failed after {duration}s"

                                # Update spinner
                                if self.current_spinner:
                                    if status == "success":
                                        self.current_spinner.succeed(msg)
                                    else:
                                        self.current_spinner.fail(msg)

                                # Cleanup
                                del self.tool_histories[tool_id]
                                self.current_spinner = None
                                self.current_tool = None


# Create global instance
callback_handler_instance = CallbackHandler()
callback_handler = callback_handler_instance.callback_handler

