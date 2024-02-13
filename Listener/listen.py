from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import socket

KEY = b'11111111111111111111111111111111'  # Same AES-256 key as the sender

def decrypt_data(iv_and_ct):
    iv = iv_and_ct[:16]  # Extract the first 16 bytes as the IV
    ct = iv_and_ct[16:]  # The rest is the ciphertext
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 9876))
        s.listen()
        print("Listening for incoming connections...")
        conn, addr = s.accept()
        with conn:
            print("Connected by {}".format(addr))
            encrypted_data = conn.recv(4096)  # Adjust buffer size as needed
            print("Received encrypted data, decrypting...")
            decrypted_data = decrypt_data(encrypted_data)
            print("Decrypted data: {}".format(decrypted_data))

if __name__ == '__main__':
    start_server()
