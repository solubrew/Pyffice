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
crow.crowLoad('', 'DELTA')

from condor import condor
from ogma.logma import Logma
from squirl.objnql import txtonql

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
logma = Logma(__name__)
log = True

# ====================================================================================================================||
pxcfg = join(here, '_data_', '.yaml')

def run(args):
	""""""
	if args[1] == 'write':
		file_ = abspath(join(here, '../pyffice', 'utilities', '_data_', 'formulas.yaml'))
		logma.info(f'Read {file_}')
		dikt = condor.instruct(file_).load().dikt
		pyfile_ = abspath(join(here, '../pyffice', 'utilities', 'formulas.py'))
		logma.info(f'Write {pyfile_}')
		text = ''
		for key in dikt.keys():
			formula = dikt[key].get('formula', None)
			if formula is None or len(formula) < 4:
				text += f'''def {key.replace('.', '_').replace("'", '').strip()}():\n\t""""""\n\treturn\n\n'''
			else:
				text += f'''def {formula.replace('.', '_').replace('=', '').replace("'", '').strip()}:\n\t""""""\n\treturn\n\n'''
		txtonql.Doc(pyfile_).write(text)


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
