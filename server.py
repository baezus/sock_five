import socket #this will be a TCP network
import hashlib #built-in python hash function library

port = 2346
s = socket.socket()
host = socket.gethostname()
s.bind((host, port))
s.listen(3)

print(f'Server listening ... on port {port}')
parser = hashlib.new('sha1')


while True:
    conn, addr = s.accept()
    print(f'Got connection from {addr}')
    data = conn.recv(4096)
    print(data)
    filename = "nicki.txt"
    f = open(filename, 'rb')
    l = f.read(4096)
    while (l):
        l = f.read(4096)
    parser.update(l)
    response = parser.hexdigest()
    conn.send(response.encode())
    f.close()

    conn.send('     '.encode())
    conn.send(filename.encode())
    print(f'Done sending {filename}.')
    conn.close()

s.close()