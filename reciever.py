
from socket import *
from time import sleep
from protocol import Message_Format
from symmetric import *
from assymetric_exchange import *

serverport = 5001
serversocket= socket(AF_INET, SOCK_DGRAM)
serversocket.bind(('',serverport) )
print("server is running")

asym = assymetrric_encryption()
public_key = asym.generate_keys()
handshake , addr = serversocket.recvfrom(2048)
handshake_msg = Message_Format.decode(handshake)
if handshake_msg and handshake_msg.msg_type == "HANDSHAKE":
     print("Received handshake, sending public key.")
     
     pub_key_packet = Message_Format("PUB", 0, public_key).encode()
     serversocket.sendto(pub_key_packet, addr)
     encrypted_key, addr = serversocket.recvfrom(2048)
     aes_key = asym.decrypt_key(encrypted_key)
     sym = SymmetricEncryption(aes_key)
     sym_key = sym.key
     print("Symmetric key established, ready to receive file.")


expected_seqnum = 0
filename = "received_file.bin"
try:
  with open(filename, 'wb') as fs:


   while True:
         packet, addr = serversocket.recvfrom(2048)
         
         packet_decrypted = sym.decrypt(packet)
         message = Message_Format.decode(packet_decrypted)
         
         if message is None:
              print("Dropped corrupted packet (Checksum mismatch).")
              continue
         if message.msg_type == "END":
              print("Received END signal, closing connection.")
              break
         if message.msg_type == "DATA" and message.seqnum == expected_seqnum:
              fs.write(message.data)
              print(f"Received chunk {message.seqnum}")
              
              ack_packet = Message_Format("ACK", message.seqnum, b'')
              serversocket.sendto(ack_packet.encode(), addr)
              print(f"Sent ACK for chunk {message.seqnum}")
              
              expected_seqnum += 1
         else:
              print(f"Received out-of-order chunk {message.seqnum}, expected {expected_seqnum}")
              ack_resend = Message_Format("ACK", expected_seqnum - 1, b'')
              serversocket.sendto(ack_resend.encode(), addr)
finally:
    print("File received successfully.")
    
    serversocket.close()  









   

