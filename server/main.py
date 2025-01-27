import socket
import secrets
import configparser
import os
import threading
import argon2

ADDRESS = '127.0.0.1'
PORT = 5000

COMMAND_BUFFER = 4096


config = configparser.ConfigParser()
config.read('config.cfg')

if not os.path.exists('./salt.key'):
    with open('./salt.key', 'w') as salt_file:
        salt = secrets.token_hex(8).encode()
        salt_file.write(salt)
else:
    with open('./salt.key', 'r') as salt_file:
        salt = (salt_file.read()).encode()

ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
thread_count = 0
bind_address = (ADDRESS, PORT)
try:
    ServerSocket.bind(bind_address)
    print(f'Bind to Address {ADDRESS}:{PORT}')
except socket.error:
    print(str(socket.error))

print('Waiting for Connection...')
ServerSocket.listen(5)

def threaded_client(connection, address):
    connection.send(bytes(salt))
    hasher = argon2.PasswordHasher()
    username = connection.recv(32)
    password = connection.recv(66)
    if (username.decode() + '.key') in os.listdir('./Users'):
        with open(('./Users/' + username.decode() + '.key'), 'r') as user_key:
            key = user_key.read()
        try:
            hasher.verify(str('$argon2id$v=19$m=65536,t=3,p=4$'+key), password)
            connection.send(b'User logged in!')
            print('User logged in!')
        except argon2.exceptions.VerificationError:
            connection.send(b'Wrong Password!')
            print('Wrong Password!')
    else: 
        connection.send(b'User not found!')
        print('User not found!')
    while True:
        command = connection.recv(COMMAND_BUFFER)
        if command == 'close': break
        elif command.startswith(b'file-up'):
            command = command.decode()[8:]
            instruction = command.split('|')
            
        elif command.startswith(b'file-up2'):
            command = command.decode()[9:]
            instruction = command.split('|')

while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,address)
    )
    client_handler.start()
    thread_count += 1
    print(f'Connection Request {thread_count} from {address[0]}:{address[1]}')
ServerSocket.close()