# J.A.R.V.I.S. / F.R.I.D.A.Y. — Local Voice Assistant

> *"Fully Responsive Intelligent Digital Assistant for You"*

A Tony Stark-inspired local voice assistant that runs on your Windows PC, with no heavy AI models required for basic functionality.

---

## Current Version: Local Friday (Stable)

This is the active, stable version of the assistant. It works without Ollama or cloud APIs for basic commands, using:
- **SpeechRecognition** (Google Speech API) for voice input (requires internet)
- **edge-tts** (Microsoft Edge TTS) for voice output (requires internet)
- **playsound** for audio playback
- Basic built-in commands (no heavy LLM required)

*Note: This version is not 100% offline, as both speech recognition and text-to-speech require an internet connection.*

---

## Features (Local Version)

### Basic Voice Commands
| Command | Response |
|---------|-----------|
| `hola Friday` | "A sus órdenes, señor." |
| `hora` | "Son las [H] y [M]" (e.g., "Son las 13 y 27") |
| `qué día es` / `fecha` | "Hoy es [día], [día] de [mes] de [año]." (e.g., "Hoy es martes, 28 de abril de 2026.") |
| `buenos días` / `buenas tardes` / `buenas noches` | "Buenos días/tardes/noches, señor." |
| `gracias` | "Siempre a sus órdenes, señor." |
| `cómo estás` | "Operativa y lista para asistirle, señor." |
| `quién eres` | "Soy Fraidey, su asistente local." |
| `qué eres` | "Soy una interfaz de asistencia local inspirada en Fraidey." |
| `qué puedes hacer` | Lists all available commands |
| `abre Chrome` | Opens Google Chrome (if installed) |
| `abre VS Code` / `abre Visual Studio Code` | Opens VS Code (if installed) |
| `abre Spotify` | Opens Spotify (if installed) |
| `abre YouTube` / `abre Google` / `abre GitHub` / `abre ChatGPT` | Opens corresponding website |
| `salir` / `adiós` / `terminar` | "Hasta luego, señor." and closes the assistant |

### Optional: Ollama Integration
For advanced queries beyond basic commands, you can optionally use Ollama with the `mistral` model. If Ollama is unavailable, the assistant will respond with a friendly message and continue working with basic commands.
*Note: Ollama is not required for basic functionality and is not recommended for low-memory PCs.*

---

## Quick Start (Local Version)

### Prerequisites
- Python 3.11+
- Windows 10/11
- Microphone
- Internet connection (for speech recognition and text-to-speech)

### Installation
1. Clone the repository (if not already done):
   ```bash
   git clone https://github.com/yourusername/J.A.R.V.I.S.git
   cd J.A.R.V.I.S
   ```

2. Install required dependencies:
   ```bash
   python -m pip install SpeechRecognition PyAudio requests edge-tts playsound==1.2.2
   ```

### Run the Assistant
1. Verify syntax:
   ```bash
   python -m py_compile local_friday.py
   ```

2. Start the assistant:
   ```bash
   python local_friday.py
   ```

3. Speak naturally into your microphone using the commands listed above.

---

## Alternative: Cloud/API Version (Future Phase)

The original F.R.I.D.A.Y. demo uses cloud APIs and LiveKit for a more advanced experience:
- **FastMCP** server for tools/extensions
- **LiveKit Agents** for real-time voice pipeline
- **Google Gemini** (LLM), **Sarvam** (STT), **OpenAI** (TTS)

This version requires API keys and a LiveKit Cloud account, and is planned as a future phase. It is not the current active version.

### Comparison: Local vs Cloud Version
| Feature | Local Version (Active) | Cloud Version (Future) |
|---------|------------------------|------------------------|
| Internet required | Yes (STT/TTS) | Yes (all components) |
| Paid APIs | No | Yes (multiple) |
| Privacy | Local processing (except STT/TTS) | Cloud processing |
| Speed | Fast | Depends on network |
| AI Quality | Basic commands + optional Ollama | High (Gemini LLM) |
| Setup Time | ~5 minutes | ~30+ minutes |
| Voice Recognition | Google Speech | Sarvam AI |
| Voice Synthesis | edge-tts (Microsoft) | OpenAI TTS |

Refer to the original project documentation for setup details (note: this is not the current stable version).

---

## Project Structure
```
J.A.R.V.I.S/
├── local_friday.py       # Main local assistant script (active version)
├── server.py             # FastMCP server (cloud version, future phase)
├── agent_friday.py       # LiveKit voice agent (cloud version, future phase)
├── pyproject.toml       # Project dependencies
├── .env.example          # Environment variables template
├── README.md            # This documentation
├── LOCAL_GUIDE.md       # Quick local setup guide
├── friday/              # Cloud version MCP package (future phase)
│   ├── config.py
│   ├── tools/
│   ├── prompts/
│   └── resources/
└── .gitignore
```

---

## Common Issues
- **No voice output**: Verify `edge-tts` and `playsound==1.2.2` are installed correctly.
- **Speech recognition fails**: Check internet connection and microphone settings.
- **Ollama errors**: Ignore if using basic commands only; Ollama is optional.
- **playsound errors**: Install the compatible version: `pip install playsound==1.2.2`

---

## License
MIT
