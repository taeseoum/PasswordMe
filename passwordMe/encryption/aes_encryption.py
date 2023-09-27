from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from os import urandom


class AESEncryption:
    def __init__(self,key):
        self.key = key


    def encrypt(self, data):
        iv = urandom(12)
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Ensure data is encoded as bytes
        encrypted_data = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
        
        return (iv, encryptor.tag, encrypted_data)

    def decrypt(self, iv, tag, encrypted_data):
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decode decrypted byte-string back to string (unicode)
        return (decryptor.update(encrypted_data) + decryptor.finalize()).decode('utf-8')
