import threading
from os import getenv

from dotenv import load_dotenv
import openai

import internetexplorer.speach_to_text.main as speach_to_text
from internetexplorer.browser_control.browser import Browser
import internetexplorer.browser_control.ai as ai
import internetexplorer.server.server as server


load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")


def main():
    main_thread = threading.Thread(target=main_worker)
    main_thread.start()

    server.run()   
    #thread = threading.Thread(target=server.run)
    #thread.start()


def main_worker():
    browser = Browser()
    client = openai.Client(api_key=OPENAI_API_KEY)

    for prompt in speach_to_text.main():
        print(prompt)
        ai.main(browser, client, prompt)


if __name__ == "__main__":
    main()
