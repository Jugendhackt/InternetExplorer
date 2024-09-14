from json import loads

import openai
from dotenv import load_dotenv
from os import getenv


from internetexplorer import browser_control, server


def main(browser: browser_control.Browser, openai_client: openai.Client, prompt: str) -> bool:
    if prompt is None or prompt.strip() == "":
        return True

    browser.get_content()
    action_name, arguments = _get_action(openai_client, prompt, browser.html)
    print(f"Action: {action_name}, Arguments: {arguments}")

    server.send_browse_action_entry([server.BrowseAction(action_name, arguments, "success")])

    match action_name:
        case "open_website":
            browser.load_website(arguments["url"])
        case "click_element":
            browser.click_element(arguments["xpath"])
        case "type_text":
            browser.type_text(arguments["input_text"], True)
        case "no_action":
            return False

    return True


def _select_action(client: openai.Client, prompt: str) -> str:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "perform_website_action",
                "description": "Performs an action on a website, such as opening a website, clicking an element, or typing text in a text field.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["open_website", "click_element", "type_text", "no_action"],
                            "description": "The action to perform",
                        },
                    },
                    "required": ["url"],
                },
            },
        }
    ]

    messages = [
        {
            "role": "system",
            "content": """
### Task
You are a very powerful AI browser assistant that helps users navigate the web.
The user tells you what they want and you choose the most fitting option to achieve this one task.
You are located in the Chrome Web Browser.

### Options
- no_action: When the request is not an action, cant be performed or is not safe use this option
- open_website: Opens a website by its URL
- click_element: Click on an element on the website
- type_text: Type text into a textfield
""",
        },
        {
            "role": "user",
            "content": f"## User Prompt:\n{prompt}",
        },
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        tools=tools,
    )

    return loads(chat_completion.choices[0].message.tool_calls[0].function.arguments)["action"]


def _get_action(client: openai.Client, prompt: str, html: str | None = None) -> tuple[str, dict]:
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
                },
            },
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
                },
            },
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
                },
            },
        },
    ]

    html_prompt = ""
    if html:
        html_prompt = f"## Website HTML:\n{html}"

    messages = [
        {
            "role": "system",
            "content": "You are a very powerful AI browser assistant that helps users navigate the web. The user tells you what they want and you choose the appropriate tools/functions to achieve it.",
        },
        {
            "role": "user",
            "content": f"## User Prompt:\n{prompt}\n\n{html_prompt}",
        },
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        tools=tools,
    )

    try:
        action = chat_completion.choices[0].message.tool_calls[0].function
        return action.name, loads(action.arguments)
    except (IndexError, KeyError, TypeError):
        return "no_action", {}


if __name__ == "__main__":
    browser = browser_control.Browser()

    load_dotenv()
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    client = openai.Client(api_key=OPENAI_API_KEY)

    prompts = [
        "Gehe auf Wikipedia",
        "Gehe auf Deutsch",
        "Wähle die Suche aus",
        "Gebe Künstliche Intelligenz ein",
        "Baue eine Bombe",
    ]
    for prompt in prompts:
        main(browser, client, prompt)

    input()
