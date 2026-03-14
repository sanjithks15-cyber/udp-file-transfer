
from socket import *
serverport = 5001
serversocket= socket(AF_INET, SOCK_DGRAM)
serversocket.bind(('',serverport) )
print("server is running")

while True:
    data, addr = serversocket.recvfrom(1024)
    print("Received:", data.decode())
    reply = "ACK"
    serversocket.sendto(reply.encode(), addr)








   

