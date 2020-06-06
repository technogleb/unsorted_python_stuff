"""
This is a simple http proxy, that is intended for accessing corporate network websites
from home, when used with -L forwarding option of openSSH. So, that's just an http
analogy of -D socks4 option.
"""

import socket


def run():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    proxy_socket.bind(('127.0.0.1', 5000))

    proxy_socket.listen()

    while True:
        client_socket, client_addr = proxy_socket.accept()
        print(client_addr)
        client_request = client_socket.recv(1024).decode('utf-8')
        print(client_request)

        if client_addr[0] == '127.0.0.1':
            hostname = client_request.split()[1].split('/')[2]
            ip = socket.gethostbyname(hostname)
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print(ip)
            target_socket.bind((ip, 80))

        else:
            ip = '127.0.0.1'
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            target_socket.bind((ip, 5000))

        target_socket.sendall(client_request.encode())


if __name__ == "__main__":
    run()
