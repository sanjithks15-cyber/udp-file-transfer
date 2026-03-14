
from socket import *
from chunk import *
from protocol import *

servername= 'localhost'
serverport = 5001
sock = socket(AF_INET, SOCK_DGRAM)

filename = input("Enter file name: ")
chunk = get_chunks(filename,1024)


sock.sendto(chunk.encode(), (servername, serverport))

ACK ,address = sock.recvfrom(1024)
print(ACK.decode())

sock.close()

