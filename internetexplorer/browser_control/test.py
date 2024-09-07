from os import getenv

from dotenv import load_dotenv
import openai

from internetexplorer.browser_control.browser import Browser
import internetexplorer.browser_control.ai as ai


load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")


def main():
    browser = Browser()
    client = openai.Client(api_key=OPENAI_API_KEY)

    prompts = ["Öffne YouTube"]

    for prompt in prompts:
        print(prompt)
        ai.main(browser, client, prompt)

    input()


if __name__ == "__main__":
    main()
