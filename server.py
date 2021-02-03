import socket #this will be a TCP network
import hashlib #built-in python hash function library
import re 

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

    # This receives the algorithm passed into the client
    data = conn.recv(8)
    decoded = data.decode('utf-8')
    algo_slice = decoded[0:6][2:]
    print(algo_slice)

    # This receives the list of filenames passed into the client.
    filenames_slice = conn.recv(4096)
    remainder = filenames_slice.decode()
    remainder = re.findall(r'"([^"]*)"', remainder)
    for idx, value in enumerate(remainder):
        print(remainder[idx])

    # This begins the file reading process
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