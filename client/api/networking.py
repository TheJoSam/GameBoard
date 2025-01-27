import socket
import ipaddress
DIGITS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def connect(address: str = '127.0.0.1', port: int = 5040):
    try:
        ipaddress.ip_address(address)
        print('Adress is IPv4. Valid! continuing...')
    except ValueError:
        try:
            socket.gethostbyname(address)
            print('Adress is Hostname. Valid! continuing...')
        except socket.error:
            raise ValueError('Adress not Valid!')
    net = socket.socket()
    print(f'Connecting to {address}:{str(port)}')
    net.connect((address, port))
    print('Connected')
    return net

