from cryptography.fernet import Fernet
import util

config = util.parse_config()
key = config['encryption']['key']


def encrypt(data):
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(encrypted):
    f = Fernet(key)
    return f.decrypt(encrypted)