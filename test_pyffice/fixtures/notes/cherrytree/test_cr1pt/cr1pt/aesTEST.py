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
from base64 import b64encode

# ======================================3rd Party Library Modules=====================================================||
from pandas import Series

# ======================================Solutions Brewer Library Modules==============================================||
from cr1pt import aes
from eaglytics.evaluation import DataListEvaluation
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'aesTEST.yaml')


def test_symmetric_key():
	""""""
	keysize = 32
	key = aes.create_symmetric_key(keysize)
	assert len(key) == keysize

	# logma.info(f"Key Size Verified {key}")
	# dsle = DataListEvaluation(Series(list(b64encode(key).decode('utf-8'))))
	# assert dsle.is_random()

	logma.info("Key Randomness Verified")
	message = """Encrypt this message thoroughly"""
	encrypted_message, nonce, auth_tag = aes.encrypt_aes(message, key)

	decrypted_message = aes.decrypt_aes(encrypted_message, nonce, auth_tag, key)
	assert decrypted_message == message


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
