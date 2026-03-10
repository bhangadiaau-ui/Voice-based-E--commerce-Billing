from rich import print

from audio_io.recorder import record
from audio_io.text_to_speech import speak

from stt.whisper_stt import WhisperSTT
from nlp.ollama_nlp import extract_entities
from domain.cart import Cart

from config import AUDIO_FILE

from flask import Flask, render_template, jsonify

# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)

# -------------------------------
# Initialize Models
# -------------------------------
stt = WhisperSTT(model_size="small")
cart = Cart()

# Words that indicate bill completion
STOP_WORDS = [
    "total",
    "bill",
    "finish",
    "done",
    "टोटल",
    "बिल",
    "समाप्त"
]


# -------------------------------
# Webpage
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Record + Process Voice
# -------------------------------
@app.route("/record", methods=["POST"])
def record_voice():

    print("[bold green]🎤 Recording Voice...[/bold green]")

    # 🎤 record audio
    record()

    # 🧠 speech to text
    text = stt.transcribe(AUDIO_FILE).strip().lower()
    print(f"[cyan]Recognized Speech:[/cyan] {text}")

    # 🔴 Ignore silence
    if not text:
        print("[yellow]⚠️ No speech detected[/yellow]")
        speak("I did not hear anything. Please speak again.")
        return jsonify({
            "speech": "",
            "cart": cart.items,
            "total": cart.total()
        })

    # 🔑 detect bill request
    bill_requested = any(word in text for word in STOP_WORDS)

    # 🧹 remove bill words before NLP
    clean_text = text
    for word in STOP_WORDS:
        clean_text = clean_text.replace(word, "")

    clean_text = clean_text.strip()

    # 📦 extract items using NLP
    nlp_data = extract_entities(clean_text)

    if nlp_data.get("items"):
        for item in nlp_data["items"]:
            cart.add_item(item["name"], item["quantity"])
            speak(f"Added {item['quantity']} {item['name']}")

    # 🧾 If user asked for bill
    if bill_requested:

        print("\n[bold yellow]🧾 Final Bill[/bold yellow]")

        if cart.is_empty():
            print("[red]❌ Cart is empty[/red]")
            speak("Your cart is empty.")

            return jsonify({
                "speech": text,
                "cart": {},
                "total": 0
            })

        total = cart.total()

        print(f"[bold red]💰 Total Amount: {total} rupees[/bold red]")
        speak(f"Your total bill amount is {total} rupees. Thank you.")

        return jsonify({
            "speech": text,
            "cart": cart.items,
            "total": total,
            "bill_complete": True
        })

    return jsonify({
        "speech": text,
        "cart": cart.items,
        "total": cart.total(),
        "bill_complete": False
    })


# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    print("[bold green]🚀 Starting Voice Billing Web Server[/bold green]")
    app.run(debug=True)