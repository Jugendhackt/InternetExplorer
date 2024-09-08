import asyncio
from dataclasses import dataclass
import websockets
import json 
from os import path
import time

file = open(path.join("internetexplorer", "server", "config.json"))

configFileContent = json.loads(file.read())

shared_state = {
    "websocket": None
}

async def handle_client(socket, path):
    shared_state["websocket"] = socket
    print(f"New client connected to path {path}")

    # TODO send the state of the settings here
    
    try:
        async for message in socket:
            print(f"Received message: {message}")

            parsed_message = json.loads(message)
            action = parsed_message["action"]
            
            print(f"Action: {action}")

            if action == "change_setting":
                setting_id = parsed_message["setting_id"]
                new_state = parsed_message["new_state"]
                print(f"Changing setting {setting_id} to {new_state}")
                # TODO implement
            elif action == "kill":
                print("Kill switch pressed!")
                # TODO implement
            elif action == "submit_prompt":
                prompt = parsed_message["prompt"]
                # TODO implement

    except websockets.ConnectionClosedOK:
        print("Connection closed.")

async def main():
    #websocket = websockets.serve(handle_client, configFileContent["server"]["address"], configFileContent["server"]["port"])
    address = configFileContent["server"]["address"]
    port =  configFileContent["server"]["port"]

    print(f"Running server on {address}:{port}")

    async with websockets.serve(handle_client, address, port):
        await asyncio.Future()  # run forever       

def send_voice_input(input: str):
    send({
        "action": "input",
        "inputType": "voice",
        "inputText": input
    })

@dataclass
class BrowseAction:
    type: str # the function name (e.g. open_website)
    action_data: dict[str, str] # map of properties for debugging
    result: str #either "success" or "failure", currently unused

# takes a list of entries that will be grouped
def send_browse_action_entry(actions):
    list = []

    for action in actions:
        list.append({
            "type": action.type,
            "actionData": action.action_data,
            "result": action.result
        })

    send({
        "action": "action_entry",
        "actions": list
    })

def send(object):
    string = json.dumps(object)
    asyncio.run(send_async(string))

async def send_async(string):
    if shared_state["websocket"]:
        await shared_state["websocket"].send(string)

# Call this function to start the server thread
def run():
    print("Running server")

    asyncio.run(main())

if __name__ == "__main__":
    run()


