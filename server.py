import socket
import json
from datetime import datetime, timedelta


HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            queue = []
            start = datetime.now()
            while True:
                try:
                    data = conn.recv(1024)
                    if data:
                        messages = json.loads(data.decode('utf-8'))
                        messages = sorted(messages, key = lambda k: k['timestamp'])
                        queue += messages

                    elapsed = start - datetime.now()
                    if elapsed > timedelta(seconds=10) or len(queue) > 10:
                        with open('output.txt', 'a') as file:
                            file.write(json.dumps(queue))
                        queue = []
                        start = datetime.now()

                    conn.sendall(data) 
                except Exception as e:
                    print("Got error: ")
                    print(e)
                    break


