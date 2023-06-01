import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption:
    def __init__(self, salt, pw):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=100000
        )
        self.__key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
        self.__fernet = Fernet(self.__key)

    def encrypt(self, message):
        message = str(message)
        return self.__fernet.encrypt(message.encode())

    def decrypt(self, message):
        if isinstance(message, bytes):
            return self.__fernet.decrypt(message).decode()

        message = bytes(str(message)[2:], 'utf-8').decode()
        return self.__fernet.decrypt(message).decode()
