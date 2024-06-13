# import torch
# import whisper

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = whisper.load_model("medium", device="cuda")

# fileName = "audio.mp3"
# # use cuda for faster processing
# result = whisper.transcribe(fileName, model)

# print(result["text"])

# # import torch

# # print("CUDA disponible:", torch.cuda.is_available())
# # print("Dispositivos CUDA:", torch.cuda.device_count())
# # if torch.cuda.is_available():
# #     print("Nombre de la GPU:", torch.cuda.get_device_name(0))
# # else:
# #     print("No se encontró GPU.")
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

# Parámetros
fs = 44100  # Frecuencia de muestreo
duration = 5  # Duración de la grabación en segundos
threshold = 0.05  # Umbral de sonido para comenzar a grabar

def record_audio(filename):
    print("Grabación iniciada")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype=np.int16)

    while True:
        sd.wait()
        if np.max(np.abs(recording)) > threshold:
            break

    print("Grabación finalizada")
    sd.wait()
    wavfile.write(filename, fs, recording)

if __name__ == "__main__":
    filename = "grabacion.wav"
    record_audio(filename)
