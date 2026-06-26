from gtts import gTTS
import tempfile
import os

# ── Online TTS (gTTS) ──────────────────────────────────────────────────────
def online_tts(text, lang="en", speed=False):
    tts = gTTS(text=text, lang=lang, slow=speed)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        temp_path = f.name

    tts.save(temp_path)

    with open(temp_path, "rb") as f:
        audio_bytes = f.read()

    os.remove(temp_path)
    return audio_bytes, "audio/mp3"


# ── Offline TTS (pyttsx3) — only works locally ────────────────────────────
def offline_tts(text, speed=150):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", speed)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            temp_path = f.name

        engine.save_to_file(text, temp_path)
        engine.runAndWait()

        with open(temp_path, "rb") as f:
            audio_bytes = f.read()

        os.remove(temp_path)
        return audio_bytes, "audio/wav"

    except Exception:
        return None, None