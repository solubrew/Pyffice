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
from sys import argv
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
import crow
crow.crowLoad('Cr1pt', 'DELTA')

from condor import condor
from test_cr1pt.cr1pt.aesTEST import test_symmetric_key
from test_cr1pt.cr1pt.hmacTEST import test_create_hash
from test_cr1pt.cr1pt.keyringTEST import *
from test_cr1pt.cr1pt.pwordTEST import test_fernet_key, test_password_key
from test_cr1pt.cr1pt.rsaTEST import test_create_public_private_rsa_key
from test_cr1pt.cr1pt.signaturesTEST import test_keccak_signature, test_sha3_signature
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
logma = Logma(__name__)
log = True

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'runTest.yaml')

def run(args):
	"""Run individual tabs with mock data for development purposes"""
	if args[1] == 'aes' or args[1] == 'all':
		test_symmetric_key()

	if args[1] == 'hmac' or args[1] == 'all':
		test_create_hash()

	if args[1] == 'keyring' or args[1] == 'all':
		test_keyring_password()

	if args[1] == 'pword' or args[1] == 'all':
		test_fernet_key()
		test_password_key()

	if args[1] == 'rsa' or args[1] == 'all':
		test_create_public_private_rsa_key()

	if args[1] == 'signatures' or args[1] == 'all':
		test_keccak_signature()
		test_sha3_signature()


if __name__ == '__main__':
	start = dt.datetime.now()
	logma.info(f'Start {start}')
	run(argv)
	end = dt.datetime.now()
	logma.info(f'Start {start}')
	logma.info(f'End {end}')
	logma.info(f'End Duration {end - start}')

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
