
# with open(r"C:\Users\User\Downloads\12.png", "rb") as f:
#     text = f.read()
#     #print(text)
# temp = "lol".encode()+text
# print(temp[:3].decode())
# with open(r"C:\Users\User\Downloads\new2.png", "wb") as f:
#     f.write(temp[3:])

# import socket
# tmp = socket.gethostbyname(socket.gethostname())
# print((tmp))

# import queue

# q = queue.Queue()
# print(q.get())

# import database as db
# tmp = db.users_db("try.db")
# tmp.add_client("omer", "1.18.52.1", 9999, "aaaa")
# tmp.add_client("tom", "1.2.9.1", 9111, "bbbbb")
# tmp.add_client("hi", "1.9.11.3", 4111, "ccccc")
# a = (tmp.get_user_by_single_info("1.2.9.1", 3))
# # print(a)
# print(111111111, tmp.get_specific_stat_from_all_users(3))from vidstream import StreamingServer
# from vidstream import StreamingServer

# server = StreamingServer('127.0.0.1', 9999)
# server.start_server()

# # Other Code
# input("121")
# # When You Are Done
# server.stop_server()
# import ssl

# print(ssl.PROTOCOL_SSLv23)
#server
import socket, ssl




def server(host, port, certfile=r"cyberProject\try\localhost.pem", cafile = r"cyberProject\try\cacert.pem"):
    purpose = ssl.Purpose.CLIENT_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)
    context.load_cert_chain(certfile)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, port))
    listener.listen(1)
    print('Listening at interface {!r} and port {}'.format(host, port))
    raw_sock, address = listener.accept()
    print('Connection from host {!r} and port {}'.format(*address))
    ssl_sock = context.wrap_socket(raw_sock, server_side=True)

    ssl_sock.sendall('Simple is better than complex.'.encode('ascii'))
    ssl_sock.close()

if __name__ == '__main__':
    server("0.0.0.0", 18820)
