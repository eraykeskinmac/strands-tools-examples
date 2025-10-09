# Strands Tools Community - Examples

Real-world examples and interactive demo showcasing [strands-tools-community](https://github.com/eraykeskinmac/strands-tools-community) in action.

## 🚀 What's Included

### 📱 Interactive Demo Agent

A fully-featured interactive demo agent with:

- ✨ REPL interface with command history
- 🔄 Hot-reload tools from directory
- 💾 Session persistence
- 🎨 Beautiful console output
- 📝 Natural language interface

**[→ Try the Demo Agent](./demo_agent/)**

### 📝 Example Scripts

Real-world automation examples:

- **`call_analytics.py`** - End-to-end call processing workflow
  - Transcribe audio → Search CRM → Create activity → Send notification
- **`crm_automation.py`** - Automated HubSpot workflows
  - Daily lead digest, pipeline reports, contact enrichment
- **`team_notifications.py`** - Microsoft Teams integration patterns
  - Notifications, approvals, status updates, custom cards

## 📦 Quick Start

### 1. Install Package

```bash
# Install from PyPI
pip install strands-tools-community

# Install Strands with your preferred model provider
pip install 'strands-agents[anthropic]'  # Recommended
# OR
pip install 'strands-agents[openai]'
# OR
pip install 'strands-agents[bedrock]'
```

### 2. Set Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit with your API keys
nano .env
```

Required API keys:

- **DEEPGRAM_API_KEY** - Get at [console.deepgram.com](https://console.deepgram.com/)
- **HUBSPOT_API_KEY** - Get at [app.hubspot.com/private-apps](https://app.hubspot.com/private-apps)
- **TEAMS_WEBHOOK_URL** - Setup in Teams Channel → Connectors
- **ANTHROPIC_API_KEY** - Get at [console.anthropic.com](https://console.anthropic.com/)

### 3. Run Examples

```bash
# Interactive demo
cd demo_agent
python agent.py

# Or run example scripts
python call_analytics.py recording.mp3 +1234567890
python crm_automation.py --workflow daily-leads
python team_notifications.py --type notification --title "Test" --message "Hello"
```

## 🎮 Demo Agent Features

The interactive demo agent showcases all three tools in action:

```bash
cd demo_agent
pip install -r ../requirements.txt
cp .env.example .env  # Add your API keys
python agent.py
```

**Try these commands:**

```
# Speech processing
transcribe audio: recording.mp3 in Turkish

# CRM search
search for contacts with email containing '@example.com'

# Teams notification
send a Teams notification about new leads

# Combined workflow
transcribe call.mp3, find customer in HubSpot, and send summary to Teams
```

## 🛠️ Tools Overview

### Deepgram - Speech & Audio Processing

- Speech-to-text with 30+ languages
- Text-to-speech with natural voices
- Audio intelligence (sentiment, topics, intents)
- Speaker diarization

### HubSpot - CRM Operations

- Search across any object type
- Get, create, update records
- Property discovery
- Association management

### Microsoft Teams - Rich Notifications

- Adaptive card templates
- Custom cards with buttons
- Approval requests
- Status updates

## 📚 Documentation

- **Package Docs**: [strands-tools-community](https://github.com/eraykeskinmac/strands-tools-community)
- **Strands SDK**: [strands-agents](https://github.com/strands-agents/strands)
- **Demo Agent Guide**: [demo_agent/README.md](./demo_agent/README.md)

## 🤝 Contributing

Found a bug or have an example to share? PRs welcome!

## 📄 License

MIT License - see the main package [LICENSE](https://github.com/eraykeskinmac/strands-tools-community/blob/main/LICENSE)

---

**Made with ❤️ by the community**
