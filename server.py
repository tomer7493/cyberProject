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
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt_data(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted_data = iv + cipher.encrypt(padded_data)
    return encrypted_data

def dh_key_exchange(conn):
    # Public parameters agreed by both client and server
    p = 23
    g = 5

    # Generate private key
    b = get_random_bytes(16)  # 16 bytes for AES-128
    B = pow(g, int.from_bytes(b, byteorder='big'), p)

    # Send public key to client
    conn.send(B.to_bytes(256, byteorder='big'))

    # Receive client's public key
    A = int.from_bytes(conn.recv(256), byteorder='big')

    # Compute shared secret key
    s = pow(A, int.from_bytes(b, byteorder='big'), p)
    s_bytes = s.to_bytes(16, byteorder='big')

    return s_bytes


def decrypt_data(data, key):
    iv = data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data[AES.block_size:])
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode('utf-8')



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

        self.private_key = ""
        
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
                 # Perform Diffie-Hellman key exchange
                self.private_key = dh_key_exchange(client_conn)
    
                
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
            # raw_data = raw_data.decode(FORMAT)
            data = decrypt_data(raw_data,self.private_key)
            data = data.split("@")

            cmd = data[0]
            data = data[1]
           # if (cmd=="signup"):

            self.server_assignment_queue.put((cmd, data, (client_address,)))

    def send_to_client(self, client_conn, client_addr, assignment_queue):
        
        # # Securely exchange keys with the client
        # send_public_key(client_conn, public_key)
        # shared_key = receive_public_key_and_derive_key(client_conn, private_key)
        
        # # Use the shared key for encryption
        # cipher = Cipher(algorithms.AES(shared_key), modes.CBC(secrets.token_bytes(16)))
        # encryptor = cipher.encryptor()
        
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
                client_conn.send(encrypt_data(msg,self.private_key))

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
