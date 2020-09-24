#!/usr/bin/env python

import socket
import threading
import sys


def handle(buffer):
    return buffer


def transfer(src, dst, direction):
    src_name = src.getsockname()
    src_address = src_name[0]
    src_port = src_name[1]
    dst_name = dst.getsockname()
    dst_address = dst_name[0]
    dst_port = dst_name[1]
    while True:
        buffer = src.recv(0x400)
        if len(buffer) == 0:
            print("[-] No data received! Breaking...")
            break
        if direction:
            print(f"[+] {src_address}:{src_port} >>> {dst_address}:{dst_port} [{len(buffer)}]")
        else:
            print(f"[+] {dst_address}:{dst_port} <<< {src_address}:{src_port} [{len(buffer)}]")
        dst.send(handle(buffer))
    print(f"[+] Closing connections! [{src_address}:{src_port}]")
    src.shutdown(socket.SHUT_RDWR)
    src.close()
    print(f"[+] Closing connections! [{dst_address}:{dst_port}]")
    dst.shutdown(socket.SHUT_RDWR)
    dst.close()


def server(local_host, local_port, remote_host, remote_port, max_connection):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(max_connection)
    print(f"[+] Server started [{local_host}:{local_port}]")
    print(f"[+] Connected to [{local_host}:{local_port}] to get the content of [{remote_host}:{remote_port}]")
    while True:
        local_socket, local_address = server_socket.accept()
        print(f"[+] Detect connection from [{local_address[0]}:{local_address[1]}]")
        print(f"[+] Connecting to the REMOTE server [{remote_host}:{remote_port}]")
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        print("[+] Tunnel connected! Transferring data...")
        # threads = []
        s = threading.Thread(target=transfer, args=(
            remote_socket, local_socket, False))
        r = threading.Thread(target=transfer, args=(
            local_socket, remote_socket, True))
        # threads.append(s)
        # threads.append(r)
        s.start()
        r.start()
    print("[+] Releasing resources...")
    remote_socket.shutdown(socket.SHUT_RDWR)
    remote_socket.close()
    local_socket.shutdown(socket.SHUT_RDWR)
    local_socket.close()
    print("[+] Closing the server...")
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    print("[+] Shutting down the server!")


def main():
    if len(sys.argv) != 5:
        print("Usage : ")
        print(f"\tpython {sys.argv[0]} [L_HOST] [L_PORT] [R_HOST] [R_PORT]")
        print("Example : ")
        print(f"\tpython {sys.argv[0]} 127.0.0.1 8888 127.0.0.1 22")
        print("Author : ")
        print("\tRudransh <JRudransh@protonmail.com>")
        exit(1)
    LOCAL_HOST = sys.argv[1]
    LOCAL_PORT = int(sys.argv[2])
    REMOTE_HOST = sys.argv[3]
    REMOTE_PORT = int(sys.argv[4])
    MAX_CONNECTION = 0x10
    server(LOCAL_HOST, LOCAL_PORT, REMOTE_HOST, REMOTE_PORT, MAX_CONNECTION)


if __name__ == "__main__":
    main()