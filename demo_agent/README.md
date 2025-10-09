# Demo Agent - Strands Tools Community Showcase

Interactive agent demonstrating Deepgram, HubSpot, and Microsoft Teams integrations.

## Features

- 🎯 **Research-Agent Pattern** - Follows Strands SDK v1.11.0 best practices
- 📄 **`.prompt` File** - Customizable system prompt (edit `.prompt` to change behavior)
- ✨ **Interactive REPL** with command history and auto-suggestions
- 🔄 **Hot-reload tools** from `./tools/` directory
- 💾 **Session persistence** with FileSessionManager
- 🎨 **Beautiful console output** with Rich library and Halo spinners
- 📝 **Natural language interface** - just describe what you want
- 🎯 **Three modes**: Interactive, single query, or piped input
- 🔭 **OpenTelemetry/Langfuse** observability support

## Quick Start

### 1. Installation

```bash
# From the demo_agent directory
pip install -r ../requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp ../.env.example .env

# Edit .env with your API keys
nano .env
```

Required API keys:

**Model Provider** (choose one):

- **Anthropic** (recommended for non-AWS users): Get from [console.anthropic.com](https://console.anthropic.com/)
  ```bash
  MODEL_PROVIDER=anthropic
  ANTHROPIC_API_KEY=your_key
  ```
- **OpenAI**: Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
  ```bash
  MODEL_PROVIDER=openai
  OPENAI_API_KEY=your_key
  ```
- **AWS Bedrock** (requires AWS account): Configure via `aws sso login`
  ```bash
  MODEL_PROVIDER=bedrock
  AWS_PROFILE=your_profile
  ```

**Community Tools**:

- **DEEPGRAM_API_KEY**: Get from [console.deepgram.com](https://console.deepgram.com/)
- **HUBSPOT_API_KEY**: Get from [app.hubspot.com/private-apps](https://app.hubspot.com/private-apps)
- **TEAMS_WEBHOOK_URL**: Create in Teams Channel → Connectors → Incoming Webhook

### 3. Run

```bash
# Interactive mode (default)
python agent.py

# Single query mode
python agent.py "transcribe audio: recording.mp3"

# Piped input mode
echo "search for contacts in HubSpot" | python agent.py
```

## Usage Examples

### Deepgram - Speech Processing

```
# Transcribe audio
# transcribe audio: path/to/recording.mp3

# Transcribe with language
# transcribe https://example.com/call.mp3 in Turkish

# Text-to-speech
# convert this text to speech: Hello, welcome to our platform

# Audio analysis
# analyze sentiment and topics in audio: call.wav
```

### HubSpot - CRM Operations

```
# Search contacts
# search for contacts with email containing '@example.com'

# Create a deal
# create a deal called 'Acme Corp Q4' with amount 50000

# Get object details
# get contact details for ID 12345

# Update records
# update company 67890 with industry set to Technology

# List available properties
# list all properties for deals
```

### Microsoft Teams - Notifications

```
# Simple notification
# send a Teams notification: New lead from Acme Corp

# Approval request
# send an approval request to Teams for Q4 budget of $25,000

# Status update
# send a status update to Teams: Website redesign is 75% complete

# Custom message
# send a Teams message with title "Daily Digest" and summary of today's activities
```

### Combined Workflows

```
# End-to-end call processing
# transcribe call.mp3, find the caller in HubSpot by phone, create a call activity, and send summary to Teams

# Daily digest
# search for all deals closed today in HubSpot and send a formatted digest to Teams

# Lead qualification
# search for leads created in the last 24 hours and send a notification to Teams with details
```

## Special Commands

- `help` - Show help message with examples
- `exit`, `quit`, `bye` - Exit the agent
- `Ctrl+C` - Interrupt current operation

## Hot-Reload Tools

Create custom tools in the `./tools/` directory and they'll be automatically loaded:

```python
# ./tools/my_custom_tool.py
from strands import tool

@tool
def my_tool(param: str) -> str:
    \"\"\"My custom tool description.

    Args:
        param: Parameter description
    \"\"\"
    return f"Result: {param}"
```

The tool will be immediately available in the agent without restart!

## Session Management

- Sessions are saved hourly in `./sessions/` directory
- Session ID format: `demo-agent-YYYY-MM-DD-HH`
- History is preserved between invocations
- Sessions include conversation context and tool results

## Console Output

The agent provides beautiful console output:

- 🔧 **Tool Calls**: Blue panels showing tool invocations
- ✅ **Success**: Green indicators for successful operations
- ❌ **Errors**: Red indicators with helpful error messages
- 💬 **Agent Responses**: Green panels with agent messages
- 📊 **Tables**: Rich formatted tables for search results

## Troubleshooting

### API Key Issues

```bash
# Check if environment variables are loaded
echo $DEEPGRAM_API_KEY
echo $HUBSPOT_API_KEY
echo $TEAMS_WEBHOOK_URL
```

### Model Provider Issues

```bash
# For Bedrock (AWS)
aws sso login
export AWS_PROFILE=your_profile

# For other providers
export MODEL_PROVIDER=anthropic  # or openai, etc.
```

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r ../requirements.txt
```

## Environment Variables

```bash
# Required
DEEPGRAM_API_KEY=xxx
HUBSPOT_API_KEY=xxx
TEAMS_WEBHOOK_URL=xxx

# Optional
MODEL_PROVIDER=bedrock
DEEPGRAM_DEFAULT_MODEL=nova-3
DEEPGRAM_DEFAULT_LANGUAGE=en
HUBSPOT_DEFAULT_LIMIT=100

# Observability (optional)
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=xxx
LANGFUSE_SECRET_KEY=xxx
```

## Architecture

```
demo_agent/
├── agent.py                 # Main agent script
├── handlers/
│   ├── __init__.py
│   └── callback_handler.py  # Rich console output handler
├── tools/                   # Hot-reload tools directory
│   └── .gitkeep
├── sessions/                # Session storage (auto-created)
└── README.md               # This file
```

## Tips

1. **Start Simple**: Try basic queries first, then combine operations
2. **Use Natural Language**: The agent understands conversational queries
3. **Check Help**: Type `help` for command examples
4. **Explore Tools**: Try different combinations of the three tools
5. **Hot-Reload**: Add custom tools in `./tools/` for extended functionality
6. **History**: Use up/down arrows to navigate command history
7. **Sessions**: Sessions are automatically saved and restored

## Next Steps

- Explore the [main documentation](../../)
- Check out other [example scripts](../)
- Read about individual tools:
  - [Deepgram](../../deepgram.md)
  - [HubSpot](../../hubspot.md)
  - [Teams](../../teams.md)

## Support

For issues or questions:

- GitHub Issues: [strands-agents/tools-community/issues](https://github.com/strands-agents/tools-community/issues)
- Documentation: [docs/](../../)

---

**Happy exploring! 🚀**
