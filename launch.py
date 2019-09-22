#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: <^[uuid]^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===========================Core Modules================================||
import sys, os
#===========================3rd Party Modules===========================||
#============================Pheonix Modules============================||
from pheonix.elements.config import config#								||
from pheonix.elements.thing import thing#								||
#==============================GUI Modules==============================||
from PyQt5.QtWidgets import QApplication
#=============================App Modules===============================||
import app, cfg, gui, style.qss
#================Common Globals=========================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
qss = os.path.join(here,'style/z-data_/pyffice.qss')#					||
#=======================================================================||
class spawn2(object):
	def __init__(self, cfg):
		'Spawn the Application'
		pxcfg = here+'z-data_/launch.yaml'
		if cfg == None:
			pass
			#create new config file for the current user and what ever file is trying to be opened if any
		self.config = config.instruct(pxcfg).load()#.override(cfg)
		self.ctrlServer()
		self.appService()
		self.mainDesktop()
		self.exit()
	def appService(self):
		''
		self.app = QApplication(self.config.select('Application'))#		||Start the App Container
		return self
	def _loadData(self):
		'load basic initial data from app tables to in memappdb and setup shared data db'

	def ctrlServer(self):
		''
		self.ctrlSrvr = run_nameserver()
		return self
	def mainDesktop(self):
		self.win = desktop.mainWindow(self.config.select('Desktop'))#	||
		self.win.show()
	def exit(self):
		sys.exit(app.exec_())
	#if not create a config file
		#ask about importing app file
		#if not create a new app db
		#create sample filedb with lots of example pyfiles
	#if config file exists
#	muliprocess
		#appfile....open the app file
			#spin up nameserver
			#check paths any connected filedbs
			#file tree is stored in the appdb
			#...somehow indicate this as not live...grey out
def spawn(cfg):
	'Spawn the Application'
	pxcfg = here+'z-data_/launch.yaml'
	spawnCFG = config.instruct(pxcfg).load()#override(cfg)
	app = QApplication(sys.argv)#			||Start the App Container
	aw = gui.mainWindow()#			||
	aw.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	cfg = {'args': sys.argv, 'user': thing.who()}
	spawn(cfg)
