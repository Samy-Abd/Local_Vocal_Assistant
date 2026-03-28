import subprocess
from pathlib import Path
from config import PIPER_EXE, PIPER_VOICE_ONNX

def synthesize_to_wav(text: str, out_wav_path: str) -> None:
    """
    Uses Piper CLI:
      echo "text" | piper.exe --model voice.onnx --output_file out.wav
    """
    out_path = Path(out_wav_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Piper reads from stdin; we pass text via subprocess input
    cmd = [
        PIPER_EXE,
        "--model", PIPER_VOICE_ONNX,
        "--output_file", str(out_path),
    ]

    # text must be bytes; add newline for safety
    p = subprocess.run(
        cmd,
        input=(text.strip() + "\n").encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if p.returncode != 0:
        raise RuntimeError(
            "Piper failed.\n"
            f"STDOUT:\n{p.stdout.decode(errors='ignore')}\n"
            f"STDERR:\n{p.stderr.decode(errors='ignore')}"
        )