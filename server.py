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
import uiActions
from vidstream import StreamingServer, ScreenShareClient
import socket
import ssl
import secrets
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Generate a new private-public key pair for the server
parameters = dh.generate_parameters(generator=2, key_size=2048)
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

# Send the server's public key to the client
def send_public_key(conn, public_key):
    serialized_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    conn.sendall(serialized_key)

# Receive the client's public key and derive a shared secret key
def receive_public_key_and_derive_key(conn, private_key):
    serialized_key = conn.recv(1024)
    client_public_key = serialization.load_pem_public_key(serialized_key)
    shared_key = private_key.exchange(client_public_key)
    return shared_key

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cyberProject\server.crt", keyfile="cyberProject\server.key")
# purpose = ssl.Purpose.CLIENT_AUTH
# context = ssl.create_default_context(purpose, cafile="cyberProject\keys_try\localhost.pem")
# context.load_cert_chain("cyberProject\keys_try\ca.crt")


IP = socket.gethostbyname(socket.gethostname())

ADDR = (IP, PORT)
print(ADDR)
ADDR = ("192.168.1.21", PORT)


class Server:
    def __init__(self):
        # [0]- cmd , [1]-data, [2]-clients that should get the assignment
        self.server_assignment_queue = queue.Queue()
        print("Server is starting")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(ADDR)
        self.server_socket.listen()
        self.unregistered_users_list = {}
        self.queue_for_client_dict = {}
        self.database = database.users_db("users_database.db")
        self.connected_users = 0
        # self.server_get_share_screen = StreamingServer(ADDR[0], 10000).start_server()
        self.first_run = True

        global shutdown
        shutdown = False
        print(f"Server is listening on {ADDR}.")
        ui_thread = threading.Thread(target=self.uiRunner)
        ui_thread.start()

        handle_server_asg_thread = threading.Thread(
            target=self.handle_server_assignment)
        handle_server_asg_thread.start()

        while (True):  # this loop will be closed immediately when the server will shut down because off the try-except statement
            try:
                client_conn, client_addr = self.server_socket.accept()
                self.server_socket = context.wrap_socket(self.server_socket, server_side=True)
                

                # Set the SSL protocol version
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

                # Create an SSL socket
                self.server_socket = ssl_context.wrap_socket(socket.socket(), server_hostname=str(self.server_socket))

            except OSError:  # If the ui is closed the server will shutdown
                exit(0)
            handle_client_thread = threading.Thread(
                target=self.handle_client, args=(client_conn, client_addr))
            handle_client_thread.start()

    def handle_client(self, client_conn, client_addr):
        print(f"{client_addr} connected.")

        client_assignment_queue = queue.Queue()
        self.queue_for_client_dict.update(
            {client_addr: client_assignment_queue})

        recv_thread = threading.Thread(
            target=self.recv_from_client, args=(client_conn, client_addr))
        recv_thread.start()

        send_to_client_thread = threading.Thread(
            target=self.send_to_client, args=(client_conn, client_addr, client_assignment_queue))
        send_to_client_thread.start()
        self.connected_users += 1

    def handle_server_assignment(self):
        while (not shutdown):
            cmd, data, users_addr = self.server_assignment_queue.get()
            for user_addr in users_addr:
                if (not user_addr == []):  # ????????????????
                    current_user_queue = self.queue_for_client_dict.get(
                        user_addr)
                    current_user_queue.put((cmd, data))
            if (cmd == "close server"):
                # time.sleep(10)
                self.server_socket.close()

    def recv_from_client(self, client_conn, client_address):
        while (not shutdown):
            raw_data = ""
            try:
                raw_data = client_conn.recv(SIZE)
            except:
                if (shutdown):
                    break
                else:
                    print("ERROR: client class - recv_thread method - receive cmd")
            # The communication protocol- [cmd]@[data]
            raw_data = raw_data.decode(FORMAT)
            raw_data = raw_data.split("@")

            cmd = raw_data[0]
            data = raw_data[1]
           # if (cmd=="signup"):

            self.server_assignment_queue.put((cmd, data, (client_address,)))

    def send_to_client(self, client_conn, client_addr, assignment_queue):
        
        # Securely exchange keys with the client
        send_public_key(client_conn, public_key)
        shared_key = receive_public_key_and_derive_key(client_conn, private_key)
        
        # Use the shared key for encryption
        cipher = Cipher(algorithms.AES(shared_key), modes.CBC(secrets.token_bytes(16)))
        encryptor = cipher.encryptor()
        
        # when the client first connecting to the server, the signup command will be send
        msg = self.protocol_msg_to_send("signup", "enter your name: ")
        client_conn.send(msg)
        id = ""
        server_share = ""
        server_get_share_screen = ""
        inAction = False
        if self.first_run:
            # server_get_share_screen = StreamingServer(ADDR[0], 10000).start_server()
            print(client_addr,88888888888888888888888)
            self.first_run = False
        share_screen_first_run = True
        start_or_stop = True
        while (not shutdown):
            msg = ""
            # # checks if the this client is the last one the should get the assignment
            # users_selected_list = assignment_queue.queue[0][2]
            # if (len(users_selected_list) == 1):
            #     cmd, data, tmp = assignment_queue.get()
            # else:
            #     cmd, data, tmp = assignment_queue.queue[0]

            cmd, data = assignment_queue.get()

            print(cmd, 121212, data)
            # seeing which user is selected
            # for x in data:
            #    print(333,x.text())

            if (cmd == "signup"):
                self.database.add_client(
                    data, client_addr[0], client_addr[1], "TODO")
                uiActions.add_user_to_list(data)
                id = self.database.get_user_by_single_info(data, 1)[0]
                msg = self.protocol_msg_to_send(cmd, f"registration successful#{id}")

            elif (cmd == "close server"):
                msg = self.protocol_msg_to_send("close client", "")
                break

            elif (cmd == "startShareScreenMet"):
                server_share = ScreenShareClient(
                    client_addr[0], 10000+id,1920,1050)
                msg = self.protocol_msg_to_send("startShareScreenMet", str(10000+id))
                # inAction = True
                server_share.start_stream()

            elif (cmd == "stopShareScreenMet"):
                msg = self.protocol_msg_to_send("stopShareScreenMet", "")
                # inAction = False
                time.sleep(0.5)
                server_share.stop_stream()
                
            elif (cmd == "watchStudentScreenMet"):
                if start_or_stop:    
                    print(client_addr[0], "hahahhahahha")
                    server_get_share_screen = StreamingServer(ADDR[0], 10000+id)
                    server_get_share_screen.start_server() 
                else:
                    server_get_share_screen.stop_server()
                msg = self.protocol_msg_to_send(
                    "watchStudentScreenMet", str(10000))
                
                start_or_stop = not start_or_stop
            if (not msg == ""):
                client_conn.send(encryptor.update(msg) + encryptor.finalize())

    # def send_all (self,msg):
    #     self.

    def protocol_msg_to_send(self, cmd, data):
        return f"{cmd}@{data}".encode(FORMAT)

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
