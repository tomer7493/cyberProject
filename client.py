import PyQt5
import client_start
import sys
import queue
import socket
import ssl
import threading
import time
import pynput
from finals import *
from vidstream import ScreenShareClient, StreamingServer
import client_name

context = ssl.create_default_context()

# Set the context to not verify the server's SSL/TLS certificate
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


class Client:
    def __init__(self, server_address=(socket.gethostbyname(socket.gethostname()), PORT)):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.assignment_queue = queue.Queue()
        self.id = ""
        self.close_client = False
        self.is_ip_valid = False
        self.is_name_valid = False
        self.name = ""

        try:
            self.ui_thread = threading.Thread(target=self.start_open_screen)
            self.ui_thread.start()
        except:
            print("closing ui")
        while (not self.is_ip_valid ):
            pass
        try:
            self.sock.connect(self.server_address)
            print("Connected to server from address", self.server_address)
        except Exception as e:
            print("There is a problem with connecting to server")
            print("server address:", self.server_address)
            print(e)
            exit(0)

        self.sock = context.wrap_socket(
            self.sock, server_hostname=server_address[0])

        receive_thread = threading.Thread(target=self.recv_from_server)
        receive_thread.start()

        self.handle_server()
   

    def recv_from_server(self):

        while (not self.close_client):
            raw_data = ""
            try:
                raw_data = self.sock.recv(SIZE)
            except:
                if (self.close_client):
                    break
                else:
                    print("ERROR: client class - recv_from_server method - receive cmd")
                continue
            # The communication protocol- [cmd]@[data]
            raw_data = raw_data.decode(FORMAT)
            raw_data = raw_data.split("@")

            cmd = raw_data[0]
            try:
                data = raw_data[1]
            except:
                data = ""
            self.assignment_queue.put((cmd, data))

    def handle_server(self):
        client_get = ""

        client_share = ""

        inAction = False

        while (not self.close_client):
            msg = ""
            cmd, data = self.assignment_queue.get()
            if (cmd == "signup"):
                if (data.split("#")[0] == "registration successful"):
                    self.id = data.split("#")[1]
                else:
                    # name = input(data)
                    self.ui_thread = threading.Thread(target=self.client_name_screen)
                    self.ui_thread.start()
                    while(not self.is_name_valid):
                        pass
                    msg = self.protocol_msg_to_send("signup", self.name)
            elif (cmd == "close client"):

                self.close_client = True
                self.sock.close()
                break
            elif (cmd == "startShareScreenMet"):
                client_get = StreamingServer(
                    socket.gethostbyname(socket.gethostname()), int(data))
                client_get.start_server()
                mouse_listener = pynput.mouse.Listener(suppress=True)
                mouse_listener.start()
                keyboard_listener = pynput.keyboard.Listener(suppress=True)
                keyboard_listener.start()

            elif (cmd == "stopShareScreenMet"):
        
                client_get.stop_server()
                # Enable mouse and keyboard events
                mouse_listener.stop()
                keyboard_listener.stop()

            elif (cmd == "watchStudentScreenMet"):
                if (inAction):
                    time.sleep(0.5)
                    client_share.stop_stream()
                else:
                    client_share = ScreenShareClient(
                        self.server_address[0], 10000+int(self.id), 1920, 1050)
                    client_share.start_stream()
                inAction = not inAction
            elif (cmd == "lock screen"):
                mouse_listener = pynput.mouse.Listener(suppress=True)
                mouse_listener.start()
                keyboard_listener = pynput.keyboard.Listener(suppress=True)
                keyboard_listener.start()

            elif (cmd == "unlock screen"):
                # Enable mouse and keyboard events
                mouse_listener.stop()
                keyboard_listener.stop()

            if (msg != ""):
                self.sock.send(msg.encode(FORMAT))

    def protocol_msg_to_send(self, cmd, data):
        # return f"{cmd}@{data}".encode(FORMAT)
        return f"{cmd}@{data}"

    def start_open_screen(self):
        app = PyQt5.QtWidgets.QApplication(sys.argv)
        ex = client_start.Ui_MainWindow()
        w = PyQt5.QtWidgets.QMainWindow()

        ex.setupUi(w, self)

        w.show()
        ex.done_button.clicked.connect(lambda: self.get_input(ex.ip_input, w))
        app.exec()

    def client_name_screen(self):
        app = PyQt5.QtWidgets.QApplication(sys.argv)
        ex = client_name.Ui_MainWindow()
        w = PyQt5.QtWidgets.QMainWindow()
        
        ex.setupUi(w, self)

        w.show()
        ex.done_button.clicked.connect(lambda: self.get_input_name(ex.ip_input, w))
        app.exec()

    # def ui_input(self, ip_input, done_button):
    #     done_button.clicked.connect(lambda: self.get_input(ip_input))

    def get_input(self, ip_input, app):
        self.server_address = (ip_input.text(), PORT)
        self.is_ip_valid = True
        # time.sleep(1)
        app.close()
    
    def get_input_name(self, name_input, app):
        self.name = name_input.text()
        if (self.name.isalpha()):
            self.is_name_valid = True
            app.close()
        

def main():
    Client()
    # Client(("127.0.0.1",18820))


if __name__ == "__main__":
    main()
