import queue
import socket
import ssl
import threading
import time

import pynput
from finals import *
from vidstream import ScreenShareClient, StreamingServer

# def dh_key_exchange(conn):
#     # Public parameters agreed by both client and server
#     p = 23
#     g = 5

#     # Generate private key
#     a = get_random_bytes(16)  # 16 bytes for AES-128
#     A = pow(g, int.from_bytes(a, byteorder='big'), p)

#     # Send public key to server
#     conn.send(A.to_bytes(256, byteorder='big'))

#     # Receive server's public key
#     B = int.from_bytes(conn.recv(256), byteorder='big')

#     # Compute shared secret key
#     s = pow(B, int.from_bytes(a, byteorder='big'), p)
#     s_bytes = s.to_bytes(16, byteorder='big')

#     return s_bytes


# def encrypt_data(data, key):
#     iv = get_random_bytes(AES.block_size)
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     padded_data = pad(data.encode('utf-8'), AES.block_size)
#     encrypted_data = iv + cipher.encrypt(padded_data)
#     return encrypted_data


# def receive_response(conn, key):
#     buffer_size = 1024
#     data = conn.recv(buffer_size)
#     decrypted_data = decrypt_data(data, key)
#     print(f'Received response: {decrypted_data}')


# def decrypt_data(data, key):
#     iv = data[:AES.block_size]
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     decrypted_data = cipher.decrypt(data[AES.block_size:])
#     unpadded_data = unpad(decrypted_data, AES.block_size)
#     return unpadded_data.decode('utf-8')

# def send_request(conn, key):
#     message = 'Hello from client!'
#     encrypted_message = encrypt_data(message, key)
#     conn.send(encrypted_message)
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
        self.private_key = ""
        try:
            
            self.sock.connect(self.server_address)
            print(111)
            print("Connected to server from address", self.server_address)
        except Exception as e:
            print("There is a problem with connecting to server")
            print("server address:", self.server_address)
            print(e)
            exit(0)

        #  # Perform Diffie-Hellman key exchange
        # self.private_key = dh_key_exchange(self.sock)
        self.sock = context.wrap_socket(self.sock, server_hostname=server_address[0])
        self.handle_server()

    def recv_thread(self):
        
        
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
            # raw_data = raw_data.decode(FORMAT)
            raw_data = raw_data.decode(FORMAT)
            raw_data = raw_data.split("@")

            cmd = raw_data[0]
            try:
                data = raw_data[1]
            except:
                data = ""
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
            msg = ""
            cmd, data = self.assignment_queue.get()
            print(cmd, 85274, data)
            if (cmd == "signup"):
                if (data.split("#")[0] == "registration successful"):
                    print(data)
                    self.id = data.split("#")[1]
                else:
                    name = input(data)
                    msg = self.protocol_msg_to_send("signup", name)
                    # self.sock.send(encrypt_data(msg,self.private_key))
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


def main():
    Client()
    # Client(("127.0.0.1",18820))

if __name__ == "__main__":
    main()
