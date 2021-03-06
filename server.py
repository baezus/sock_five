import socket #this will be a TCP network
import hashlib #built-in python hash function library
import re 

hashStore = []
port = 2345
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
    filenames_slice = conn.recv(1024)
    remainder = filenames_slice.decode()
    remainder = re.findall(r'"([^"]*)"', remainder)
    for idx, value in enumerate(remainder): 
        print('working file: ', remainder[idx])
        filename = value

        f = open(filename, 'rb')
        l = f.read(1024)
        while (l):
            l = f.read(1024)
        parser.update(l)
        response = parser.hexdigest()
        conn.send(response.encode())
        conn.send('     '.encode())
        conn.send(filename.encode())
        print(f'Done sending {filename}.')    
        f.close()
    conn.close()
s.close()
