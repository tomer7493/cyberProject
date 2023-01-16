import os
import socket
import threading
from finals import *
import queue



class Client:
    def __init__(self ,server_address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = socket.gethostbyname(socket.gethostname())
        self.assignment_queue = queue.Queue()
        try :
            self.sock.connect(self.server_address)
            print("Connected to server from address",self.server_address)
        except :
            print("There is a problem with connecting to server")
            print("server address:", self.server_address)
            exit(0)
        
    def recv_thread(self):
        cmd = ''
        while (True):
            try:
                raw_data = self.sock.recv(SIZE).decode(FORMAT)
            except:
                print("ERROR: client class - recv_thread method - receive cmd") 
            
            cmd_len = raw_data[:CMD_LENGTH_LENGTH].decode(FORMAT)
            raw_data = raw_data[CMD_LENGTH_LENGTH:]
            
            cmd = raw_data[:cmd_len]
            data = raw_data[cmd_len:]
            
            self.assignmentQueue.put((cmd,data))
            
                
    def handle_server(self):
        receive_thread = threading.Thread(target = self.recv_thread)
        receive_thread.start()
        
        while not queue.empty():
            cmd = self.assignment_queue.get()
            if (cmd == "fff"):
                pass
            elif (cmd == "ddd"):
                pass