import json
import queue
import wave
import os

VOICE_AVAILABLE = True

try:
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
except Exception as e:
    print(f"⚠️ Voice STT disabled: {e}")
    VOICE_AVAILABLE = False

MODEL_PATH = "vosk-model-small-en-us-0.15"

# Global queue for mic stream
q = queue.Queue()

if VOICE_AVAILABLE and os.path.exists(MODEL_PATH):
    model = Model(MODEL_PATH)
else:
    VOICE_AVAILABLE = False


def _callback(indata, frames, time, status):
    q.put(bytes(indata))


def live_voice_to_text(timeout=10) -> str:
    """
    🎤 Live mic speech-to-text
    Stops after first sentence or timeout
    """
    if not VOICE_AVAILABLE:
        return "VOICE_NOT_AVAILABLE"

    try:
        rec = KaldiRecognizer(model, 16000)
        rec.SetWords(True)

        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=_callback
        ):
            print("🎤 Listening (live mic)...")

            for _ in range(timeout * 2):  # ~10 seconds
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        return text

        return "NO_SPEECH_DETECTED"

    except Exception as e:
        print(f"Live STT error: {e}")
        return "VOICE_PROCESSING_FAILED"


def voice_file_to_text(file_path: str) -> str:
    """
    WAV file → text (fallback)
    """
    if not VOICE_AVAILABLE:
        return "VOICE_NOT_AVAILABLE"

    try:
        wf = wave.open(file_path, "rb")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        text = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                text += " " + res.get("text", "")

        final = json.loads(rec.FinalResult())
        text += " " + final.get("text", "")

        return text.strip()

    except Exception as e:
        print(f"File STT error: {e}")
        return "VOICE_PROCESSING_FAILED"
