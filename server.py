#!/usr/bin/python3

import socket, sys, _thread, os
from time import sleep

os.system('cls' if os.name == 'nt' else 'clear')

if len(sys.argv) != 2:
    print(f"\nUsage: python3 {sys.argv[0]} [Name]")
    print(f"Example: python3 {sys.argv[0]} Rudransh\n")
    exit(1)

name = sys.argv[1]


print('Setup Server...')

soc = socket.socket()
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = 1234
soc.bind((host_name, port))
print(host_name, '({})'.format(ip))


# name = input('Enter name: ')
soc.listen(1) #Try to locate using socket
print('Waiting for incoming connections...')
connection, addr = soc.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")
print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))

client_name = connection.recv(1024)
client_name = client_name.decode()

os.system('cls' if os.name == 'nt' else 'clear')

print(client_name + ' has connected...')
print('Enter -q to exit.')
connection.send(name.encode())

def print_msg( thread_name ):
    while True:
        msg = connection.recv(1024)
        msg = msg.decode()
        if msg == "-q":
            print(f'{client_name} exit the chat room')
        elif msg != "":
            print(f'{client_name}: {msg}')
        sleep(0.5)

while True:
    try:
        _thread.start_new_thread( print_msg, ("Thread-1", ) )
    except:
        break
    
    try:
        message = input()
        if message == '-q':
            connection.send(message.encode())
            print("\n")
            break
        connection.send(message.encode())
    except KeyboardInterrupt:
        print('Enter -q to close the connection.')
    
