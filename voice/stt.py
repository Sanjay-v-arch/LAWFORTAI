import json
import queue
import sounddevice as sd
import wave
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-small-en-us-0.15")
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def voice_to_text():
    rec = KaldiRecognizer(model, 16000)

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        print("🎤 Listening...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
            
def voice_file_to_text(file_path):
    """
    Converts a pre-recorded WAV audio file to text (for testing without mic)
    """
    wf = wave.open(file_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    result_text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result_text += " " + res.get("text", "")
    final_res = json.loads(rec.FinalResult())
    result_text += " " + final_res.get("text", "")
    return result_text.strip()
            
        