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
from secrets import token_bytes
import hashlib

# ======================================3rd Party Library Modules=====================================================||
from coincurve import PublicKey
from ecdsa import SigningKey, SECP256k1
import base58
from Crypto.Hash import keccak

# ======================================Solutions Brewer Library Modules==============================================||
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'signatures.yaml')


def create_public_private_sha3_keys():
	"""
	Generate a pair of public and private keys using the Keccak (SHA-3) hashing algorithm.

	:return: A tuple containing the private key and the corresponding address, both in hexadecimal format.
	"""
	pkey = hashlib.sha3_256(token_bytes(32)).digest()
	public = PublicKey.from_valid_secret(pkey).format(compressed=True)[1:]
	addr = hashlib.sha3_256(public).digest()[-20:].hex()
	return pkey.hex(), addr


def create_public_private_keccak_keys():
	"""
	Generate a pair of public and private keys using the Keccak (SHA-3) hashing algorithm.

	:return: A tuple containing the private key and the corresponding address, both in hexadecimal format.
	"""
	# Generate private key
	private_key = SigningKey.generate(curve=SECP256k1)
	private_key_bytes = private_key.to_string()
	private_key_hex = private_key_bytes.hex()

	# Derive public key
	public_key = private_key.verifying_key
	public_key_bytes = public_key.to_string()

	# Compress the public key
	public_key_compressed = (b'\x02' + public_key_bytes[32:]) if public_key_bytes[32] % 2 == 0 else (b'\x03' + public_key_bytes[32:])
	return private_key_hex, public_key_compressed.hex()

def convert_keccak_publickey_to_address(compressed_public_key):
	""""""
	# Hash the public key using Keccak-256
	if isinstance(compressed_public_key, str):
		compressed_public_key = bytes.fromhex(compressed_public_key)
	k = keccak.new(digest_bits=256)
	k.update(compressed_public_key)
	public_key_keccak_hash = k.digest()
	return f"0x{public_key_keccak_hash[-20:].hex()}"


def convert_sha3_publickey_to_address(compressed_public_key):
	"""
	:param compressed_public_key: A byte string representing the compressed public key.
	:return: A Base58 encoded Bitcoin address corresponding to the given compressed public key.
	"""
	if isinstance(compressed_public_key, str):
		compressed_public_key = bytes.fromhex(compressed_public_key)
	digest = hashlib.sha256(compressed_public_key).digest()
	pubkey_hash = hashlib.new('ripemd160', digest).digest()
	version = b'\x00'  # mainnet 	# Prepend the version byte (0x00 for mainnet, 0x6f for testnet)
	pubkey_hash = version + pubkey_hash
	checksum = hashlib.sha256(hashlib.sha256(pubkey_hash).digest()).digest()[:4] 	# Calculate the double-SHA256 checksum
	address_bin = pubkey_hash + checksum 	# Add the 4 checksum bytes from stage 7 at the end of extended RIPEMD-160 hash from stage 4.
	return base58.b58encode(address_bin).decode('ascii')


def verify_sha3_signature(address, private_key_hex):
	"""
	:param address: The address to be verified.
	:param private_key_hex: The private key in hexadecimal format.
	:return: Returns True if the address is verified against the private key, otherwise False.
	"""
	private_key = bytes.fromhex(private_key_hex)  # Convert private key to bytes
	signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
	public_key = signing_key.verifying_key.to_string()
	public_key_compressed = b'\x02' + public_key[32:] if public_key[32] % 2 == 0 else b'\x03' + public_key[32:]
	converted_key = convert_sha3_publickey_to_address(public_key_compressed)
	if address == converted_key:
		return True
	logma.info(f"Address: {address} != {converted_key}")
	return False


def verify_keccak_signature(address, private_key_hex):
	"""
	:param address: The address to be verified.
	:param private_key_hex: The private key in hexadecimal format.
	:return: Returns True if the address is verified against the private key, otherwise False.
	"""
	private_key = bytes.fromhex(private_key_hex)  # Convert private key to bytes
	signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
	public_key = signing_key.verifying_key.to_string()
	public_key_compressed = b'\x02' + public_key[32:] if public_key[32] % 2 == 0 else b'\x03' + public_key[32:]
	converted_key = convert_keccak_publickey_to_address(public_key_compressed)
	if address == converted_key:
		return True
	logma.info(f"Address: {address} != {converted_key}")
	return False

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
