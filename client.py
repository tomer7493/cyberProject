import os
import socket
import threading
from finals import *
import queue

class Client:
    def __init__(self ,server_address = (socket.gethostbyname(socket.gethostname()),PORT)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.assignment_queue = queue.Queue()
        try :
            self.sock.connect(self.server_address)
            print("Connected to server from address",self.server_address)
        except Exception as e:
            print("There is a problem with connecting to server")
            print("server address:", self.server_address)
            print(e)
            exit(0)
        self.handle_server()
    
    
    def recv_thread(self):
        while (True):
            raw_data =""
            try:
                raw_data = self.sock.recv(SIZE).decode(FORMAT)
            except:
                print("ERROR: client class - recv_thread method - receive cmd") 
            #The communication protocol- [cmd]@[data]
            raw_data = raw_data.decode(FORMAT)
            raw_data = raw_data.split("@")
           
            
            cmd = raw_data[0] 
            data = raw_data[1]
            
            self.assignment_queue.put((cmd,data))
            
    def send_data_to_server(self,cmd,data):
        msg = f"{cmd}@{data}"
        self.sock.send(msg)
        
       
    def handle_server(self):
        receive_thread = threading.Thread(target = self.recv_thread)
        receive_thread.start()
        
        while (not  self.assignment_queue.empty()):
            cmd = self.assignment_queue.get()
            if (cmd == "signup"):
                name=input("enter your name: ")
                self.send_data_to_server("signup",name)
            elif (cmd == "ddd"):
                pass
            
def main():
    Client()


if __name__ == "__main__":
    main()
