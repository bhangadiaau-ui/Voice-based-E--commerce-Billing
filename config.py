from pathlib import Path

BASE_DIR = Path(__file__).parent

AUDIO_DIR = BASE_DIR / "audio"
AUDIO_FILE = AUDIO_DIR / "input.wav"

PRODUCT_FILE = BASE_DIR / "data" / "products.json"
FFMPEG_DIR = BASE_DIR / "ffmpeg"

SAMPLE_RATE = 44100
RECORD_SECONDS = 5

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"