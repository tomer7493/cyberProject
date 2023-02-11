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
import database


IP = socket.gethostbyname(socket.gethostname())

ADDR = (IP, PORT)


class Server:
    def __init__(self):
        self.assignment_queue = queue.Queue()
        print("Server is starting")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(ADDR)
        self.server_socket.listen()
        self.database = database.users_db()
        print(f"Server is listening on {ADDR}.")
        ui_thread = threading.Thread(
            target=self.uiRunner, args=(self.server_socket,))
        ui_thread.start()

        while (True):
            try:
                client_conn, client_addr = self.server_socket.accept()
            except OSError:  # If the ui is closed the server will shutdown
                exit(0)
            handle_client_thread = threading.Thread(
                target=self.handle_client, args=(client_conn, client_addr))
            handle_client_thread.start()

    def handle_client(self, client_conn, client_addr):
        print(f"{client_addr} connected.")
        recv_thread = threading.Thread(
            target=self.recv_from_client, args=(client_conn, self.assignment_queue))
        recv_thread.start()

        send_to_client_thread = threading.Thread(
            target=self.send_to_client, args=(client_conn, client_addr, self.assignment_queue))
        send_to_client_thread.start()
        

    def recv_from_client(self, client_conn, assignment_queue):
        pass
        
    
    def send_to_client(self, client_conn, client_addr, assignment_queue):
        
        while (True):
            cmd, data = assignment_queue.get()
            print(cmd,121212,data)
            for x in data:
                print(333,x.text())
            if (cmd == "startShareScreenMet"):
                pass
            elif (cmd == "stopShareScreenMet"):
                pass
            elif (cmd=="signup"):
                msg=self.protocol_msg_to_send("signup","enter your name: ")
                client_conn.send(msg)
                
            
    def protocol_msg_to_send(self, cmd,data):
        return f"{cmd}@{data}"
    
    
    def uiRunner(self, server_socket):
        # You need one (and only one) QApplication instance per application.
        # Pass in sys.argv to allow command line arguments for your app.
        # If you know you won't use command line arguments QApplication([]) works too.
        app = PyQt5.QtWidgets.QApplication(sys.argv)
        ex = uiFile.Ui_MainWindow()
        w = PyQt5.QtWidgets.QMainWindow()

        ex.setupUi(w, self)
        w.show()
        app.exec()
        self.close_socket(server_socket)
        exit(0)

    def close_socket(self, server_socket):
        server_socket.close()
        print("closing server")


def main():
    Server()


if __name__ == "__main__":
    main()
