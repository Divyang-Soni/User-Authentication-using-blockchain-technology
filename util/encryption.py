from cryptography.fernet import Fernet
from util import util

config = util.parse_config()
key = Fernet.generate_key()


def encrypt(data):
    f = Fernet(key)
    return f.encrypt(str(data).encode())


def decrypt(encrypted):
    f = Fernet(key)
    return f.decrypt(encrypted).decode()
