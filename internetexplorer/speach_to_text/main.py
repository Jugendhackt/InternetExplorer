from typing import Callable
import wave

import pyaudio
import pynput

import internetexplorer.speach_to_text.stt as stt


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

        return True     # tell the listener to continue listening

    def on_release(self, key):
        if key != pynput.keyboard.Key.space:
            return
        self.recording = False
        print("Aufnahme beendet.")

        wav_output_filename = "input.wav"
        with wave.open(wav_output_filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))

        self.handler(stt.speech_recognizer())

        self.frames = []

        return True     # tell the listener to continue listening


# Beispielaufruf
if __name__ == "__main__":
    r = Recorder(lambda text: text)
