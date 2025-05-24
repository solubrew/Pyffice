# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid: 06719761-798d-77aa-8000-d68c0b83e533
	name:
	description: >
		A simplified RSA implementation to leverage basic features along with other cryptography libraries in the cr1pt
		package.
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# ======================================Solutions Brewer Library Modules==============================================||
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'rsa.yaml')


def create_public_private_rsa_keys(keysize=4096, public_exponent=65537, return_verification=False):
	"""
	:param keysize: The size of the RSA key in bits (default: 4096)
	:param public_exponent: The public exponent value (default: 65537)
	:param return_verification: Flag indicating whether to return the key objects along with their PEM representations (default: False)
	:return: A tuple containing the public key and private key in PEM format. If return_verification is True, the tuple also includes the public and private key objects.
	"""
	private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
	private_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
											format=serialization.PrivateFormat.PKCS8,
											encryption_algorithm=serialization.NoEncryption())
	# Generate public key
	public_key = private_key.public_key()
	public_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
											format=serialization.PublicFormat.SubjectPublicKeyInfo)
	if return_verification:
		return public_pem, private_pem, public_key, private_key
	return public_pem, private_pem


def encrypt_rsa(message, public_pem, encoding='utf-8'):
	"""
	:param message: The plaintext message to be encrypted. Can be a string or bytes.
	:param public_pem: The public key in PEM format. This is used for encrypting the message.
	:param encoding: The character encoding to use if the message is a string. Defaults to 'utf-8'.
	:return: The encrypted message as bytes.
	"""
	if isinstance(message, str):
		message = message.encode(encoding)
	public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())
	encrypted_message = public_key.encrypt(message,
											padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
																			algorithm=hashes.SHA256(),
																			label=None)
	)
	return encrypted_message


def decrypt_rsa(message, private_pem, encoding='utf-8'):
	"""
	:param message: The encrypted message which needs to be decrypted.
	:param private_pem: The private key in PEM format used for decryption.
	:param encoding: The encoding format for the decrypted message, defaults to 'utf-8'.
	:return: The decrypted message as a string.
	"""
	private_key = serialization.load_pem_private_key(private_pem, password=None, backend=default_backend())
	decrypted_message = private_key.decrypt(message,
											padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
																			algorithm=hashes.SHA256(),
																			label=None)
	)
	return decrypted_message.decode(encoding)

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
