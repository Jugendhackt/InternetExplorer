import time
import server
import threading

thread = threading.Thread(target=server.run)
thread.start()

while True:
    time.sleep(5)
    print("sending")
    server.send_voice_input("test 123 wtf")