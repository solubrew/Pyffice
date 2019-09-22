#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: <(UUID)>
	name: <[document_name]>
	description: >
	version: <[version]>
	path: <[LEXIvrs]><[path]>.yaml
	outline: <[outline]>
	authority: <[authority]>
	security: <[seclvl]>
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import os, datetime as dt, pandas as pd, re#							||
import queue#															||
#=======================================================================||
import pyodbc as sql, sqlite3 as sql3#									||
from osbrain import run_nameserver, run_agent#							||
#=======================================================================||
from pheonix.elements.calcgen import text as calct#						||
from pheonix.elements.comm import comm#									||
from pheonix.elements.comm import log#									||
from pheonix.elements.config import config#								||
from pheonix.elements.exam import exam#									||
from pheonix.elements.rule import rule#									||
from pheonix.elements.thing import thing#								||
#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class colab(object):
	def __init__(self):

	def creBranch(self):
		'create a new branch for each edit'
		return self
	def sendBranch(self):
		''
		return self
	def receiveBranch(self):
		''
		return self
	def acceptBranch(self, auto=None):
		''
		return self
	def saveBranch(self):
		'Integrate branch into tree, add old tree section to branch and kill the branch'
		return self
	def pruneTree(self):
		'Cut off dead branches'
		return self
class message(object):
	def __init__(self):

	def send(self):
		''
		return self
	def receive(self):
		''
		return self
#==========================Source Materials=============================||
'''
<[source_links]>
'''
#============================:::DNA:::==================================||
'''
<(DNA)>:
	<(WT)>: 32
	<@[datetime]@>:
		<[class]>:
			version: <[active:.version]>
			test:
		description: >
			<[description]>
		work:
			- <@[work_datetime]@>
	<[datetime]>:
		here:
			version: <[active:.version]>
		test:
		description: >
			<[description]>
		work:
			- <@[work_datetime]@>
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||