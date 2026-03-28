import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse, JSONResponse
from config import TMP_DIR
from stt import transcribe_wav
from llm import ask_ollama
from tts import synthesize_to_wav

app = FastAPI(title="Local Voice Assistant MVP")

# Simple in-memory history (per session)
HISTORY: dict[str, list[dict]] = {}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/audio/{name}")
def get_audio(name: str):
    path = TMP_DIR / name
    if not path.exists():
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(str(path), media_type="audio/wav")

@app.post("/pipeline")
async def pipeline(
    audio: UploadFile = File(...),
    session_id: str = Query(default="demo"),
):
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # Save input wav
    req_id = str(uuid.uuid4())
    in_wav = TMP_DIR / f"{req_id}_in.wav"
    out_wav = TMP_DIR / f"{req_id}_out.wav"

    content = await audio.read()
    in_wav.write_bytes(content)

    # 1) STT
    stt = transcribe_wav(str(in_wav))
    user_text = stt["text"].strip()

    if not user_text:
        return {
            "session_id": session_id,
            "transcript": "",
            "answer": "I didn't catch that. Please repeat.",
            "audio_url": None,
        }

    # 2) LLM
    history = HISTORY.get(session_id, [])
    answer = ask_ollama(user_text, history=history)

    # Update history
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": answer})
    HISTORY[session_id] = history[-12:]  # keep small

    # 3) TTS
    synthesize_to_wav(answer, str(out_wav))

    return {
        "session_id": session_id,
        "transcript": user_text,
        "answer": answer,
        "audio_url": f"/audio/{out_wav.name}",
    }