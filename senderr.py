
from socket import *
from assymetric_exchange import AsymmetricEncryption
from chunk import *
from protocol import *
from symmetric import *
from assymetric_exchange import *

servername= 'localhost'
serverport = 5001
windowsize = 3

  

filename = input("Enter file name to send: ")
total=get_total_chunks(filename, 1024)

sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(0.5)

sym = SymmetricEncryption()
des_key = sym.key
handshake = Message_Format("HANDSHAKE", 0, des_key).encode()
sock.sendto(handshake.encode(), (servername, serverport))
aes_packet, addr = sock.recvfrom(2048)
aes_msg = Message_Format.decode(aes_packet)
if aes_msg and aes_msg.msg_type == "PUB":
    print("Received public key, encrypting symmetric key.")
    pub_key = aes_msg.data
    encrypted_key = AsymmetricEncryption.encrypt_key(des_key, pub_key)
    sock.sendto(encrypted_key, addr)
    print("Symmetric key sent, starting file transfer.")


base =0
next=0
ack_counter=0


try:
  while  next < total-1 or ack_counter < total-1:
    while next < base + windowsize and next < total:
        data=get_chunks_by_number(filename,next,1024)
        packet=Message_Format("DATA", next, data)
        packet_encoded = packet.encode()
        packet_encrypted = sym.encrypt(packet_encoded)
        sock.sendto(packet_encrypted, (servername, serverport))
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
    end_packet_encrypted = sym.encrypt(end_packet.encode())
    sock.sendto(end_packet_encrypted, (servername, serverport))
    print("closing socket")
    sock.close()

