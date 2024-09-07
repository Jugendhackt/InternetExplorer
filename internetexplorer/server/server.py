import asyncio
import websockets
import json 
file = open("config.json")
configFileContent = json.loads(file.read())

# Funktion, die Nachrichten vom Client empfängt und antwortet
async def handle_client(websocket, path):
    print(f"Neuer Client verbunden: {path}")
    
    try:
        async for message in websocket:
            print(f"Nachricht vom Client: {message}")
            
            # Sende eine Antwort zurück an den Client
            response = f"Server hat deine Nachricht '{message}' erhalten."
            await websocket.send(response)
    except websockets.ConnectionClosedOK:
        print("Verbindung wurde geschlossen.")

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(handle_client, configFileContent["server"]["address"], configFileContent["server"]["port"]):
        await asyncio.Future()  # run forever       

if __name__ == "__main__":
    asyncio.run(main())
