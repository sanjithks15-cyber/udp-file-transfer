
from socket import *
from protocol import Message_Format
from symmetric import *
from assymetric_exchange import *

serverport = 5001
serversocket = socket(AF_INET, SOCK_DGRAM)
serversocket.bind(('', serverport))
print("server is running")

clients = {}

while True:
    try:
        packet, addr = serversocket.recvfrom(2048)
    except ConnectionResetError:
        # Windows may raise this on UDP when peer closes; keep listening.
        continue
    except Exception as e:
        print("recvfrom error:", e)
        continue

    if addr not in clients:
        # New client: process handshake
        handshake_msg = Message_Format.decode(packet)
        if handshake_msg and handshake_msg.msg_type == "HANDSHAKE":
            asym = AsymmetricEncryption()
            public_key = asym.generate_keys()
            clients[addr] = {
                'asym': asym,
                'pub_key': public_key,
                'state': 'sent_pub'
            }
            pub_key_packet = Message_Format("PUB", 0, public_key).encode()
            serversocket.sendto(pub_key_packet, addr)
            print("Received handshake, sending public key.")
    else:
        client = clients[addr]
        
        if client['state'] == 'sent_pub':
            # Expect encrypted key
            encrypted_key = packet
            aes_key = client['asym'].decrypt_key(encrypted_key)
            sym = SymmetricEncryption(aes_key)
            client['sym'] = sym
            client['expected_seqnum'] = 0
            client['filename'] = f"received_file_{addr[0]}_{addr[1]}.bin"
            client['file'] = open(client['filename'], 'wb')
            client['state'] = 'receiving'
            print("Symmetric key established, ready to receive file.")
        
        elif client['state'] == 'receiving':
            packet_decrypted = client['sym'].decrypt(packet)
            message = Message_Format.decode(packet_decrypted)
            
            if message is None:
                print("Dropped corrupted packet (Checksum mismatch).")
                continue
            if message.msg_type == "END":
                print("Received END signal, closing connection.")
                client['file'].close()
                client['state'] = 'done'
                del clients[addr]
                continue
            if message.msg_type == "DATA" and message.seqnum == client['expected_seqnum']:
                client['file'].write(message.data)
                print(f"Received chunk {message.seqnum}")
                ack_packet = Message_Format("ACK", message.seqnum, b'')
                serversocket.sendto(ack_packet.encode(), addr)
                print(f"Sent ACK for chunk {message.seqnum}")
                client['expected_seqnum'] += 1
            else:
                print(f"Received out-of-order chunk {message.seqnum}, expected {client['expected_seqnum']}")
                ack_resend = Message_Format("ACK", client['expected_seqnum'] - 1, b'')
                serversocket.sendto(ack_resend.encode(), addr)  









   

