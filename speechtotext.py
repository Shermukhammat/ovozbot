import speech_recognition as sr
from pydub import AudioSegment


ogg : AudioSegment = AudioSegment.from_ogg('betofiq.ogg')
ogg.export("audio.wav", format="wav")


recognizer : sr.Recognizer = sr.Recognizer()
with sr.AudioFile('audio.wav') as source:
    audio_data = recognizer.record(source)

# Recognize speech using Google
try:
    text = recognizer.recognize_google(audio_data, language="uz-UZ")  # Uzbek language code
    print("Recognized Text:", text)
except sr.UnknownValueError:
    print("Google STT could not understand the audio")
except sr.RequestError:
    print("Google STT request failed")
