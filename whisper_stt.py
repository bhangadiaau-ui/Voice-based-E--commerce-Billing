import os
import whisper
from config import FFMPEG_DIR
from logger import get_logger

log = get_logger("WhisperSTT")

# Add ffmpeg to PATH
os.environ["PATH"] += os.pathsep + str(FFMPEG_DIR)


class WhisperSTT:

    def __init__(self, model_size="small"):
        log.info(f"Loading Whisper model ({model_size})")
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path: str) -> str:
        log.info("Transcribing audio")

        result = self.model.transcribe(
            str(audio_path),
            language="hi",     # supports Hindi speech
            task="transcribe"
        )

        return result["text"].lower().strip()