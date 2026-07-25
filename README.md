# Purple AI - Modern Autonomous Voice Assistant 🧠🚀

A **fully autonomous, self-improving, voice-controlled AI assistant** with full PC access, modern web/media integration, LLM support, and advanced emotional intelligence. Runs on macOS with complete system control.

---

## ✨ What's New in v2.0 (Major Update)

| Category | Features Added |
|----------|----------------|
| **🎬 Web & Media** | YouTube (Shorts/Music/Live), Netflix, Spotify, Hulu, Disney+, Prime Video, Vimeo, Dailymotion, Twitch, TikTok, Instagram |
| **🤖 Autonomous Engine** | Full PC control (files, processes, shell, apps), self-modification, self-analysis, self-optimization, goal planning |
| **🧠 Advanced LLM** | Ollama local models, OpenAI API, streaming responses, function calling, vision analysis, model management |
| **🌐 Web & Search** | 12+ search engines, Google Maps/Translate, downloads, clipboard, bookmarks, history |
| **💬 Voice & Emotion** | 47 emotion-specific voices, 30+ mood states, sarcasm, playfulness, professional modes |
| **🔐 Permissions** | Granular access control (read/write/execute/admin/full), auto-approve mode, safety guards |
| **📱 Social & Communication** | Twitter/X posting, video upload, multi-platform posting, bookmarks |
| **📁 File System** | Read/write/execute/delete/copy/move, playlist/bookmark management, media cache |
| **🎯 Smart Controls** | Volume/speed/quality/repeat/shuffle, process management, system status, shutdown/restart |

---

## 🎯 Core Capabilities

### 🎙️ Voice Control & Emotional Intelligence
- **Wake Words**: "purple", "hey purple", "ai", "jarvis", "computer", "hello", "hey" + 30+ variants
- **47 Emotion Voices**: happy, sad, angry, excited, calm, sarcastic, professional, playful, cute, flirty, cheerful, worried, grief, rage, terrified, confused, embarrassed, proud, grateful, shame, disgust, fear, hopeful, curious, thoughtful, supportive, energetic, chill, focused, silly, impatient, annoyed, disappointed, remorse, honored, obliging, teacher, nurse, cheerleader
- **30+ Mood States**: auto-shifting based on conversation context
- **Multi-language**: English + Bangla (বাংলা) support
- **Speaker Verification**: recognizes your voice for security

### 🧠 Autonomous Intelligence
- **Self-Thinking**: analyzes, plans, decides, and acts independently
- **Self-Modification**: rewrites own code, adds features, fixes bugs
- **Self-Analysis**: reviews performance, identifies weaknesses, optimizes
- **Goal Management**: sets, tracks, and completes autonomous goals
- **Continuous Learning**: learns from every interaction + internet auto-learning
- **Code Analysis**: scans entire project, finds bugs, auto-fixes

### 🖥️ Full PC Access (System Control)
```
File System     → read, write, execute, delete, copy, move, create dirs
Processes       → list, kill, monitor (CPU/memory), process tree
Shell           → execute any command, run Python scripts
Apps            → open/close any app (macOS + Windows support)
System          → shutdown, restart, sleep, status, network info
Clipboard       → copy/paste programmatically
Permissions     → granular control per category, auto-approve mode
```

### 🌐 Web & Media Mastery
- **YouTube**: play, search, shorts, music, live, playlists, download audio/video
- **Streaming**: Netflix, Hulu, Prime Video, Disney+, Spotify, Apple TV
- **Social**: Twitter/X (post tweets, video), TikTok, Instagram, Reddit, LinkedIn
- **Search**: Google, Bing, DuckDuckGo, Wikipedia, Amazon, IMDB, StackOverflow, GitHub, npm, PyPI
- **Google**: Maps, Translate, Images, News, Scholar, Drive, Docs
- **Browser**: open URLs, new tabs, history, bookmarks, close browser
- **Downloads**: files, YouTube audio/video, progress tracking

### 🤖 LLM Integration (Local + Cloud)
| Provider | Models | Features |
|----------|--------|----------|
| **Ollama** | llama3, mistral, codellama, phi3, gemma, qwen2, etc. | Local, streaming, function calling, vision |
| **OpenAI** | gpt-4o, gpt-4-turbo, gpt-3.5-turbo | Streaming, tools, vision, JSON mode |
| **LM Studio** | Any GGUF model | Local inference, OpenAI-compatible API |
| **Custom** | llama.cpp, TGI, vLLM | Extensible provider system |

**LLM Features**: streaming chat, function/tool calling, vision analysis, code generation, JSON mode, embeddings, model management (pull/delete/list), health checks

---

## 📦 Installation

### Prerequisites
- **macOS** (primary) / Linux / Windows (WSL2)
- **Python 3.10+** (3.11+ recommended)
- **Microphone** access
- **Screen Recording** permission (for screen awareness)
- **Accessibility** permission (for app control)

### Quick Start
```bash
# 1. Clone
git clone https://github.com/iam169459/purple-ai.git
cd purple-ai

# 2. Setup (auto-creates venv, installs deps)
./run.sh

# That's it! Purple AI starts listening...
```

### Optional: LLM Setup (for advanced AI)
```bash
# Option 1: Ollama (recommended for local)
brew install ollama
ollama pull llama3
ollama serve

# Option 2: LM Studio (GUI for local models)
# Download from https://lmstudio.ai

# Option 3: OpenAI API
export OPENAI_API_KEY="your-key-here"
```

---

## 🚀 Usage

### Running Purple AI

| Command | Description |
|---------|-------------|
| `./run.sh` | Run foreground (interactive) |
| `./run.sh background` / `./run.sh bg` | Run background (always listening) |
| `./run.sh stop` | Stop background instance |
| `./run.sh clean` | Clean temp/cache files |
| `./run.sh diagnose` | Run system diagnostics |
| `./run.sh service start\|stop\|status\|install\|logs` | Background service control |
| `./run.sh --help` | Show all options |

### Wake Words (Always Active)
```
"purple"        "hey purple"      "hello purple"    "okay purple"
"ai"            "hey ai"          "computer"        "jarvis"
"wake up"       "listen"          "hello"           "hey"
"excuse me"     "are you there"   "good morning"    "good night"
```
> **Always Listening**: No wake word needed for short commands (≤4 words)

---

## 🗣️ Voice Commands Reference

### 🎵 Media & Streaming
| Command | Action |
|---------|--------|
| "play youtube [song/video]" | Play on YouTube |
| "play youtube shorts [query]" | YouTube Shorts |
| "play youtube music [song]" | YouTube Music |
| "play netflix [show]" | Open Netflix |
| "play spotify [song/playlist]" | Spotify |
| "play twitch [channel]" | Twitch stream |
| "play vimeo [video]" | Vimeo |
| "pause" / "resume" / "stop" | Media control |
| "next video" / "previous video" | Navigation |
| "volume 50" / "volume up/down" | Volume control |

### 🌐 Web & Search
| Command | Action |
|---------|--------|
| "google search [query]" | Google search |
| "search the web [query]" | Multi-engine search |
| "google maps [place]" | Google Maps |
| "translate [text]" | Google Translate |
| "open [url]" | Open any URL |
| "bookmark [name] at [url]" | Save bookmark |
| "open bookmark [name]" | Open bookmark |
| "download [url]" | Download file |
| "download youtube audio [video]" | Extract audio |

### 🖥️ System Control
| Command | Action |
|---------|--------|
| "open [app]" | Launch app (chrome, vscode, finder, etc.) |
| "close [app]" | Quit app |
| "list apps" / "running apps" | Show processes |
| "shutdown" / "restart" / "sleep" | System power |
| "system status" | CPU, RAM, disk, network |
| "run command [cmd]" | Execute shell command |
| "run python [code]" | Execute Python |
| "kill process [name/pid]" | Kill process |

### 📁 File Operations
| Command | Action |
|---------|--------|
| "read file [path]" | Read file |
| "write file [path] [content]" | Write file |
| "delete file [path]" | Delete file |
| "list files [dir]" | List directory |

### 🤖 AI & Autonomous
| Command | Action |
|---------|--------|
| "think about [topic]" | Autonomous reasoning |
| "make a plan for [goal]" | Create action plan |
| "execute plan" | Run autonomous plan |
| "set goal [goal]" | Set autonomous goal |
| "self improve" / "optimize yourself" | Self-optimization |
| "analyze yourself" | Self-analysis |
| "self analyze [file]" | Code analysis |
| "self modify [file] [changes]" | Self-code-modification |
| "grant permission [type] [action]" | Grant permission |
| "enable full access" | Auto-approve mode |

### 🤖 LLM Commands
| Command | Action |
|---------|--------|
| "ask llm [question]" | Query LLM |
| "chat with ai [message]" | Streaming chat |
| "generate code [prompt]" | Code generation |
| "analyze image [path/url]" | Vision analysis |
| "list models" | Available models |
| "pull model [name]" | Download model |
| "switch model [name]" | Change model |
| "llm health" | Provider status |

### 🎭 Mood & Personality
| Command | Action |
|---------|--------|
| "what's your mood" | Current mood + traits |
| "be happy/excited/calm/silly" | Set mood |
| "be professional/teacher/nurse" | Role modes |
| "be sarcastic/playful/flirty" | Personality modes |

### 🧠 Knowledge & Memory
| Command | Action |
|---------|--------|
| "remember [info]" | Save to memory |
| "what do you remember about [topic]" | Recall |
| "search memory [query]" | Search knowledge |
| "learn about [topic]" | Internet learning |
| "what do you know" | Knowledge stats |

### 📊 Productivity
| Command | Action |
|---------|--------|
| "set reminder [time] [text]" | Reminders |
| "add note [text]" | Notes |
| "add task [text]" | Tasks |
| "show calendar" | Events |
| "set alarm [time]" | Alarms |

---

## 🏗️ Architecture

```
purple-ai/
├── main.py                      # Entry point
├── config.py                    # Configuration
├── logger.py                    # Logging
├── run.sh                       # Smart run script
├── requirements.txt             # Dependencies
├── core/
│   ├── ai_engine.py            # Main AI engine (4500+ lines)
│   └── command_registry.py     # Fast command matching
├── voice/
│   ├── voice_controller.py     # Optimized VAD + emotion voices
│   ├── tts_engine.py           # Text-to-speech
│   └── speaker_verification.py # Voice auth
├── utils/
│   ├── autonomous_engine.py    # Full PC control + permissions
│   ├── web_media.py            # 26 platforms, media, social
│   ├── llm_support.py          # LLM providers (Ollama, OpenAI, etc.)
│   ├── emotion_engine.py       # Context-aware emotion detection
│   ├── mood_system.py          # 30+ moods + adaptive shifting
│   ├── toolchain.py            # System operations bridge
│   ├── self_thinking_engine.py # Autonomous goals/analysis
│   ├── self_repair.py          # Auto-diagnostics + fixes
│   ├── advanced_ai.py          # Episodic/semantic memory
│   ├── knowledge_graph.py      # Concept relationships
│   ├── hypothesis_engine.py    # Scientific reasoning
│   ├── metacognition.py        # Self-awareness
│   ├── training_engine.py      # Auto-training
│   ├── screen_awareness.py     # Proactive screen monitoring
│   ├── screen_vision.py        # OCR + object detection
│   ├── response_generator.py   # Personality responses
│   ├── personal_assistant.py   # Calendar/notes/tasks
│   ├── code_analyzer.py        # Static analysis + fixes
│   ├── web_search.py           # Multi-engine search
│   ├── internet_learning.py    # Auto internet learning
│   └── ... (20+ more modules)
├── memory/                      # Persistent JSON storage
├── logs/                        # Application logs
├── temp/                        # Temp files + media cache
└── thinking_data/               # AI reasoning logs
```

---

## ⚙️ Configuration

Edit `config.py` for customization:

```python
# Voice & Speaker
SPEAKER_THRESHOLD = 0.08      # Voice recognition sensitivity
ENERGY_THRESHOLD = 0.6        # Microphone energy threshold
PAUSE_THRESHOLD = 1.2         # Pause before phrase ends

# Auto-Improvement
AUTO_IMPROVE_INTERVAL = 5     # Commands between self-improvement

# LLM Providers (configure in llm_support.py or env vars)
OLLAMA_HOST = "http://localhost:11434"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LMSTUDIO_HOST = "http://localhost:1234"

# Permissions
AUTO_APPROVE_THRESHOLD = 0.7  # Confidence for auto-approve
```

### Environment Variables
```bash
export OPENAI_API_KEY="sk-..."          # OpenAI
export BRAVE_API_KEY="..."              # Brave Search
export OLLAMA_HOST="http://localhost:11434"
export LMSTUDIO_HOST="http://localhost:1234"
```

---

## 🔐 Permissions System

Purple AI uses a granular permission model:

```python
# Categories
file_system:    read, write, delete, create, modify, execute
system:         apps, processes, services, network, hardware, shutdown, restart
internet:       search, browse, download, upload, api_calls
ai_self_modify: modify_code, add_features, improve_responses, learn_tasks, optimize, create_modules
voice:          speak, listen, record, tts, stt
camera:         access, capture, recognition, recording
accounts:       manage, create, delete, access
admin:          full_permission, bypass_restrictions, auto_approve, self_update, system_config
```

**Voice Commands:**
- `"grant permission system apps"` - Allow app control
- `"revoke permission internet download"` - Remove permission
- `"show permissions"` - List all
- `"enable full access"` - Auto-approve everything (admin)

---

## 📊 Data & Memory

| File | Purpose |
|------|---------|
| `memory/user_accounts.json` | Saved accounts |
| `memory/screen_context.json` | Screen activity |
| `memory/internet_knowledge.json` | Learned knowledge |
| `memory/search_history.json` | Web searches |
| `ai_memory.json` | Main conversation memory |
| `data/training_data.json` | Training patterns |
| `data/knowledge_base.json` | Semantic memory |
| `data/autonomous_memory.json` | AI autonomous memory |
| `thinking_data/` | Reasoning/decision logs |

---

## 🛠️ Troubleshooting

| Issue | Fix |
|-------|-----|
| "Could not understand" | Speak clearly, reduce noise, check mic |
| "Speaker verification failed" | Re-enroll voice, lower `SPEAKER_THRESHOLD` |
| "Screen awareness error" | Grant Screen Recording + Accessibility |
| "TTS not available" | Check `say` command (macOS) / `espeak` (Linux) |
| "Ollama not found" | `brew install ollama && ollama serve` |
| "Permission denied" | `"grant permission [category] [action]"` |

### Reset Everything
```bash
./run.sh clean
rm -rf memory/ data/ thinking_data/ logs/
./run.sh
```

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Rifat** - Creator of Purple AI

---

## 🙏 Acknowledgments

- **Ollama** for local LLM inference
- **OpenAI** for API models
- **SpeechRecognition** / **pyttsx3** for voice
- **OpenCV** for computer vision
- **psutil** for system monitoring

---

**Made with 💜 by Rifat** — *Your autonomous AI companion*

> *"I think, I learn, I improve, and I'm always listening."* — Purple AI