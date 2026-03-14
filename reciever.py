
from socket import *
from protocol import Message_Format

serverport = 5001
serversocket= socket(AF_INET, SOCK_DGRAM)
serversocket.bind(('',serverport) )
print("server is running")

expected_seqnum = 0
filename = "received_file.bin"
try:
  with open(filename, 'wb') as fs:


   while True:
         packet, addr = serversocket.recvfrom(2048)
         message = Message_Format.decode(packet)
         
         if message.msg_type == "DATA" and message.seqnum == expected_seqnum:
              fs.write(message.data)
              print(f"Received chunk {message.seqnum}")
              
              ack_packet = Message_Format("ACK", message.seqnum, b'')
              serversocket.sendto(ack_packet.encode(), addr)
              print(f"Sent ACK for chunk {message.seqnum}")
              
              expected_seqnum += 1
         else:
              print(f"Received out-of-order chunk {message.seqnum}, expected {expected_seqnum}")

finally:
    print("File received successfully.")
    serversocket.close()  









   

