import pyttsx3
from logger import get_logger
import threading

log = get_logger("TTS")

engine = pyttsx3.init()
engine.setProperty("rate", 150)

lock = threading.Lock()

def speak(text: str):
    with lock:
        try:
            log.info("Speaking output")
            engine.stop()  # stop previous speech if running
            engine.say(text)
            engine.runAndWait()
        except RuntimeError:
            # restart engine if loop already started
            log.warning("Restarting TTS engine")
            engine.stop()