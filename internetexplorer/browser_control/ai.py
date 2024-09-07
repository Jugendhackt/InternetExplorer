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
                "description": "If you want to write text into a textfield you can use this instruction. You need to get the XPath of the element you want to type in. Also you need to specify, what you want to type in the textfield and you can also directly submit, if it is a form",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "xpath": {
                            "type": "string",
                            "description": "The XPath to the element you want to type into",
                        },
                        "input_text": {
                            "type": "string",
                            "description": "The text you want to type into the element",
                        }
                    },
                    "required": ["xpath", "input_text"],
                    "additionalProperties": False,
                }
            }
        }
    ]

    messages = [
        {
            "role": "system",
            "content": "You are a very powerful AI browser assistant that helps users navigate the web. The user tells you what they want and you choose the appropriate tools/functions to achieve it."
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
