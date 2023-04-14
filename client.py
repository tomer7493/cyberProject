import os
import socket
import threading
from finals import *
import queue
import time
from vidstream import StreamingServer,ScreenShareClient
import pynput
import socket
import ssl
import secrets
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import ssl


# # Receive the server's public key and send the client's public key
# def receive_public_key_and_send_public_key(conn):
#     serialized_key = conn.recv(1024)
#     server_public_key = serialization.load_pem_public_key(serialized_key)
#     parameters = server_public_key.parameters()
#     private_key = parameters.generate_private_key()
#     public_key = private_key.public_key()
#     serialized_key = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )
#     conn.sendall(serialized_key)
#     return private_key

# context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# context.load_verify_locations(cafile=r'cyberProject\keys_try\ca.crt')



# purpose = ssl.Purpose.SERVER_AUTH
# context = ssl.create_default_context(purpose, cafile="cyberProject\keys_try\localhost.pem")

class Client:
    def __init__(self, server_address=(socket.gethostbyname(socket.gethostname()), PORT)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.assignment_queue = queue.Queue()
        self.id = ""
        self.close_client = False
        try:
            
            self.sock.connect(self.server_address)
            print(111)
            # Set the SSL protocol version
            # ssl_context  = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            # Create an SSL socket
            # self.sock = ssl_context .wrap_socket(socket.socket(), server_hostname=str(self.server_address))
            
            # self.sock=context.wrap_socket(self.sock, server_hostname=str(self.server_address))
            
            print("Connected to server from address", self.server_address)

        except Exception as e:
            print("There is a problem with connecting to server")
            print("server address:", self.server_address)
            print(e)
            exit(0)
        self.handle_server()

    def recv_thread(self):
        
        # # Securely exchange keys with the server
        # private_key = receive_public_key_and_send_public_key(self.sock)
        # shared_key = private_key.exchange(self.sock.server_public_key())

        # # Use the shared key for decryption
        # cipher = Cipher(algorithms.AES(shared_key), modes.CBC(secrets.token_bytes(16)))
        # decryptor = cipher.decryptor()
        
        while (not self.close_client):
            raw_data = ""
            try:
                raw_data = self.sock.recv(SIZE)
                # raw_data = decryptor.update(raw_data) + decryptor.finalize()
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

        client_get = ""
        
        share_screen_first_run = True
        get_screen_first_run = True
        
        client_share = ""

        print(self.server_address[0],11111111111111111111)
        inAction = False

        while (not self.close_client):
            cmd, data = self.assignment_queue.get()
            print(cmd, 85274, data)
            if (cmd == "signup"):
                if (data.split("#")[0] == "registration successful"):
                    print(data)
                    self.id = data.split("#")[1]
                else:
                    name = input(data)
                    msg = self.protocol_msg_to_send("signup", name)
                    self.sock.send(msg)
            elif (cmd == "close client"):

                self.close_client = True
                self.sock.close()
                break
            elif (cmd == "startShareScreenMet"):
                #if (get_screen_first_run):
                print(socket.gethostbyname(socket.gethostname()),int(data),"hahahhahahahah")#socket.gethostbyname(socket.gethostname())
                client_get = StreamingServer(socket.gethostbyname(socket.gethostname()), int(data))
                get_screen_first_run = False
                # inAction = True
                client_get.start_server()
                mouse_listener = pynput.mouse.Listener(suppress=True)
                mouse_listener.start()
                keyboard_listener = pynput.keyboard.Listener(suppress=True)
                keyboard_listener.start()

            elif (cmd == "stopShareScreenMet"):
                # inAction = False
                
                client_get.stop_server()
                # Enable mouse and keyboard events
                mouse_listener.stop()
                keyboard_listener.stop()

            elif (cmd == "watchStudentScreenMet"):
                if (inAction):
                    print("noooooooooooooooo")
                    time.sleep(0.5)
                    client_share.stop_stream()
                    #client_share._cleanup()
                else:
                    client_share = ScreenShareClient(self.server_address[0], 10000+int(self.id),1920,1050)
                    client_share.start_stream()
                    
                inAction =not inAction
                
                
    def protocol_msg_to_send(self, cmd, data):
        return f"{cmd}@{data}".encode(FORMAT)


def main():
    # Client(("192.168.1.21",PORT))
    Client()

if __name__ == "__main__":
    main()
