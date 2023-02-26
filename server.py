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


IP = socket.gethostbyname(socket.gethostname())

ADDR = (IP, PORT)


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
        self.connected_users+=1

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

        # when the client first connecting to the server, the signup command will be send
        msg = self.protocol_msg_to_send("signup", "enter your name: ")
        client_conn.send(msg)
        id =""
        server = ""
        inAction = False
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

            if (cmd == "close server"):
                msg = self.protocol_msg_to_send("close client", "")

                break

            elif (cmd == "startShareScreenMet"):
                server = ScreenShareClient(
                    socket.gethostbyname(socket.gethostname()), 10000+id)
                msg = self.protocol_msg_to_send("startShareScreenMet", str(10000+id))
                inAction = True
                server.start_stream()

            elif (cmd == "stopShareScreenMet"):
                msg = self.protocol_msg_to_send("stopShareScreenMet", "")
                inAction = False
                server.stop_stream()
            # elif (cmd == "watchStudentScreenMet"):
                
            
            elif (cmd == "signup"):
                self.database.add_client(
                    data, client_addr[0], client_addr[1], "TODO")
                uiActions.add_user_to_list(data)
                msg = self.protocol_msg_to_send(cmd, "registration successful")
                id =  self.database.get_user_by_single_info(data,1)[0]
            if (not msg == ""):
                client_conn.send(msg)
                
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
