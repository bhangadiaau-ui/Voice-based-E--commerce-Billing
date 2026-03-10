import os
import whisper
from config import FFMPEG_DIR
from logger import get_logger

os.environ["PATH"] += os.pathsep + str(FFMPEG_DIR)

log = get_logger("WhisperSTT")

class WhisperSTT:
    def __init__(self, model_size="base"):
        log.info("Loading Whisper model (%s)", model_size)
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path: str) -> str:
        log.info("Transcribing audio")
        result = self.model.transcribe(
    str(audio_path),
    language="hi",        # 🔥 FORCE HINDI
    task="transcribe"
)
        return result["text"].lower().strip()