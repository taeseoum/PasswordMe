import hashlib
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class MasterKey:
    SALT_PATH = "salt.dat"
    KEY_HASH_PATH = "key_hash.dat"

    def __init__(self, master_password):
        self.master_password = master_password.encode()
        if not os.path.exists(self.SALT_PATH):
            self.salt = os.urandom(16)
            with open(self.SALT_PATH, "wb") as f:
                f.write(self.salt)
        else:
            with open(self.SALT_PATH, "rb") as f:
                self.salt = f.read()
        self.key = self.derive_key()
        
        # Check if hash exists and verify
        if os.path.exists(self.KEY_HASH_PATH):
            with open(self.KEY_HASH_PATH, "rb") as f:
                stored_key_hash = f.read()
            if self.hash_key(self.key) != stored_key_hash:
                raise ValueError("Incorrect master password!")
        else:
            with open(self.KEY_HASH_PATH, "wb") as f:
                f.write(self.hash_key(self.key))

    def derive_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.master_password)

    @staticmethod
    def hash_key(key):
        return hashlib.sha256(key).digest()
