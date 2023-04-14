# from vidstream import StreamingServer

# server = StreamingServer('127.0.0.1', 9999)
# server.start_server()

# # Other Code
# input("11111111111")
# # When You Are Done
# server.stop_server()
#client
import socket, ssl

def client(host, port):
    context = ssl.create_default_context()

    # Set the context to not verify the server's SSL/TLS certificate
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    print('Connected to host {!r} and port {}'.format(host, port))
    raw_sock = context.wrap_socket(raw_sock, server_hostname=host)

    while True:
        data = raw_sock.recv(1024).decode()
        if not data:
            break
        print(repr(data))

    raw_sock.close()




if __name__ == '__main__':
    client("127.0.0.1", 18820)