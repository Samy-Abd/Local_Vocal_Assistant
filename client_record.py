import sys
import requests
from pathlib import Path
from audio_io import record_wav, play_wav
from config import SAMPLE_RATE, CHANNELS, TMP_DIR

SERVER = "http://127.0.0.1:8000"


def send_wav(wav_path: Path):
    print(f"Sending {wav_path} to pipeline...")

    with open(wav_path, "rb") as f:
        r = requests.post(
            f"{SERVER}/pipeline?session_id=demo",
            files={"audio": (wav_path.name, f, "audio/wav")},
            timeout=180,
        )

    r.raise_for_status()
    data = r.json()

    print("\nTranscript:", data["transcript"])
    print("Answer:", data["answer"])

    if data.get("audio_url"):
        audio_url = SERVER + data["audio_url"]

        out_wav = TMP_DIR / "output.wav"
        wav = requests.get(audio_url, timeout=60)
        wav.raise_for_status()

        out_wav.write_bytes(wav.content)

        print("\nPlaying answer...")
        play_wav(str(out_wav))
    else:
        print("\nNo audio returned.")


def record_mode():
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    print("Press ENTER to record 5 seconds...")
    input()

    in_wav = TMP_DIR / "input.wav"

    print("Recording...")
    record_wav(
        str(in_wav),
        duration_s=5.0,
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
    )

    send_wav(in_wav)


def file_mode(filepath: str):
    wav_path = Path(filepath)

    if not wav_path.exists():
        print(f"File not found: {filepath}")
        return

    send_wav(wav_path)


def main():

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python client_record.py 1")
        print("  python client_record.py 2 input.wav")
        return

    mode = sys.argv[1]

    if mode == "1":
        record_mode()

    elif mode == "2":
        if len(sys.argv) < 3:
            print("Please provide a wav file.")
            print("Example: python client_record.py 2 input.wav")
            return

        file_mode(sys.argv[2])

    else:
        print("Unknown mode. Use 1 or 2.")


if __name__ == "__main__":
    main()