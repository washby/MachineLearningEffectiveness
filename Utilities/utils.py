import base64
import re

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_course_level(course_json_object):
    try:
        crs = course_json_object['course_code']
        pattern = r'[a-zA-Z\-]{2,4}(\d)\d{3}'
        matches = re.findall(pattern, crs)
        matches = list(set(matches))
        if len(matches) == 0:
            return -1
        if len(matches) == 1:
            return matches[0]
        result = min([int(x) for x in matches])
        # print(f'---------->Multi levels {matches} on {crs}\n--> so result is {result}')
        return result
    except KeyError:
        pass
    return -1


def encrypt(message, salt, pw):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())


def decrypt(message, salt, pw):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
    fernet = Fernet(key)
    return fernet.decrypt(message).decode()
