import getpass
import socket
import hashlib
from argon2 import PasswordHasher

ADDRESS = '127.0.0.1'
PORT = 5000

if ADDRESS == None and PORT == None:
    print('Connection Info')
    address = input('Adress: ')
    port = int(input('Port: '))
else:
    print('Connection Info supplied!')
    address = ADDRESS
    port = PORT

net = socket.socket()
net.connect((address, port))

salt = net.recv(16)
ph = PasswordHasher()

username = hashlib.md5(input('Username: ').encode()).hexdigest()
password = ph.hash(getpass.getpass('Password: '), salt=salt)[31:]

net.send(username.encode())
net.send(password.encode())
reponse = net.recv(15).decode()
if reponse == 'Wrong Password!': exit
elif reponse == 'User not found!': exit

# file-up project-name|path|size|(md5)
# file-up2 sha1|path|size|(md5)
# MD5 comes later

command = input('> ')
net.send(command.encode())