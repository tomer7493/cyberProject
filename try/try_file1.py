# from vidstream import StreamingServer

# server = StreamingServer('127.0.0.1', 9999)
# server.start_server()

# # Other Code
# input("11111111111")
# # When You Are Done
# server.stop_server()
#client
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def dh_key_exchange(conn):
    # Public parameters agreed by both client and server
    p = 23
    g = 5

    # Generate private key
    a = get_random_bytes(16)  # 16 bytes for AES-128
    A = pow(g, int.from_bytes(a, byteorder='big'), p)

    # Send public key to server
    conn.send(A.to_bytes(256, byteorder='big'))

    # Receive server's public key
    B = int.from_bytes(conn.recv(256), byteorder='big')

    # Compute shared secret key
    s = pow(B, int.from_bytes(a, byteorder='big'), p)
    s_bytes = s.to_bytes(16, byteorder='big')

    return s_bytes


def encrypt_data(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return encrypted_data


def receive_response(conn, key):
    buffer_size = 1024
    data = conn.recv(buffer_size)
    decrypted_data = decrypt_data(data, key)
    print(f'Received response: {decrypted_data}')


def decrypt_data(data, key):
    iv = data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size)
    return decrypted_data.decode('utf-8')


def send_request(conn, key):
    message = 'Hello from client!'
    encrypted_message = encrypt_data(message, key)
    conn.send(encrypted_message)


def main():
    host = 'localhost'
    port = 1234

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((host, port))

        # Perform Diffie-Hellman key exchange
        key = dh_key_exchange(client_sock)

        # Send request to server
        send_request(client_sock, key)

        # Receive and decrypt response from server
        receive_response(client_sock, key)


if __name__ == '__main__':
    main()
