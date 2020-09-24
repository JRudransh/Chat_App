#!/usr/bin/python3

import socket, sys, _thread, os
from time import sleep

os.system('cls' if os.name == 'nt' else 'clear')

if len(sys.argv) != 3:
    print(f"\nUsage: python3 {sys.argv[0]} [IP] [Name]")
    print(f"Example: python3 {sys.argv[0]} 127.0.0.1 Rudransh\n")
    exit(1)

server_host = sys.argv[1]
name = sys.argv[2]


print('Client Server...')

soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)

print(shost, '({})'.format(ip))

# server_host = input('Enter IP: ')
# name = input('Enter Name: ')
port = 1234
print(f'Trying to connect to the server: {server_host}, ({port})')

sleep(1)
soc.connect((server_host, port))
print("Connected...\n")

sleep(2)
os.system('cls' if os.name == 'nt' else 'clear')

soc.send(name.encode())
server_name = soc.recv(1024)
server_name = server_name.decode()
print(f'{server_name} has joined...')
print('Enter -q to exit.')

def print_msg( thread_name ):
    while True:
        msg = soc.recv(1024)
        msg = msg.decode()
        if msg == "-q":
            print(f'{server_name} close the connection')
        elif msg != "":
            print(f'{server_name}: {msg}')
        sleep(0.5)

while True:
    try:
        _thread.start_new_thread( print_msg, ("Thread-1", ) )
    except:
        break
    try:
        message = input()
        if message == "-q":
            soc.send(message.encode())
            print("\n")
            break
        soc.send(message.encode())
    except KeyboardInterrupt:
        print('Enter -q to close the connection.')