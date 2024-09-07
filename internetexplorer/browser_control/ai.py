from dotenv import load_dotenv
from os import getenv
import openai
from internetexplorer.browser_control.browser import Browser
from time import sleep
from json import loads


load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")


def main(user_prompt: str):
    client = openai.Client(api_key=OPENAI_API_KEY)
    action = _get_action(client, user_prompt)
    print(action)

    browser = Browser()

    arguments = loads(action.arguments)
    match action.name:
        case "open_website":
            browser.load_website(arguments["url"])

    input()


def _get_action(client: openai.Client, prompt: str):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "open_website",
                "description": "Opens a website by its URL",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL of the website to open",
                        },
                    },
                    "required": ["url"],
                    "additionalProperties": False,
                }
            }
        }
    ]

    messages = [
        {
            "role": "system",
            "content": "You are a very powerful AI browser assistant that helps users navigate the web. The user tells you what they want and you choose the appropriate tools/functions to archive it."
        },
        {
            "role": "user",
            "content": prompt,
        }
    ]


    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        tools=tools,
    )

    print(chat_completion.choices[0].message.tool_calls)
    return chat_completion.choices[0].message.tool_calls[0].function


if __name__ == "__main__":
    main("Open YouTube")
