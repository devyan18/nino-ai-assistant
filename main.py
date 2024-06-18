from src.listen_mic import AudioRecorder
from src.nino_assistant import NinoAssistant
from src.nino_context import NINO_CONTEXT
from src.sound_to_text import AudioToTextConverter
from src.utils import delete_file

def on_save(self, filename):

    att = AudioToTextConverter()

    try:
        self.mute_microphone()
        
        nino = NinoAssistant(context=NINO_CONTEXT)
        
        prompt = att.convert_wav_to_text(filename)

        print("User: ", prompt)

        text = nino.fetch_nino(prompt)
        
        nino.nino_say(text)

        self.unmute_microphone()


        delete_file(filename)
    except KeyboardInterrupt:
        print("Bye")


if __name__ == "__main__":
    threshold = 9000  # Umbral de volumen para comenzar a grabar
    output_dir = "./records/"  # Directorio de salida para los archivos de audio
    silence_timeout_ms = 1000  # Tiempo de silencio en milisegundos
    recorder = AudioRecorder(threshold, output_dir, silence_timeout_ms, on_save=on_save)
    try:
        recorder.record()
    except KeyboardInterrupt:
        print("Grabación detenida por el usuario.")
        recorder.stop_stream()
    print("Bye")