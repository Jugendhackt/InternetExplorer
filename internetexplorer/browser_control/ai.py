from time import sleep
from json import loads

import openai
from dotenv import load_dotenv
from os import getenv

from internetexplorer.browser_control.browser import Browser
import internetexplorer.server.server as server

def main(browser: Browser, openai_client: openai.Client, prompt: str) -> None | bool:
    if not prompt: return False
    action = _get_action(openai_client, prompt, browser.html)
    print(prompt, action)

    browser.get_content()

    try:
        arguments = loads(action.arguments)
        server.send_browse_action_entry([
            server.BrowseAction(action.name, arguments, "success")
        ])
        match action.name:
            case "open_website":
                browser.load_website(arguments["url"])
            case "click_element":
                browser.click_element(arguments["xpath"])
            case "type_text":
                browser.type_text(arguments["input_text"], True)
    except: print("AI send invalid response")


def _select_action(client: openai.Client, prompt: str) -> str:
    tools = [{
        "type": "function",
        "function": {
            "name": "perform_website_action",
            "description": "Performs an action on a website, such as opening a website, clicking an element, or typing text in a text field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["open_website", "click_element", "type_text"],
                        "description": "The action to perform on the website.",
                    },
                },
                "required": ["url"],
            }
        }
    }]


    messages = [
        {
            "role": "system",
            "content": """
You are a very powerful AI browser assistant that helps users navigate the web.
The user tells you what they want and you choose the appropriate tools/functions to achieve it.
You are located in the Chrome Web Browser.
"""
        },
        {
            "role": "user",
            "content": f"## User Prompt:\n{prompt}",
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        tools=tools,
    )

    return loads(chat_completion.choices[0].message.tool_calls[0].function.arguments)["action"]



def _get_action(client: openai.Client, prompt: str, html: str | None = None):
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
        },
        {
            "type": "function",
            "function": {
                "name": "click_element",
                "description": "If you want to click an element on the website you can call this instruction. You get the website HTML and return an XPATH of the element you want to click",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "xpath": {
                            "type": "string",
                            "description": "The XPath of the element you want to click",
                        },
                    },
                    "required": ["xpath"],
                    "additionalProperties": False,
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "type_text",
                "description": "If you want to write text into a textfield you can use this instruction. Also you need to specify, what you want to type in the textfield",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_text": {
                            "type": "string",
                            "description": "The text you want to type into the element",
                        }
                    },
                    "required": ["input_text"],
                    "additionalProperties": False,
                }
            }
        }
    ]

    html_prompt = ""
    if html:
        html_prompt = f"## Website HTML:\n{html}\n\n"

    messages = [
        {
            "role": "system",
            "content": "You are a very powerful AI browser assistant that helps users navigate the web. The user tells you what they want and you choose the appropriate tools/functions to achieve it."
        },
        {
            "role": "user",
            "content": f"## User Prompt:\n{prompt}\n\n{html_prompt}",
        }
    ]


    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        tools=tools,
    )
    try: return chat_completion.choices[0].message.tool_calls[0].function
    except: return False


if __name__ == "__main__":
    browser = Browser()
    html = browser.load_website("https://wikipedia.org")

    load_dotenv()
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    client = openai.Client(api_key=OPENAI_API_KEY)

    print(_select_action(client, "Gehe auf die Suchleiste"))
