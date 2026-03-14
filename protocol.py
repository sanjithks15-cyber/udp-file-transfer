class Message_Format:
    def __init__(self, msg_type, seqnum, data):
        self.msg_type =msg_type
        self.seqnum = seqnum
        self.data = data
        
        
    def encode(self):
        header = f"{self.msg_type}|{self.seqnum}|"
        return header.encode() + self.data


    @staticmethod   
    def decode(packet):
          parts = packet.split(b'|', 3)
          msg_type = parts[0].decode()
          seqnum = int(parts[1])
          total = int(parts[2])
          data = parts[3]

          return Message_Format(msg_type, seqnum, total, data)





