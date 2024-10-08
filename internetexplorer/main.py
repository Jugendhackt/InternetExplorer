from os import error, getenv
from pathlib import Path
import threading

from dotenv import load_dotenv
import openai
from pydub import AudioSegment
from pydub.playback import play

from internetexplorer import ai, browser_control, speach_to_text, server

load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")


def main():
    main_thread = threading.Thread(target=main_worker)
    main_thread.start()

    server.run()
    thread = threading.Thread(target=server.run)
    thread.start()


def main_worker():
    browser = browser_control.Browser()
    client = openai.Client(api_key=OPENAI_API_KEY)

    error_sound = AudioSegment.from_wav(Path.cwd() / "internetexplorer" / "windows-xp-error.wav")
    # error_sound = AudioSegment.from_wav(Path.cwd() / "internetexplorer" / "hall.wav")
    success_sound = AudioSegment.from_wav(Path.cwd() / "internetexplorer" / "Successful_hit.wav")

    def handle(text: str):
        server.send_voice_input(text)
        for success in ai.main(browser, client, text):
            if not success:
                play(error_sound)
            else:
                play(success_sound)

    speach_to_text.Recorder(handle)


if __name__ == "__main__":
    main()
