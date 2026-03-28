from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TMP_DIR = BASE_DIR / "tmp"
ASSETS_DIR = BASE_DIR / "assets"

# Audio format for STT/TTS pipeline
SAMPLE_RATE = 16000
CHANNELS = 1

# STT (faster-whisper)
WHISPER_MODEL_SIZE = "base"  # "tiny" faster, "small" more accurate

# LLM (Ollama)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma2:2b"

SYSTEM_PROMPT = (
    "You are a helpful assistant .Answer clearly and briefly. Do not use emojis, emoticons, or decorative characters.Use plain professional text only."
)

# TTS (Piper CLI)
# Point this to your piper.exe path (absolute is safest on Windows)
PIPER_EXE = r"C:\Users\caggi\OneDrive\Bureau\M\piper\piper.exe"

# Voice model path
PIPER_VOICE_ONNX = str(ASSETS_DIR / "voice.onnx")

# Optional: Piper speaking rate (1.0 normal)
PIPER_SPEAKER_RATE = "1.0"