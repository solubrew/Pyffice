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

from cr1pt.pword import create_private_fernet_key, encrypt_fernet, decrypt_fernet, password_key, encrypt_password, \
	decrypt_password

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'pword.yaml')


def test_fernet_key():
	""""""
	key = create_private_fernet_key()
	assert key is not None
	given_message = """Check The Fernet Key"""
	encrypted_message = encrypt_fernet(given_message, key)
	assert encrypted_message != given_message, encrypted_message
	message = decrypt_fernet(encrypted_message, key)
	assert given_message == message, message


def test_password_key():
	""""""
	password = "password1234"
	salt = "salt"
	key = password_key(password, salt)
	assert key == b'-7XSpXv7zVhI2gxjtsu8Krrwcz0IukwezXE_9NquSKY=', key
	given_message = """Check The Password Key"""
	encrypted_message = encrypt_password(given_message, password, salt)
	assert encrypted_message != given_message, encrypted_message
	message = decrypt_password(encrypted_message, password, salt)
	assert message == given_message, message


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
