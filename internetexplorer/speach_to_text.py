import locale
from pathlib import Path
from typing import Callable
import wave

import pyaudio
import pynput
import speech_recognition as sr


# Audio-Aufnahme Einstellungen
CHUNK = 1024  # Datenblockgröße
FORMAT = pyaudio.paInt16  # 16 Bit Format
CHANNELS = 1  # Mono
RATE = 44100  # Abtastrate in Hz


class Recorder:
    def __init__(self, handler: Callable):
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        self.frames = []
        self.handler = handler
        self.recording = False

        print("Drücke die Leertaste zum Aufnehmen...")
        with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if key != pynput.keyboard.Key.space:
            return
        if not self.recording:
            print("Aufnahme gestartet.")
            self.recording = True

        data = self.stream.read(CHUNK)
        self.frames.append(data)

        return True  # tell the listener to continue listening

    def on_release(self, key):
        if key != pynput.keyboard.Key.space:
            return
        self.recording = False
        print("Aufnahme beendet.")

        wav_output_filename = "input.wav"
        with wave.open(wav_output_filename, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(self.frames))

        self.handler(_speech_recognizer())

        self.frames = []

        return True  # tell the listener to continue listening


def _speech_recognizer(audio_file_path="input.wav") -> str | None:
    # Bestimme die Spracheinstellungen des Systems
    lang, _ = locale.getlocale()
    lang = "de_DE"

    # Initialisiere den Recognizer
    r = sr.Recognizer()

    Path("input.wav").touch()
    # Lade die Audiodatei
    with sr.AudioFile(audio_file_path) as source:
        audio_data = r.record(source)  # Nimm das Audio aus der Datei auf

    # Erkenne die Sprache im Audio und gebe den Text zurück
    try:
        recognized_text = r.recognize_google(audio_data, language=lang)
        print(f"Erkannter Text: {recognized_text}")
        return recognized_text
    except sr.UnknownValueError:
        print("Google Speech Recognition konnte den Text nicht verstehen.")
    except sr.RequestError as e:
        print(f"Fehler bei der Verbindung mit der Google-API: {e}")
        return None

        # Beispielaufruf der Funktion
        recognized_text = _speech_recognizer()
        # print(recognized_text)
        return recognized_text


# Beispielaufruf
if __name__ == "__main__":
    r = Recorder(lambda text: text)
