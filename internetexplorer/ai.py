from json import loads
from os import getenv
from pathlib import Path
from re import A
from typing import Generator, Literal

from dotenv import load_dotenv
import openai
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic import BaseModel

from internetexplorer import browser_control, server


class AIError(Exception):
    pass


def main(browser: browser_control.Browser, openai_client: openai.Client, prompt: str) -> Generator[bool, None, None]:
    if prompt is None or prompt.strip() == "":
        yield False
        return

    try:
        # Let the ai figure out the ruff steps to achieve the prompt
        instructions = _select_instructions(openai_client, prompt, browser.get_current_url(), browser.get_content())
        print(f"Nächste Schritte: {instructions}")
        # Process the actions one by one
        for instruction in instructions:
            print(f"Führe aus: {instruction}")
            _process_instruction(openai_client, browser, instruction)
            yield True
    except AIError as e:
        print(f"AI Error: {e}")
        yield False
        return


def _process_instruction(client: openai.Client, browser: browser_control.Browser, instruction: str):
    action_name, arguments = _create_action(client, instruction, browser.get_content())
    print(f"Action: {action_name}, Arguments: {arguments}")

    match action_name:
        case "open_website":
            browser.load_website(arguments["url"])
        case "click_element":
            browser.click_element(arguments["xpath"])
        case "type_text":
            browser.type_text(arguments["input_text"], True)

    server.send_browse_action_entry([server.BrowseAction(action_name, arguments, "success")])


def _create_action(client: openai.Client, prompt: str, html: str | None = None) -> tuple[str, dict]:
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
        {
            "type": "function",
            "function": {
                "name": "no_action",
                "description": "If you want to do nothing, you can call this instruction. You get the website HTML and return an XPATH of the element you want to click",
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
        messages=messages, model="gpt-4o-mini", tools=tools, timeout=10, max_tokens=1000
    )

    if not chat_completion.choices or not chat_completion.choices[0].message.tool_calls:
        raise AIError(chat_completion)

    action = chat_completion.choices[0].message.tool_calls[0].function
    if action.name == "no_action":
        raise AIError("No action performed")

    return action.name, loads(action.arguments)


class SelectActionsResponseFormat(BaseModel):
    actions: list[str]


def _select_instructions(client: openai.Client, prompt: str, website_url: str, html: str) -> list[str]:
    with open(Path().cwd() / "internetexplorer" / "prompts" / "select_actions.md", "r") as f:
        system_prompt = f.read()
    system_prompt = system_prompt.format(website=website_url, html=html)

    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content=system_prompt,
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=prompt,
        ),
    ]

    chat_completion = client.beta.chat.completions.parse(
        messages=messages, model="gpt-4o-mini", response_format=SelectActionsResponseFormat, timeout=10, max_tokens=1000
    )

    if not chat_completion.choices or not chat_completion.choices[0].message.content:
        raise AIError(chat_completion)

    return loads(chat_completion.choices[0].message.content)["actions"]


def test_1():
    browser = browser_control.Browser()

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


if __name__ == "__main__":
    load_dotenv()
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    client = openai.Client(api_key=OPENAI_API_KEY)

    print(_select_instructions(client, "öffne the youtube kanal 'The Morpheus'", "browser startpage", ""))
