import socketio
import eventlet
from eventlet import wsgi
from flask import Flask
import json
file = open("internetexplorer\config.json","r+")
configFileContent = json.loads(file.read())
file.close()

# Erstelle eine Flask-App
app = Flask(__name__)

# Initialisiere einen Socket.IO-Server
sio = socketio.Server()

# Verbinde den Socket.IO-Server mit der Flask-App
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Ereignis, wenn ein Client eine Verbindung herstellt
@sio.event
def connect(sid, environ):
    print(f"Client {sid} verbunden.")
    sio.send("Willkommen beim WebSocket-Server!", to=sid)

# Ereignis, wenn eine Nachricht empfangen wird
@sio.event
def message(sid, data):
    print(f"Nachricht von {sid}: {data}")
    
    # Sende eine Antwort zurück an den Client
    sio.send(f"Server: Nachricht '{data}' empfangen", to=sid)

# Ereignis, wenn die Verbindung eines Clients getrennt wird
@sio.event
def disconnect(sid):
    print(f"Client {sid} getrennt.")

# Starte den WebSocket-Server
if __name__ == '__main__':
    print("WebSocket-Server wird gestartet...")
    eventlet.wsgi.server(eventlet.listen((configFileContent["server"]["address"], configFileContent["server"]["port"])), app)
