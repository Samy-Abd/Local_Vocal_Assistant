import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write, read

def record_wav(out_path: str, duration_s: float, sample_rate: int = 16000, channels: int = 1):
    audio = sd.rec(int(duration_s * sample_rate), samplerate=sample_rate, channels=channels, dtype="int16")
    sd.wait()
    write(out_path, sample_rate, audio)

def play_wav(path: str):
    sr, audio = read(path)
    # Ensure shape is (n, channels)
    if audio.ndim == 1:
        audio = audio.reshape(-1, 1)
    sd.play(audio, sr)
    sd.wait()