import queue
import socket
import ssl
import sys
import threading
import time

import database
import PyQt5.QtWidgets
import uiActions
import uiFile
from finals import *
from vidstream import ScreenShareClient, StreamingServer

certfile = r"keys\localhost.pem"
cafile = r"keys\cacert.pem"
purpose = ssl.Purpose.CLIENT_AUTH
context = ssl.create_default_context(purpose, cafile=cafile)
context.load_cert_chain(certfile)

IP = socket.gethostbyname(socket.gethostname())

ADDR = (IP, PORT)
# ADDR = ("192.168.1.21", PORT)




class Server:
    def __init__(self, localhost_ip=socket.gethostbyname(socket.gethostname()), localhost_port=PORT):
        # [0]- cmd , [1]-data, [2]-clients that should get the assignment
        self.server_assignment_queue = queue.Queue()
        print("Server is starting")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((localhost_ip, localhost_port))
        self.server_socket.listen()
        self.clients_dict = {}
        self.database = database.users_db("users_database.db")
        self.connected_users = 0

        global shutdown
        shutdown = False
        print(f"Server is listening on {ADDR}.")
        ui_thread = threading.Thread(target=self.uiRunner)
        ui_thread.start()

        handle_server_asg_thread = threading.Thread(
            target=self.handle_server_assignment)
        handle_server_asg_thread.start()

        while (self.connected_users < 100):  # this loop will be closed immediately when the server will shut down because off the try-except statement
            try:
                client_conn, client_addr = self.server_socket.accept()
                # tcp - tls secure connection
                client_conn = context.wrap_socket(
                    client_conn, server_side=True)
                self.connected_users += 1

            except OSError:  # If the ui is closed the server will shutdown
                exit(0)
            handle_client_thread = threading.Thread(
                target=self.handle_client, args=(client_conn, client_addr))
            handle_client_thread.start()

    def handle_client(self, client_conn, client_addr):
        print(f"{client_addr} connected.")

        client_assignment_queue = queue.Queue()
        self.clients_dict.update(
            {client_addr: client_assignment_queue})

        recv_thread = threading.Thread(
            target=self.recv_from_client, args=(client_conn, client_addr))
        recv_thread.start()

        send_to_client_thread = threading.Thread(
            target=self.send_to_client, args=(client_conn, client_addr, client_assignment_queue))
        send_to_client_thread.start()

    def handle_server_assignment(self):
        while (not shutdown):
            cmd, data, users_addr = self.server_assignment_queue.get()
            for user_addr in users_addr:
                if (not user_addr == []):
                    current_user_queue = self.clients_dict.get(
                        user_addr)
                    current_user_queue.put((cmd, data))
            if (cmd == "close server"):
                self.server_socket.close()

    def recv_from_client(self, client_conn, client_address):
        while (not shutdown):
            raw_data = ""
            try:
                raw_data = client_conn.recv(SIZE)
            except:
                    print("ERROR: client class - recv_thread method - receive cmd")
                    break
            # The communication protocol- [cmd]@[data]
            try:
                data = raw_data.decode(FORMAT)
                data = data.split("@")

                cmd = data[0]
                data = data[1]
            except:
                break
            self.server_assignment_queue.put((cmd, data, (client_address,)))

    def send_to_client(self, client_conn, client_addr, assignment_queue):

        msg = self.protocol_msg_to_send("signup", " ")
        client_conn.send(msg.encode(FORMAT))
        id = ""
        server_share = ""
        server_get_share_screen = ""
        is_action = False
        
        start_or_stop = True
        while (not shutdown):
            msg = ""
            cmd, data = assignment_queue.get()

            
            if (cmd == "signup"):
                self.database.add_client(
                    data, client_addr[0], client_addr[1], "TODO")
                uiActions.add_user_to_list(data)
                id = self.database.get_user_by_single_info(data, 1)[0]
                msg = self.protocol_msg_to_send(
                    cmd, f"registration successful#{id}")
            elif (cmd == "close server"):
                msg = self.protocol_msg_to_send("close client", "")
                break
            elif (cmd == "startShareScreenMet"):
                if is_action == False:
                    is_action = True
                    server_share = ScreenShareClient(
                        client_addr[0], 10000+id, 1920, 1050)
                    msg = self.protocol_msg_to_send(
                        "startShareScreenMet", str(10000+id))
                    # inAction = True
                    server_share.start_stream()
            elif (cmd == "stopShareScreenMet"):
                if is_action == True:
                    is_action = False
                    msg = self.protocol_msg_to_send("stopShareScreenMet", "")
                    # inAction = False
                    time.sleep(0.5)
                    server_share.stop_stream()
            elif (cmd == "watchStudentScreenMet"):
                if is_action != start_or_stop:
                    is_action = start_or_stop
                    if start_or_stop:
                        server_get_share_screen = StreamingServer(
                            ADDR[0], 10000+id)
                        server_get_share_screen.start_server()
                    else:
                        server_get_share_screen.stop_server()
                    msg = self.protocol_msg_to_send(
                        "watchStudentScreenMet", str(10000))
                    start_or_stop = not start_or_stop
            elif (cmd == "lock screen"):
                if is_action == False:
                    is_action = True
                    msg = self.protocol_msg_to_send(
                        "lock screen", "")
            elif (cmd == "unlock screen"):
                if is_action == True:    
                    is_action = False
                    msg = self.protocol_msg_to_send(
                        "unlock screen", "")
            if (not msg == ""):
                client_conn.send(msg.encode(FORMAT))

    # def send_all (self,msg):
    #     self.

    def protocol_msg_to_send(self, cmd, data):
        # return f"{cmd}@{data}".encode(FORMAT)
        return f"{cmd}@{data}"

    def uiRunner(self):
        # You need one (and only one) QApplication instance per application.
        # Pass in sys.argv to allow command line arguments for your app.
        # If you know you won't use command line arguments QApplication([]) works too.
        app = PyQt5.QtWidgets.QApplication(sys.argv)
        ex = uiFile.Ui_MainWindow()
        w = PyQt5.QtWidgets.QMainWindow()

        ex.setupUi(w, self)
        w.show()
        app.exec()
        self.close_socket()
        exit(0)

    def close_socket(self):
        global shutdown
        shutdown = True
        all_users = self.database.get_specific_stat_from_all_users(3)
        self.server_assignment_queue.put(("close server", "", all_users))
        print("closing server")


def main():
    Server()


if __name__ == "__main__":
    main()
