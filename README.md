# 🎙️ Local Vocal Assistant

A fully **local, privacy-first voice assistant** built with a clean modular pipeline:  
**Speech → Text → LLM → Speech**, entirely on-device with no cloud dependencies.

---

## 🧠 How It Works

The system runs as a **client-server architecture** over localhost:

```
Client (mic)
    │
    │  HTTP POST /pipeline (WAV file)
    ▼
Server (FastAPI @ localhost:8000)
    ├── [faster-whisper]  →  Transcript
    ├── [Ollama / gemma2:2b]  →  Response
    └── [Piper TTS]  →  WAV file
    │
    │  HTTP GET /audio/{name} (WAV response)
    ▼
Client (speaker playback)
```

1. **STT** — `faster-whisper` transcribes your voice in real time
2. **LLM** — `Ollama` runs `gemma2:2b` locally to generate a response
3. **TTS** — `Piper CLI` synthesizes the response into natural speech
4. **Orchestration** — `app.py` (FastAPI server) ties the full pipeline together
5. **Client** — `client_record.py` handles mic recording and audio playback

---

## 📁 Project Structure

```
Local_Vocal_Assistant/
├── app.py              # FastAPI server — pipeline orchestrator
├── stt.py              # Speech-to-Text (faster-whisper)
├── llm.py              # LLM inference via Ollama API
├── tts.py              # Text-to-Speech (Piper CLI)
├── audio_io.py         # Microphone input & speaker output
├── client_record.py    # Client — records audio and talks to the server
├── config.py           # Centralized configuration (models, paths, params)
└── requirements.txt
```

---

## ⚙️ Requirements

### System dependencies

- [Ollama](https://ollama.com/) installed and running
- [Piper TTS CLI](https://github.com/rhasspy/piper) binary accessible on your machine
- Python 3.9+

### Pull the LLM

```bash
ollama pull gemma2:2b
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

Key packages: `faster-whisper`, `fastapi`, `uvicorn`, `sounddevice`, `scipy`, `requests`

---

## 🚀 Usage

The assistant requires **two terminals** — one for the server, one for the client.

### 1. Start the server

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

### 2. Run the client

**Mode 1 — Record from microphone (5 seconds):**

```bash
python client_record.py 1
```

Press ENTER when prompted, speak, and the assistant will respond via speaker.

**Mode 2 — Send an existing WAV file:**

```bash
python client_record.py 2 path/to/input.wav
```

---

## 🔧 Configuration

Edit `config.py` to match your setup:

| Parameter | Description |
|---|---|
| `WHISPER_MODEL_SIZE` | faster-whisper model size (`tiny`, `base`, `small`...) |
| `OLLAMA_MODEL` | LLM model name via Ollama |
| `PIPER_EXE` | Absolute path to your Piper binary |
| `PIPER_VOICE_ONNX` | Path to your Piper `.onnx` voice model |
| `SYSTEM_PROMPT` | Assistant persona / instructions |

---

## 🔒 Privacy

Everything runs **100% locally**:
- No API keys required
- No data sent to external servers
- Works fully offline once models are downloaded

---

## 🗺️ Roadmap

- [ ] Wake word detection
- [ ] Streaming TTS for lower latency
- [ ] Conversation memory persistence across restarts
- [ ] Web UI (Gradio)
- [ ] Multi-language support

---

## 🧱 Built With

| Component | Technology |
|---|---|
| Speech-to-Text | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) |
| Language Model | [Ollama](https://ollama.com/) + [gemma2:2b](https://ollama.com/library/gemma2) |
| Text-to-Speech | [Piper TTS](https://github.com/rhasspy/piper) |
| Server | [FastAPI](https://fastapi.tiangolo.com/) |
| Audio I/O | sounddevice / scipy |

---

## 📄 License

MIT
