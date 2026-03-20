import zlib

class Message_Format:
    def __init__(self, msg_type, seqnum, data):
        self.msg_type =msg_type
        self.seqnum = seqnum
        self.data = data
        
        
    def encode(self):
        # Create the header as bytes
        header = f"{self.msg_type}|{self.seqnum}|".encode()
    # Concatenate bytes with bytes
        pack = header + self.data 
        checksum = str(zlib.crc32(pack)).encode() # Encode checksum to bytes

        return pack + b'|' + checksum



    @staticmethod
    def decode(packet):
        try:
            # Split into 4 parts max: type | seqnum | data | checksum
            parts = packet.split(b'|', 3)
            msg_type = parts[0].decode()
            seqnum = int(parts[1])
            data = parts[2]
            checksum_received = parts[3]

            # Compute checksum over "type|seqnum|data"
            checksum_calc = str(zlib.crc32(
                parts[0] + b'|' + parts[1] + b'|' + parts[2]
            )).encode()

            if checksum_calc == checksum_received:
                return Message_Format(msg_type, seqnum, data)
            else:
                return None
        except Exception:
            return None

      
  


