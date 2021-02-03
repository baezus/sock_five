import socket
import sys 
import argparse
import json 

#Config for CLI options [port] and arguments [address, algorithm, files]
arg_parser = argparse.ArgumentParser(description='A network hashing server implementing hash functions: sha1, sha256, sha512, md5.')
arg_parser.add_argument('-port', metavar='port', type=int, action='store', default='2345', help='[Optional] Which port to access.')
arg_parser.add_argument('ip', metavar='ip', action='store', default='127.0.1.1', help='The server IP address to network on.')
arg_parser.add_argument('algorithm', metavar='algorithm', action='store', type=str, choices=['sha1', 'sha256', 'sha512', 'md5'], help='The hashing algorithm to use.')
arg_parser.add_argument('files', metavar='files', action='store', nargs=argparse.REMAINDER, help='The filenames of data to be hashed.')
args = arg_parser.parse_args()

#With those arguments in place, now open the socket.
s = socket.socket()
host = socket.getfqdn(args.ip)
port = args.port
print(f'Connecting to {args.ip}:{port}...')
s.connect((host, port))

#with the socket open, write data received over it into a new file.
arg_packet = json.dumps([args.algorithm])
print(arg_packet)
s.send(arg_packet.encode())

#Now send the file names over
file_packet = json.dumps([args.files])
print('File packet: ', file_packet)
s.send(file_packet.encode())


with open('readout.txt', 'wb') as f:
    while True:
          data = s.recv(4069)
          if not data:
              break
          f.write(data)
          f.write('\n'.encode())
    f.close()

with open('readout.txt', 'r') as fin:
    print(fin.read(), end="")


