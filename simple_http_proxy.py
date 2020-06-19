"""
This is a simple http proxy, that is intended for accessing corporate network websites
from home, when used with -L forwarding option of openSSH. So, that's just an http
analogy of -D socks4 option.
"""

import socket
import logging

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5000
logging.basicConfig(level='DEBUG')


def run():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen()
    logging.info(f"Set up proxy, listening on {PROXY_HOST}:{PROXY_PORT}")

    while True:
        client_socket, client_addr = proxy_socket.accept()
        logging.info(f"Accepted connection from {client_addr}")
        client_request = client_socket.recv(1024).decode('utf-8')
        logging.debug(f"Client request is {client_request}")

        hostname = client_request.split()[1].split('/')[2]
        logging.info(f"Redirecting request to {hostname:80}")
        ip = socket.gethostbyname(hostname)
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        target_socket.connect((ip, 80))
        logging.info(f"Connected to target {hostname:80}")
        target_socket.sendall(client_request.encode())
        logging.info(f"Sent client request to target")

        target_response = target_socket.recv(1024)
        logging.info("Received target response")
        logging.debug(f"Target response is {target_response}")
        client_socket.sendall(target_response)
        logging.info("Sent target response back to client")

        target_socket.close()


if __name__ == "__main__":
    run()
