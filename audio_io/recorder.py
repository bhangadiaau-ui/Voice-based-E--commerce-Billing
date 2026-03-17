import sounddevice as sd
import numpy as np
import logging
from scipy.io.wavfile import write
from pathlib import Path

logger = logging.getLogger("Recorder")

SAMPLE_RATE = 44100
RECORD_SECONDS = 5  # 🔥 IMPORTANT
AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)
AUDIO_FILE = AUDIO_DIR / "input.wav"


def record():
    logger.info("Recording started")

    recording = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )

    sd.wait()
    write(AUDIO_FILE, SAMPLE_RATE, recording)

    logger.info(f"Recording saved to {AUDIO_FILE}")
