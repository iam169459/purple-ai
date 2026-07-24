# Purple AI - Personal AI Assistant 🧠

A self-improving, voice-controlled AI assistant with screen awareness, internet learning, and proactive help features.

## Features

### 🎙️ Voice Control
- Natural voice commands
- Speaker verification (recognizes your voice)
- Wake word detection ("Purple", "Hey Purple")

### 🧠 Self-Thinking Engine
- Analyzes commands before processing
- Learns from every interaction
- Auto-improves continuously
- Sets and tracks goals

### 👁️ Screen Awareness
- Watches your screen proactively
- Detects what app you're using
- Asks questions based on your activity
- Learns your work patterns

### 🌐 Internet Learning
- Auto-learns from the internet
- Web search for anything
- Learns new topics continuously
- Stores knowledge in memory

### 👤 Account Management
- Save and manage accounts
- Open accounts in browser
- Track multiple platforms

### 🔧 System Control
- Open/close applications
- Volume control
- File operations
- Run shell commands
- Screenshot and OCR

### 💬 Natural Conversations
- Witty, sarcastic personality
- Responds in English and Bangla
- Context-aware responses
- Emotional intelligence

### 📊 Personal Assistant
- Calendar events
- Reminders and alarms
- Notes and tasks
- Shopping lists
- Budget tracking

## Installation

### Prerequisites
- Python 3.8+
- macOS (primary support)

### Setup

```bash
# Clone the repository
git clone https://github.com/iam169459/purple-ai.git
cd purple-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the AI
./run.sh
```

## Usage

### Commands

| Command | Description |
|---------|-------------|
| `./run.sh` | Run Purple AI |
| `./run.sh stop` | Stop running instance |
| `./run.sh clean` | Clean temp files |
| `./run.sh diagnose` | Run diagnostics |

### Voice Commands

#### General
- "Hello" / "Hi" - Greet the AI
- "What time is it?" - Get current time
- "What's the date?" - Get current date
- "Help" - Show all commands
- "Goodbye" / "Exit" - Exit

#### Screen Awareness
- "What am I doing?" - Tell your current activity
- "Watch my screen" - Start screen monitoring
- "What apps are running?" - List running apps
- "Any suggestions?" - Get proactive help

#### Internet
- "Search [query]" - Search the web
- "Learn about [topic]" - Learn from internet
- "Start learning" - Enable auto-learning
- "What do you know?" - Show knowledge stats

#### Account Management
- "Add account [platform]" - Save account
- "Open account [platform]" - Open in browser
- "My accounts" - List all accounts
- "Remove account [platform]" - Delete account

#### Self-Thinking
- "Scan all code" - Analyze project
- "Fix all bugs" - Auto-fix issues
- "Analyze yourself" - Self-analysis
- "Think about [topic]" - Analyze something
- "Auto improve" - Self-improvement
- "Set goal [goal]" - Set improvement goal

#### System Control
- "Open [app]" - Launch application
- "Close [app]" - Quit application
- "Volume up/down" - Adjust volume
- "Screenshot" - Take screenshot

#### Personal Assistant
- "Set reminder" - Create reminder
- "Add note" - Create note
- "Add task" - Create task
- "Show calendar" - View events
- "Set alarm" - Set alarm

## Architecture

```
purple-ai/
├── main.py                 # Entry point
├── config.py              # Configuration
├── logger.py              # Logging setup
├── run.sh                 # Run script
├── requirements.txt       # Dependencies
├── core/
│   └── ai_engine.py       # Main AI engine
├── voice/
│   ├── voice_controller.py    # Voice detection
│   ├── tts_engine.py          # Text-to-speech
│   └── speaker_verification.py # Speaker recognition
├── utils/
│   ├── self_repair.py         # Auto-diagnostics
│   ├── system_monitor.py      # System monitoring
│   ├── screen_vision.py       # Screen capture/OCR
│   ├── screen_awareness.py    # Proactive monitoring
│   ├── internet_learning.py   # Internet learning
│   ├── account_manager.py     # Account management
│   ├── web_search.py          # Web search
│   ├── personal_assistant.py  # Productivity tools
│   ├── toolchain.py           # System control
│   ├── system_controller.py   # App control
│   ├── code_analyzer.py       # Code analysis
│   ├── self_thinking_engine.py # Self-improvement
│   ├── training_engine.py     # Auto-training
│   ├── thinking_engine.py     # Thinking logic
│   ├── memory_manager.py      # Memory persistence
│   └── response_generator.py  # Response generation
├── memory/               # Persistent data
└── logs/                 # Application logs
```

## How It Works

### Auto-Improvement
1. **Background Thread** - Runs every 5 minutes
2. **Per-Command Learning** - Learns from every interaction
3. **Periodic Analysis** - Self-analysis every 10 commands
4. **Internet Learning** - Learns new topics automatically

### Screen Awareness
1. Monitors screen every 20 seconds
2. Detects active app and activity
3. Asks questions when idle
4. Offers help for long tasks

### Voice Processing
1. Continuous listening with wake word
2. Speaker verification for security
3. Natural language understanding
4. Voice response with personality

## Configuration

Edit `config.py` to customize:

```python
# Speaker verification threshold
SPEAKER_THRESHOLD = 0.08

# Voice sensitivity
ENERGY_THRESHOLD = 0.6
PAUSE_THRESHOLD = 1.2

# Auto-improvement interval
AUTO_IMPROVE_INTERVAL = 5  # commands
```

## Memory Files

- `memory/user_accounts.json` - Saved accounts
- `memory/screen_context.json` - Screen activity
- `memory/internet_knowledge.json` - Learned knowledge
- `memory/search_history.json` - Web search history
- `ai_memory.json` - Main memory store

## Troubleshooting

### Common Issues

**"Could not understand command"**
- Speak clearly
- Reduce background noise
- Check microphone

**"Speaker verification failed"**
- Re-enroll your voice
- Lower threshold in config.py

**"Screen awareness error"**
- Grant screen recording permissions
- Check accessibility settings

### Reset

```bash
# Clean all temp files
./run.sh clean

# Remove memory
rm -rf memory/

# Re-run setup
./run.sh
```

## License

MIT License

## Author

**Rifat** - Creator of Purple AI

---

Made with love by Rifat 💜
