import os
import socket
import threading
import queue
import threading
import time
from finals import *
import uiFile
import PyQt5.QtWidgets
import sys



IP = socket.gethostbyname(socket.gethostname())

ADDR = (IP, PORT)


class Server:
    def __init__(self):
        self.assignment_queue = queue.Queue()
        print("Server is starting")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(ADDR)
        server_socket.listen()
        print(f"Server is listening on {ADDR}.")
        ui_thread = threading.Thread(target=self.uiRunner)
        ui_thread.start()
        print("lol")

        while (True):
            client_conn, client_addr = server_socket.accept()
            handle_client_thread = threading.Thread(
                target=self.handle_client, args=(client_conn, client_addr))
            handle_client_thread.start()

    def handle_client(self, client_conn, client_addr):
        print(f"{client_addr} connected.")
        recv_thread = threading.Thread(
            target=self.recv_from_client, args=(client_conn, self.assignment_queue))
        recv_thread.start()
    
        self.sendToClient(client_conn, client_addr, self.assignment_queue)

    def recv_from_client(self, client_conn, assignment_queue):
        pass

    def send_to_client(self, client_conn, client_addr, assignment_queue):
        while (True):
            cmd, data = assignment_queue.get()

            if (cmd == "1"):
                pass
            elif (cmd == "2"):
                pass
    def uiRunner(self):
        # You need one (and only one) QApplication instance per application.
        # Pass in sys.argv to allow command line arguments for your app.
        # If you know you won't use command line arguments QApplication([]) works too.
        app = PyQt5.QtWidgets.QApplication(sys.argv)
        ex = uiFile.Ui_MainWindow()
        w = PyQt5.QtWidgets.QMainWindow()


        ex.setupUi(w)
        w.show()
        sys.exit(app.exec())
        


def main():
   Server()


if __name__ == "__main__":
    main()
