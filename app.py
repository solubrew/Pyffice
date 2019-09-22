#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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
#=======================================================================||
import sys, os
import random
import matplotlib
matplotlib.use("Qt5Agg")
#=======================================================================||
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#=======================================================================||
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QMessageBox
from PyQt5.QtWidgets import QWidget, QToolBar, QFileSystemModel
from PyQt5.QtWidgets import QTreeView, QWidget, QBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QToolButton, QMainWindow, QAction
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtWidgets import QTextEdit, QMenu, QTabWidget, QLabel, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QDir
#=======================================================================||
from pheonix.elements.config import config#								||
#================Common Globals=========================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class prime(QWidget):
	def __init__(self, cfg=None):
		pxcfg = here+'z-data_/app.yaml'
		self.config = config.instruct(pxcfg).override(cfg)#				||
		super().__init__()
		self.title = ''
		self.left = 20
		self.top = 50
		self.width = 1650
		self.height = 960
		self.initUI()
	def initUI(self):
		''
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.createTabArea()
	def createTabArea(self, tabs):
		'implement tabs model'
		self.tabs = QTabWidget()
		cnt = 0
		for tab in tabs.keys():
			node = self.config['nodes'][tab['type']]()
			name = tab['name'] if not None else 'tab'+str(cnt)
			self.tab.addTab(table.tableWidget, name)
		doc = self.createWorkCanvas()
		self.tab.addTab(doc.canvas, "Tab 2")
		self.tab.addTab(doc.canvas, "+")
		self.tab.setTabPosition(QTabWidget.South)
		cnt += 1
		return self
	def table(self):
		''
		self.table = QTableWidget()

		return self
class dataRTR(object):#													||
	'Distribute Data between the inMemory DB and persistent Stores'
	def __init__(self, nameserver, cfg=None):#							||
		'Data Router'#							||
		self.config = config.instruct(pxcfg).override(cfg)#				||
		self.nameserver = nameserver#									||
		self.queue = queue.Queue()#										||
		self.go = True#													||
		self.listen()
	def listen(self):
		''
		wati = 0
		while self.go == True:
			poll()
			if response == None and wait < 5000:
				wait += 0.1
			else:
				wait = 0
			time.sleep(wait)
	def getQueue(self):
		''
		return self.queue
	def writeQueue(self):
		''
		self.queue.write()
	def processQue(self):
		#need to be very careful about the use of parallel processing here
		#if possible take advantage for speed but becareful and error to safe side
		self.pool = mp.Pool()
		while task in self.queue:
			self.runAction(task)
	def runAction(self, task):
		obj = getattr(self, task['how'])
		self.status[task['id']] = obj(task)
		return self
	def genSQLCMD(self):
		''
		cmd = sonql.doc()
		return self
	def mapTables(self):
		''
		#get dbs from nameserver
		return self






