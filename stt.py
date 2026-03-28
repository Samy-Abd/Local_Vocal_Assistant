from faster_whisper import WhisperModel
from config import WHISPER_MODEL_SIZE

# Load once at import time for speed
_model = WhisperModel(WHISPER_MODEL_SIZE)

def transcribe_wav(wav_path: str) -> dict:
    """
    Returns:
      {
        "text": "...",
        "language": "en",
        "segments": [{"start":..., "end":..., "text":...}, ...]
      }
    """
    segments, info = _model.transcribe(wav_path, vad_filter=True)
    segs = []
    texts = []
    for s in segments:
        segs.append({"start": float(s.start), "end": float(s.end), "text": s.text})
        texts.append(s.text.strip())
    full_text = " ".join(t for t in texts if t).strip()
    return {"text": full_text, "language": info.language, "segments": segs}