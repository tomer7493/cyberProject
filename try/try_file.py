
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
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt_data(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
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
    decrypted_data = unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size)
    return decrypted_data.decode('utf-8')


def serve_forever():
    host = 'localhost'
    port = 1234
    backlog = 5
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((host, port))
        server_sock.listen(backlog)
        print(f'Server started on {host}:{port}')

        while True:
            conn, address = server_sock.accept()
            print(f'Client connected from {address}')

            # Perform Diffie-Hellman key exchange
            key = dh_key_exchange(conn)

            # Receive and decrypt data from client
            data = conn.recv(buffer_size)
            decrypted_data = decrypt_data(data, key)
            print(f'Received data: {decrypted_data}')

            # Send response back to client
            message = 'Hello from server!'
            encrypted_message = encrypt_data(message, key)
            conn.send(encrypted_message)

            conn.close()


if __name__ == '__main__':
    serve_forever()

