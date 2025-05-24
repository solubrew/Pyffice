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
from os.path import abspath, dirname, join
import datetime as dt
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

from cr1pt.rsa import encrypt_rsa, decrypt_rsa
from cr1pt.rsa import create_public_private_rsa_keys

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', '.yaml')


def test_create_public_private_rsa_key():
	""""""
	keysize = 4096
	public_pem, private_pem, public_key, private_key = create_public_private_rsa_keys(keysize, 65537, True)
	assert public_pem != private_pem
	assert public_key != private_key

	public_numbers = public_key.public_numbers()
	modulus = public_numbers.n
	assert modulus.bit_length() == keysize

	given_message = """Check this encryption"""
	encrypted_message = encrypt_rsa(given_message, public_pem)
	#TODO: how to determine if the encryption is done correctly
	message = decrypt_rsa(encrypted_message, private_pem)
	assert message == given_message


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
