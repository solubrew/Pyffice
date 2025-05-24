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
from cr1pt.signatures import create_public_private_keccak_keys, convert_sha3_publickey_to_address, verify_sha3_signature
from cr1pt.signatures import verify_keccak_signature, convert_keccak_publickey_to_address

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = False
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'signatures.yaml')


def test_keccak_signature():
	""""""
	private, public = create_public_private_keccak_keys()
	if log: logma.info(f"Private: {private}")
	if log: logma.info(f"Public: {public}")
	assert public != private
	assert len(public) == 66, len(public)
	assert len(private) == 64, len(private)
	address = convert_keccak_publickey_to_address(public)
	if log: logma.info(f"Address: {address}")
	assert len(address) == 42, len(address)
	assert verify_keccak_signature(address, private)


def test_sha3_signature():
	""""""
	private, public = create_public_private_keccak_keys()
	if log: logma.info(f"Private: {private}")
	if log: logma.info(f"Public: {public}")
	assert public != private
	assert len(public) == 66, len(public)
	assert len(private) == 64, len(private)
	address = convert_sha3_publickey_to_address(public)
	if log: logma.info(f"Address: {address}")
	assert len(address) == 34, len(address)
	assert verify_sha3_signature(address, private)

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
