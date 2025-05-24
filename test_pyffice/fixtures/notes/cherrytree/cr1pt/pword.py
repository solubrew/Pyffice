# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: cr1pt PWord
	description: >

	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from base64 import urlsafe_b64encode
# ======================================3rd Party Library Modules=====================================================||
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# ======================================Solutions Brewer Library Modules==============================================||
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'pword.yaml')


def create_private_fernet_key():
	"""
	:return: A new private key for Fernet symmetric encryption.
	:rtype: bytes
	"""
	return Fernet.generate_key()


def decrypt_fernet(message, key):
	"""
	:param message: The encrypted message that needs to be decrypted; it should be a byte string.
	:param key: The key used for the decryption; it should be a byte string.
	:return: The decrypted plain text message as a string.
	"""
	cipher_suite = Fernet(key)
	plain_text = cipher_suite.decrypt(message)
	return plain_text.decode()


def encrypt_fernet(message, key):
	"""
	:param message: The plaintext message to be encrypted. It can be either a string or bytes.
	:param key: The key used for encryption, it should be a URL-safe base64-encoded 32-byte key.
	:return: The encrypted message as bytes.
	"""
	cipher_suite = Fernet(key)
	if isinstance(message, str):
		message = message.encode()
	cipher_text = cipher_suite.encrypt(message)
	return cipher_text


def password_key(password, salt):
	"""
	:param password: The user's password that needs to be encoded.
	:param salt: The cryptographic salt used in the key derivation process to ensure uniqueness.
	:return: The derived key encoded in a URL-safe base64 format.
	"""
	if isinstance(salt, str):
		salt = salt.encode()
	if isinstance(password, str):
		password = password.encode()
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),	length=32, salt=salt, iterations=100000,)  # generate key
	return urlsafe_b64encode(kdf.derive(password))


def decrypt_password(message, pword, salt):
	"""
	:param message: The encrypted message that needs to be decrypted.
	:param pword: The password used to generate the decryption key.
	:param salt: The salt value used in conjunction with the password to generate the decryption key.
	:return: The decrypted message.
	"""
	key = password_key(pword, salt)
	return decrypt_fernet(message, key)


def encrypt_password(message, pword, salt):
	"""
	:param message: The plaintext message that needs to be encrypted.
	:param pword: The password used to derive the encryption key.
	:param salt: A unique value used to ensure the derived key is unique.
	:return: The encrypted message as a byte string.
	"""
	key = password_key(pword, salt)
	return encrypt_fernet(message, key)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
