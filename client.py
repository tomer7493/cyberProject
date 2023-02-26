import os
import socket
import threading
from finals import *
import queue
from vidstream import StreamingServer,ScreenShareClient


class Client:
    def __init__(self, server_address=(socket.gethostbyname(socket.gethostname()), PORT)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.assignment_queue = queue.Queue()

        self.close_client = False
        try:
            self.sock.connect(self.server_address)
            print("Connected to server from address", self.server_address)
        except Exception as e:
            print("There is a problem with connecting to server")
            print("server address:", self.server_address)
            print(e)
            exit(0)
        self.handle_server()

    def recv_thread(self):
        while (not self.close_client):
            raw_data = ""
            try:
                raw_data = self.sock.recv(SIZE)
            except:
                if (self.close_client):
                    break
                else:
                    print("ERROR: client class - recv_thread method - receive cmd")
                continue
            # The communication protocol- [cmd]@[data]
            raw_data = raw_data.decode(FORMAT)
            raw_data = raw_data.split("@")

            cmd = raw_data[0]
            data = raw_data[1]

            self.assignment_queue.put((cmd, data))

    def handle_server(self):
        receive_thread = threading.Thread(target=self.recv_thread)
        receive_thread.start()

        client = ""
        
        print(self.server_address[0])
        inAction = False

        while (not self.close_client):
            cmd, data = self.assignment_queue.get()
            print(cmd, 85274, data)
            if (cmd == "signup"):
                if (data == "registration successful"):
                    print(data)
                else:
                    name = input(data)
                    msg = self.protocol_msg_to_send("signup", name)
                    self.sock.send(msg)
            elif (cmd == "close client"):

                self.close_client = True
                self.sock.close()
                break
            elif (cmd == "startShareScreenMet"):
                client = StreamingServer(self.server_address[0], int(data))
                inAction = True
                client.start_server()
            elif (cmd == "stopShareScreenMet"):
                inAction = False
                client.stop_server()

    def protocol_msg_to_send(self, cmd, data):
        return f"{cmd}@{data}".encode(FORMAT)


def main():
    Client()


if __name__ == "__main__":
    main()
