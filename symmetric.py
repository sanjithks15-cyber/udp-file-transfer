
from cryptography.fernet import Fernet

class SymmetricEncryption:
    def __init__(self , key=None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)
        
    def encrypt(self,data):
        return self.cipher.encrypt(data)

    def decrypt(self,data):
        if not isinstance(data, bytes):
            raise ValueError("Data must be bytes")

        return self.cipher.decrypt(data)
    
