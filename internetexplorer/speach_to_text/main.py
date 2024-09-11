import keyboard
from numpy import rec
import sounddevice as sd
from scipy.io.wavfile import write
from time import sleep

from internetexplorer.speach_to_text import stt


# Audio-Aufnahme Einstellungen
CHUNK = 1024  # Datenblockgröße
CHANNELS = 1  # Mono
RATE = 44100  # Abtastrate in Hz


def record_audio():
    print("Drücke die Leertaste zum Aufnehmen...")

    # Warte auf die Space-Taste zum Start der Aufnahme
    keyboard.wait("space")
    recording = sd.rec(int(10 * RATE), samplerate=RATE, channels=CHANNELS)
    print("Aufnahme gestartet...")

    # Solange die Space-Taste gedrückt ist, Audio aufnehmen
    while keyboard.is_pressed("space"):
        sleep(0.1)

    # Beende Aufnahme
    sd.stop()
    print("Aufnahme beendet.")

    # Speichere die Aufnahme als WAV-Datei
    wav_output_filename = "input.wav"
    write(wav_output_filename, RATE, recording)

    print(f"Aufnahme gespeichert als {wav_output_filename}")
    return stt.SpeechRecognizer()


def main():
    while True:
        yield str(record_audio())


# Beispielaufruf
if __name__ == "__main__":
    while True:
        print(record_audio())
