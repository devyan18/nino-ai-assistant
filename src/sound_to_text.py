from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr

class AudioToTextConverter:
    def __init__(self, language='es-ES'):
        self.language = language

    def convert_wav_to_text(self, wav_file_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=self.language)
            return text
