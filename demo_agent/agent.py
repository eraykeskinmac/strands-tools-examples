#!/usr/bin/env python3
"""Demo Agent for Strands Tools Community.

This agent showcases the three community tools (Deepgram, HubSpot, Teams)
in an interactive REPL environment with hot-reload, session management,
beautiful console output, and Langfuse observability.

Usage:
    python agent.py                    # Interactive mode
    python agent.py "your query"       # Single query mode
    echo "query" | python agent.py     # Piped input
"""

import argparse
import base64
import datetime
import os
import socket
import sys
import time
from pathlib import Path

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    # Try to load .env from current directory
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment from: {env_path.absolute()}")
except ImportError:
    # dotenv not installed, try loading manually
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip().strip('"').strip("'")
                    os.environ[key.strip()] = value
        print(f"✅ Loaded environment from: {env_path.absolute()}")

from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.panel import Panel
from strands import Agent
from strands.session.file_session_manager import FileSessionManager

try:
    from strands.telemetry import StrandsTelemetry
    TELEMETRY_AVAILABLE = True
except ImportError:
    TELEMETRY_AVAILABLE = False

try:
    from strands_tools.utils.models.model import create_model
except ImportError:
    # Fallback - implement our own model creator
    def create_model(provider="bedrock"):
        """Create model based on provider.
        
        Supports:
        - bedrock (default)
        - anthropic (requires ANTHROPIC_API_KEY)
        - openai (requires OPENAI_API_KEY)
        """
        if provider == "anthropic":
            from strands.models.anthropic import AnthropicModel
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable required")
            return AnthropicModel(
                client_args={"api_key": api_key},
                model_id="claude-sonnet-4-20250514",
                max_tokens=4096,
                params={"temperature": 0.7}
            )
        elif provider == "openai":
            from strands.models.openai import OpenAIModel
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable required")
            return OpenAIModel(
                client_args={"api_key": api_key},
                model_id="gpt-4o",
                params={"max_tokens": 4096, "temperature": 0.7}
            )
        else:  # bedrock (default)
            from strands.models.bedrock import BedrockModel
            return BedrockModel(model_id="eu.anthropic.claude-sonnet-4-20250514-v1:0")

# Import callback handler
from handlers.callback_handler import callback_handler

# Import community tools
from strands_tools_community import deepgram, hubspot, teams

console = Console()

# Generate instance ID
hostname = socket.gethostname()
timestamp = str(int(time.time()))
instance_id = f"demo-agent-{hostname}-{timestamp[-6:]}"


def setup_otel() -> None:
    """Setup OpenTelemetry for Langfuse observability (optional)."""
    if not TELEMETRY_AVAILABLE:
        return
    
    otel_host = os.environ.get("LANGFUSE_HOST")

    if otel_host:
        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        secret_key = os.environ.get("LANGFUSE_SECRET_KEY", "")

        if public_key and secret_key:
            try:
                auth_token = base64.b64encode(
                    f"{public_key}:{secret_key}".encode()
                ).decode()
                otel_endpoint = f"{otel_host}/api/public/otel"

                os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = os.environ.get(
                    "OTEL_EXPORTER_OTLP_ENDPOINT", otel_endpoint
                )
                os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = os.environ.get(
                    "OTEL_EXPORTER_OTLP_HEADERS", f"Authorization=Basic {auth_token}"
                )

                strands_telemetry = StrandsTelemetry()
                strands_telemetry.setup_otlp_exporter()
            except Exception:
                # Silently fail if observability setup fails
                pass


def get_session_id() -> str:
    """Generate session ID based on current hour."""
    return f"demo-agent-{datetime.datetime.now().strftime('%Y-%m-%d-%H')}"


def get_history_file() -> str:
    """Get history file path."""
    history_path = Path.home() / ".strands_demo_agent_history"
    if not history_path.exists():
        history_path.touch(mode=0o600)
    return str(history_path)


def read_prompt_file() -> tuple[str, str]:
    """Read system prompt from .prompt file if it exists."""
    prompt_paths = [
        Path(".prompt"),
        Path("README.md"),
    ]
    for path in prompt_paths:
        if path.is_file():
            try:
                with open(path, encoding="utf-8") as f:
                    return f.read(), str(path)
            except Exception:
                continue
    return "", ""


def construct_system_prompt() -> str:
    """Construct the system prompt for the demo agent following Strands SDK v1.11.0 patterns."""
    # Try to load .prompt file first (research-agent pattern)
    prompt_content, prompt_file = read_prompt_file()
    
    if prompt_content:
        # Use .prompt file as primary source
        base_prompt = f"[Loaded system prompt from: {prompt_file}]\n\n{prompt_content}"
    else:
        # Fallback to inline prompt
        base_prompt = """You are a demo agent built with Strands Agents SDK v1.11.0, showcasing strands-tools-community capabilities.

Available Tools:
===============

1. **deepgram** - Speech & Audio Processing
   Actions:
   - transcribe: Convert audio to text with speaker diarization
   - text_to_speech: Generate speech from text
   - analyze: Audio intelligence (sentiment, topics, intents)
   
   Supported languages: en, es, fr, de, tr, and 30+ more
   Formats: WAV, MP3, M4A, FLAC, etc.

2. **hubspot** - CRM Data Access (Read-Only)
   Actions:
   - search: Find objects with advanced filters
   - get: Retrieve specific object by ID
   - list_properties: Discover available properties
   - get_user_details: Get user/owner information
   
   Object types: contacts, deals, companies, tickets, and more
   Note: Read-only access for data safety

3. **teams** - Microsoft Teams Notifications
   Templates:
   - notification: General notifications
   - approval: Approval requests with buttons
   - status: Project/system status updates
   - simple: Basic text messages
   
   Or use custom adaptive cards

Usage Patterns:
==============

**Transcription:**
- "transcribe this audio: recording.mp3"
- "transcribe https://example.com/call.mp3 in Turkish"
- "analyze sentiment in audio: call.wav"

**CRM Queries:**
- "search for contacts with email containing '@example.com'"
- "find all deals created this month"
- "get contact details for ID 12345"
- "search for companies in the technology industry"

**Team Notifications:**
- "send a Teams notification about new leads"
- "send an approval request to Teams for the Q4 budget"
- "send a status update: project is 75% complete"

**Combined Workflows:**
- "transcribe call.mp3, find the customer in HubSpot, and send summary to Teams"
- "search for this week's deals and send a Teams digest"
- "find contacts with missing data and generate audit report for Teams"

Response Style:
==============
- Be helpful and conversational
- Use the tools to accomplish tasks
- Provide clear confirmations
- Show results in a user-friendly format
- Ask for clarification if needed

Environment:
===========
- Current Directory: """ + str(Path.cwd()) + """
- Python Version: """ + sys.version.split()[0] + """
- Session ID: """ + get_session_id() + """
- Timestamp: """ + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """

Let's help the user explore and use these community tools!"""
    
    # Add runtime environment info
    runtime_info = f"""

## 🚀 Runtime Environment:
- **Hot-Reload**: Custom tools from ./tools/ directory auto-loaded
- **Session Persistence**: FileSessionManager active
- **Model Provider**: {os.getenv('MODEL_PROVIDER', 'bedrock')}
- **Observability**: OpenTelemetry/Langfuse ready

## 💡 Hot-Reload Tool Creation:
Save any .py file in ./tools/ and it becomes immediately available!

Example:
```python
# ./tools/my_tool.py
from strands import tool

@tool
def my_custom_tool(text: str) -> str:
    \"\"\"Your custom tool description.\"\"\"
    return f"Processed: {{text}}"
```
"""
    
    # Combine with environment variable override
    system_prompt_override = os.getenv("SYSTEM_PROMPT", "")
    
    return base_prompt + runtime_info + system_prompt_override


def create_agent(model_provider: str = "bedrock") -> Agent:
    """Create the demo agent with community tools.

    Args:
        model_provider: Model provider to use (default: bedrock)

    Returns:
        Configured Agent instance
    """
    # Setup observability
    setup_otel()

    # Create model
    model = create_model(provider=os.getenv("MODEL_PROVIDER", model_provider))

    # Create session manager
    session_id = get_session_id()
    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=Path.cwd() / "sessions"
    )

    # Create agent with community tools
    agent = Agent(
        model=model,
        tools=[deepgram, hubspot, teams],
        system_prompt=construct_system_prompt(),
        callback_handler=callback_handler,
        load_tools_from_directory=True,  # Enable hot-reload from ./tools/
        session_manager=session_manager,
        trace_attributes={
            "session.id": instance_id,
            "user.id": os.getenv("USER", "demo-user"),
            "tags": ["strands-tools-community", "demo-agent"],
        },
    )

    return agent


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="demo-agent",
        description="Interactive demo agent for Strands Tools Community",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent.py                              # Interactive mode
  python agent.py "transcribe audio.mp3"       # Single query
  echo "search contacts" | python agent.py     # Piped input
        """,
    )

    parser.add_argument(
        "query",
        nargs="*",
        help="Query to ask the agent (if provided, runs once and exits)",
    )

    return parser.parse_args()


def display_welcome():
    """Display welcome message."""
    welcome_text = """
[bold cyan]Strands Tools Community - Demo Agent[/bold cyan]

Available Tools:
  🎤 [bold]deepgram[/bold]  - Speech-to-text, text-to-speech, audio analysis
  🏢 [bold]hubspot[/bold]   - CRM operations (contacts, deals, companies)
  📢 [bold]teams[/bold]     - Microsoft Teams notifications

[yellow]Tip:[/yellow] Tools in ./tools/ directory will be hot-reloaded automatically

Type your query or try:
  • "transcribe audio: recording.mp3"
  • "search for contacts in HubSpot"
  • "send a Teams notification"
  • "help" for more information

Type 'exit', 'quit', or 'bye' to quit, or press Ctrl+C
"""
    console.print(Panel(welcome_text, expand=False))


def main():
    """Main entry point for the demo agent."""
    args = parse_args()

    # Display welcome message
    if not args.query and sys.stdin.isatty():
        display_welcome()

    # Create agent
    try:
        agent = create_agent()
    except Exception as e:
        console.print(f"[red]Failed to create agent: {e}[/red]")
        return 1

    # Handle different input modes
    tasks = []

    # Priority 1: Piped input
    if not sys.stdin.isatty():
        try:
            pipe_task = sys.stdin.read().strip()
            if pipe_task:
                tasks.append(pipe_task)
        except Exception:
            pass

    # Priority 2: Command line arguments
    if args.query:
        cmd_task = " ".join(args.query)
        if cmd_task:
            tasks.append(cmd_task)

    # Execute collected tasks
    if tasks:
        for i, task in enumerate(tasks, 1):
            if len(tasks) > 1:
                console.print(f"\n[bold]Task {i}/{len(tasks)}:[/bold] {task}")
            
            try:
                result = agent(task)
                # Result is already printed by callback handler
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue

        return 0

    # Interactive mode
    history_file = get_history_file()
    history = FileHistory(history_file)

    while True:
        try:
            # Get user input
            query = prompt(
                "\n# ",
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
                mouse_support=False,
            )

            # Handle special commands
            if query.lower() in ["exit", "quit", "bye"]:
                console.print("\n👋 [bold]Goodbye![/bold]")
                break

            if not query.strip():
                continue

            if query.lower() == "help":
                console.print("""
[bold cyan]Available Commands:[/bold cyan]

[bold]Deepgram (Speech & Audio):[/bold]
  • transcribe audio: <file_or_url> [in <language>]
  • convert text to speech: <text>
  • analyze audio: <file_or_url>

[bold]HubSpot (CRM):[/bold]
  • search for <object_type> with <criteria>
  • create a <object_type> with <properties>
  • get <object_type> <id>
  • update <object_type> <id> with <properties>
  • list properties for <object_type>

[bold]Teams (Notifications):[/bold]
  • send Teams notification: <message>
  • send approval request to Teams
  • send status update to Teams

[bold]Special Commands:[/bold]
  • help    - Show this help message
  • exit    - Exit the agent
  • quit    - Exit the agent
  • bye     - Exit the agent

[yellow]Tip:[/yellow] You can combine multiple operations in natural language!
""")
                continue

            # Execute query
            try:
                result = agent(query)
                # Result is already printed by callback handler
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue

        except KeyboardInterrupt:
            console.print("\n\n[yellow]Interrupted[/yellow]\n")
            break
        except EOFError:
            console.print("\n👋 [bold]Goodbye![/bold]")
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())

