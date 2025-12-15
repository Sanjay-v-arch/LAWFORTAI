from voice.stt import voice_file_to_text
from voice.tts import speak_text

text = voice_file_to_text("voice/sample.wav")
print(text)

speak_text("Hello world!", filename="voice/test_output.wav")
