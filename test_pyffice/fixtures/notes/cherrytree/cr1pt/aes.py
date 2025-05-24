# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from base64 import b64encode

# ======================================3rd Party Library Modules=====================================================||
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from pandas import Series

# ======================================Solutions Brewer Library Modules==============================================||
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'aes.yaml')


def create_symmetric_key(keysize=32, threshold=0.5):
	"""Create a random symmetric key of given size.
		this threshold actually reduces the namespace of the key
	"""
	key = get_random_bytes(keysize)
	# while True:
	# 	key = get_random_bytes(keysize)
	# 	dsle = DataListEvaluation(Series(list(b64encode(key).decode('utf-8'))))
	# 	if dsle.is_random(threshold):
	# 		break
	return key


def encrypt_aes(msg, key, encoding='utf-8'):
	"""Encrypt a message using AES-GCM."""
	if isinstance(msg, str):
		msg = msg.encode(encoding)
	aes_cipher = AES.new(key, AES.MODE_GCM)
	ciphertext, auth_tag = aes_cipher.encrypt_and_digest(msg)
	return ciphertext, aes_cipher.nonce, auth_tag


def decrypt_aes(ciphertext, nonce, auth_tag, key, encoding='utf-8'):
	"""Decrypt a message using AES-GCM."""
	aes_cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
	message = aes_cipher.decrypt_and_verify(ciphertext, auth_tag)
	return message.decode(encoding)


# ====================================================================================================================||
"""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os


# Function to encrypt data
def encrypt(key, plaintext):
	iv = os.urandom(16)  # Initialization Vector should be random
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	encryptor = cipher.encryptor()

	# Padding plaintext to be a multiple of block size
	padder = padding.PKCS7(algorithms.AES.block_size).padder()
	padded_plaintext = padder.update(plaintext) + padder.finalize()

	ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
	return iv + ciphertext  # Return IV and ciphertext combined


# Function to decrypt data
def decrypt(key, ciphertext):
	iv = ciphertext[:16]  # Extract Initialization Vector
	actual_ciphertext = ciphertext[16:]

	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	decryptor = cipher.decryptor()

	padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

	# Unpadding the plaintext
	unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
	plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

	return plaintext


# Generate a random byte key
byte_key = os.urandom(32)  # 256-bit key

# Encode the byte key to a Base64 string
base64_key = base64.b64encode(byte_key).decode('utf-8')
print(f"Base64 Encoded Key: {base64_key}")

# Decode the Base64 string back to bytes
decoded_byte_key = base64.b64decode(base64_key)

plaintext = b"Secret Message!"

# Encrypt the message
ciphertext = encrypt(decoded_byte_key, plaintext)
print(f"Encrypted: {ciphertext}")

# Decrypt the message
decrypted_message = decrypt(decoded_byte_key, ciphertext)
print(f"Decrypted: {decrypted_message}")




from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


# Function to encrypt data
def encrypt(key, plaintext):
	iv = os.urandom(16)  # Initialization Vector should be random
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	encryptor = cipher.encryptor()

	# Padding plaintext to be a multiple of block size
	padder = padding.PKCS7(algorithms.AES.block_size).padder()
	padded_plaintext = padder.update(plaintext) + padder.finalize()

	ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
	return iv + ciphertext  # Return IV and ciphertext combined


# Function to decrypt data
def decrypt(key, ciphertext):
	iv = ciphertext[:16]  # Extract Initialization Vector
	actual_ciphertext = ciphertext[16:]

	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	decryptor = cipher.decryptor()

	padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

	# Unpadding the plaintext
	unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
	plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

	return plaintext


# Example usage
key = os.urandom(32)  # 256-bit key; you can also use 16 or 24 bytes for 128-bit or 192-bit keys
plaintext = b"Secret Message!"

# Encrypt the message
ciphertext = encrypt(key, plaintext)
print(f"Encrypted: {ciphertext}")

# Decrypt the message
decrypted_message = decrypt(key, ciphertext)
print(f"Decrypted: {decrypted_message}")




"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
