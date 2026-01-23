# voice/tts.py

VOICE_TTS_AVAILABLE = True

try:
    import pyttsx3
except Exception as e:
    print(f"⚠️ TTS (pyttsx3) disabled: {e}")
    VOICE_TTS_AVAILABLE = False

def speak_text(text):
    if not VOICE_TTS_AVAILABLE:
        print("TTS not available. Skipping speak.")
        return
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
