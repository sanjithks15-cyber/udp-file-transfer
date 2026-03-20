
from socket import *
from chunk import *
from protocol import *

servername= 'localhost'
serverport = 5001
windowsize = 3

  

filename = input("Enter file name to send: ")
total=get_total_chunks(filename, 1024)

sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(0.5)

base =0
next=0
ack_counter=0
try:
  while  next < total-1 or ack_counter < total-1:
    while next < base + windowsize and next < total:
        data=get_chunks_by_number(filename,next,1024)
        packet=Message_Format("DATA", next, data)
        sock.sendto(packet.encode(), (servername, serverport))
        print(f"Sent chunk {next}")
        next =next+1

    try:
        ack_packet,addr=sock.recvfrom(1024)
        ack = Message_Format.decode(ack_packet)
        ack_counter = ack.seqnum
        if ack.msg_type == "ACK" and ack.seqnum >= base:
          print(f"Received ACK for chunk {ack.seqnum}")
          base = ack.seqnum + 1
    except timeout:
        print(f"timeout sending chunk {base} again")
        next=base  
finally:
    end_packet = Message_Format("END", 0, b'')
    sock.sendto(end_packet.encode(), (servername, serverport))
    print("closing socket")
    sock.close()

