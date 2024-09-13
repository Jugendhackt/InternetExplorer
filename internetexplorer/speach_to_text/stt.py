import locale
from pathlib import Path

import speech_recognition as sr


def speech_recognizer(audio_file_path="input.wav") -> str | None:
    # Bestimme die Spracheinstellungen des Systems
    lang, _ = locale.getlocale()

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
        recognized_text = speech_recognizer()
        # print(recognized_text)
        return recognized_text


# SpeechRecognizer()
