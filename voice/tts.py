import pyttsx3

def speak_text(text, filename=None):
    engine = pyttsx3.init()
    
    if filename:
        # save audio to file
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return filename
    else:
        engine.say(text)
        engine.runAndWait()
        return None
