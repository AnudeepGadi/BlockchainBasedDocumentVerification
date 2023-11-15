from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes
from server.config import settings
import secrets
import string
from tinyec import registry
import secrets


def encrypt(plain_text, passphrase=settings.passphrase):
    salt = get_random_bytes(AES.block_size)
    private_key = hashlib.scrypt(
        passphrase.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32
    )
    cipher_config = AES.new(private_key, AES.MODE_GCM)
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt(enc_dict, passphrase):
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    private_key = hashlib.scrypt(
        passphrase.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted


def generate_passphrase(size=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(size))


def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y)

def decompress(curve,compressed):
    keys = compressed.split('0x')
    return registry.ec.Point(curve,int(keys[1],16),int(keys[2],16))

def generate_shared_secret(sender_private_key, receiver_public_key):
    curve = registry.get_curve(settings.ecc_curve)
    return compress(int(sender_private_key) * decompress(curve,receiver_public_key))
