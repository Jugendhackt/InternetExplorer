import pyaudio
import wave
import keyboard
import stt
# Audio-Aufnahme Einstellungen
CHUNK = 1024  # Datenblockgröße
FORMAT = pyaudio.paInt16  # 16 Bit Format
CHANNELS = 1  # Mono
RATE = 44100  # Abtastrate in Hz

def record_audio():
    # Initialisiere PyAudio
    p = pyaudio.PyAudio()

    # Öffne den Stream für die Audioaufnahme
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Drücke die Leertaste zum Aufnehmen...")

    frames = []

    # Warte auf die Space-Taste zum Start der Aufnahme
    keyboard.wait('space')
    print("Aufnahme gestartet...")

    # Solange die Space-Taste gedrückt ist, Audio aufnehmen
    while keyboard.is_pressed('space'):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Aufnahme beendet.")

    # Beende und schließe den Stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Speichere die Aufnahme als WAV-Datei
    wav_output_filename = "input.wav"
    with wave.open(wav_output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Aufnahme gespeichert als {wav_output_filename}")
    return stt.SpeechRecognizer()
# Beispielaufruf:
while True:
    print(record_audio())