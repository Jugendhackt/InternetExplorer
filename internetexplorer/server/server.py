import asyncio
import websockets
import json 
file = open("config.json")
configFileContent = json.loads(file.read())

async def handle_client(websocket, path):
    print(f"New client connected to path {path}")

    # TODO send the state of the settings here
    
    try:
        async for message in websocket:
            print(f"Received message: {message}")

            parsed_message = json.loads(message)
            action = parsed_message["action"]
            
            print(f"Action: {action}")

            if action == "change_setting":
                setting_id = parsed_message["setting_id"]
                new_state = parsed_message["new_state"]
                print(f"Changing setting {setting_id} to {new_state}")
            
            # Sende eine Antwort zurück an den Client
            #response = f"Server hat deine Nachricht '{message}' erhalten."
            #await websocket.send(response)
    except websockets.ConnectionClosedOK:
        print("Connection closed.")

async def main():
    async with websockets.serve(handle_client, configFileContent["server"]["address"], configFileContent["server"]["port"]):
        await asyncio.Future()  # run forever       

# Call this message to start the server thread
def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()
