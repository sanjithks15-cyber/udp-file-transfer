
from socket import *
from chunk import *
from protocol import *

servername= 'localhost'
serverport = 5001
windowsize = 3

  

filename = "file.txt"
total=get_total_chunks(filename, 1024)

sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(0.5)

base =0
next=0

while next < total:
    while next < base + windowsize and next < total:
        data=get_chunks_by_number(filename,next,1024)
        packet=Message_Format("DATA", next, data)
        sock.sendto(packet.encode(), (servername, serverport))
        print(f"Sent chunk {next}")
        next =next+1

try:
    ack_packet,addr=sock.recvfrom(1024)
    if ack_packet.msg_type == "ACK":
        print(f"Received ACK for chunk {ack_packet.seqnum}")
        base = ack_packet.seqnum + 1
except timeout:
    print(f"timeout sending chunk {base} again")
    next=base  

sock.close()

