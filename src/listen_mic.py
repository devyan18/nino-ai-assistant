import pyaudio
import wave
import numpy as np
import time
import uuid
import os

class AudioRecorder:
    def __init__(self, threshold, output_dir, silence_timeout_ms, on_save=None):
        self.threshold = threshold
        self.output_dir = output_dir
        self.format = pyaudio.paInt16  # Formato de audio
        self.channels = 1  # Canal mono
        self.rate = 44100  # Tasa de muestreo
        self.chunk = 1024  # Tamaño de los fragmentos de audio
        self.silence_timeout = silence_timeout_ms / 1000  # Tiempo en segundos para detener la grabación después del silencio
        self.frames = []
        self.recording = False
        self.silence_start = None
        self.on_save = on_save  # Callback que se ejecutará al guardar el archivo
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.muted = False

    def start_stream(self):
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)
        print("Escuchando...")

    def stop_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

    def generate_filename(self):
        return os.path.join(self.output_dir, f"{uuid.uuid4()}.wav")

    def save_recording(self):
        filename = self.generate_filename()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Archivo guardado: {filename}")
        if self.on_save:
            self.on_save(self, filename)  # Ejecutar el callback con el nombre del archivo

    def record(self):
        self.start_stream()

        while True:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.linalg.norm(audio_data)

            if volume > self.threshold and not self.muted:
                if not self.recording:
                    print("Comenzando a grabar...")
                    self.recording = True
                    self.frames = []
                
                self.frames.append(data)
                self.silence_start = None
            else:
                if self.recording:
                    if self.silence_start is None:
                        self.silence_start = time.time()
                    self.frames.append(data)  # Añadir datos silenciosos durante la pausa
                    if time.time() - self.silence_start > self.silence_timeout:
                        print("Deteniendo grabación...")
                        self.recording = False
                        self.save_recording()
                        self.silence_start = None  # Reiniciar el tiempo de silencio para la próxima grabación

            time.sleep(0.01)  # Pequeña pausa para evitar alta carga de CPU

        self.stop_stream()

    def mute_microphone(self):
        if not self.muted:
            self.muted = True
            print("Micrófono silenciado.")
    
    def unmute_microphone(self):
        if self.muted:
            self.muted = False
            print("Micrófono activado.")

def on_save(filename):
    print(f"Archivo guardado en: {filename}")

