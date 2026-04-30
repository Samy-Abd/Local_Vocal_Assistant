# 🎙️ Local Vocal Assistant

A fully **local, privacy-first voice assistant** built with a clean modular pipeline:  
**Speech → Text → LLM → Speech**, entirely on-device with no cloud dependencies.

---

## 🧠 How It Works

```
Microphone → [faster-whisper] → Transcript → [Ollama / gemma2:2b] → Response → [Piper TTS] → Speaker
```

1. **STT** — `faster-whisper` transcribes your voice in real time
2. **LLM** — `Ollama` runs `gemma2:2b` locally to generate a response
3. **TTS** — `Piper CLI` synthesizes the response into natural speech
4. **Audio I/O** — `audio_io.py` handles mic capture and speaker playback
5. **Orchestration** — `app.py` ties the full pipeline together

---

## 📁 Project Structure

```
Local_Vocal_Assistant/
├── app.py              # Main pipeline orchestrator
├── stt.py              # Speech-to-Text (faster-whisper)
├── llm.py              # LLM inference via Ollama API
├── tts.py              # Text-to-Speech (Piper CLI)
├── audio_io.py         # Microphone input & speaker output
├── client_record.py    # Client-side audio recording
├── config.py           # Centralized configuration (models, params)
└── requirements.txt
```

---

## ⚙️ Requirements

### System dependencies

- [Ollama](https://ollama.com/) installed and running
- [Piper TTS CLI](https://github.com/rhasspy/piper) installed and accessible in PATH
- Python 3.9+

### Pull the LLM

```bash
ollama pull gemma2:2b
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- `faster-whisper`
- `sounddevice` / `pyaudio`
- `requests`

---

## 🚀 Usage

```bash
python app.py
```

Speak into your microphone. The assistant will transcribe, think, and respond — all locally.

---

## 🔧 Configuration

Edit `config.py` to customize:

| Parameter | Default | Description |
|---|---|---|
| `WHISPER_MODEL` | `"base"` | faster-whisper model size |
| `OLLAMA_MODEL` | `"gemma2:2b"` | LLM model via Ollama |
| `PIPER_VOICE` | `"..."` | Piper voice model path |
| `LANGUAGE` | `"fr"` | Transcription language |

---

## 🔒 Privacy

Everything runs **100% locally**:
- No API keys required
- No data sent to external servers
- Works fully offline once models are downloaded

---

## 🗺️ Roadmap

- [ ] Wake word detection
- [ ] Conversation memory / multi-turn context
- [ ] Streaming TTS for lower latency
- [ ] Web UI (Gradio)
- [ ] Support for additional Piper voices / languages

---

## 🧱 Built With

| Component | Technology |
|---|---|
| Speech-to-Text | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) |
| Language Model | [Ollama](https://ollama.com/) + [gemma2:2b](https://ollama.com/library/gemma2) |
| Text-to-Speech | [Piper TTS](https://github.com/rhasspy/piper) |
| Audio I/O | sounddevice / pyaudio |

---

## 📄 License

MIT
