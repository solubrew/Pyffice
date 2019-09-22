#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: <^(UUID)^>
	name:
	description: >
		Define a top level desktop layout with connections to
		available toolbars and core applications that can be
		loaded into the main widgets of the desktop
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
from pheonix.organisms.monk import monk
#==============================GUI Modules==============================||
from PyQt5.QtWidgets import QMainWindow, QMenu, QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy, QMessageBox
from PyQt5.QtWidgets import QWidget, QToolBar, QFileSystemModel
from PyQt5.QtWidgets import QTreeView, QWidget, QBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QToolButton, QMainWindow, QAction
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtWidgets import QTextEdit, QMenu, QTabWidget, QLabel, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
#=============================App Modules===============================||
import app
#================Common Globals=========================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
qss = os.path.join(here,'style/z-data_/pyffice.qss')#					||
#=======================================================================||
class mainWindow(QMainWindow):#											||
	def __init__(self):#												||
		QMainWindow.__init__(self)#										||
		pxcfg = here+'/gui.yaml'
		self.config = monk.stone(pxcfg).
		self.setAttribute(Qt.WA_DeleteOnClose)#							||
		self.setWindowTitle("Pyffice 0.0.0.0.0.0")#						||
		self.setStyleSheet(open(qss, "r").read())#						||
		self.setAutoFillBackground(True)#								||
		self.loadMenu()#												||
		self.setLayout()#												||
		self.loadApp()#													||
	def buildMenu():
		pass
	def desktopMenu(self, application, cfg=None):
		#dynamically build menu from config file
		dtmcfg = self.config['menu']
		for item in cfg.keys():
			self.menu = QMenu(dtmcfg[item]['name'], application)
	def loadMenu(self):#												||
		menu = self.desktopMenu(self)# this sends the desktop object (self) to the menu object
		for mu in menu.__dir__():#										||dynamically add
			obj = getattr(menu, mu)#									||menu items to the
			if isinstance(obj, QMenu):#									||layout
				self.menuBar().addMenu(obj)#							||
	def setLayout(self):#												||
		self.main_widget = QWidget(self)
		self.l = QHBoxLayout(self.main_widget)
#		tbar = docAddBar()
#		l.addWidget(tbar.toolbar)
	def loadApp(self):#													||
		''
		app = alpr.App()
		self.formulaBar()
		self.createLayout()
		self.l.addWidget(app)
		self.main_widget.setFocus()
		self.setCentralWidget(self.main_widget)
		windowLayout = QBoxLayout(QBoxLayout.LeftToRight)
		self.treeview.setFixedWidth=200
		windowLayout.addWidget(self.treeview)
		windowLayout.addWidget(self.tabwidget)
		self.setLayout(windowLayout)
		self.show()
		return self
		self.functionBar = QToolBar()
		self.addToolBar(self.functionBar)
		self.functionInput = QLineEdit()
		self.functionBar.addWidget(self.functionInput)
		self.formulaBar = QToolBar()
		self.addToolBar(self.formulaBar)
		self.formulaInput = QLineEdit()
		self.formulaBar.addWidget(self.formulaInput)
		self.statusBar().showMessage('Pyffice is about to Live')
	def fileQuit(self):
		self.close()
	def closeEvent(self, ce):
		self.fileQuit()

	def treeView(self,):
		self.treeview = QTreeView()
		self.treeview.setModel(model)

		self.treeview.setRootIndex(model.index(QDir.homePath()))

		self.treeview.setColumnWidth(0,50)
		self.treeview.setColumnHidden(1, True)
		self.treeview.setColumnHidden(2, True)
		self.treeview.setColumnHidden(3, True)
		self.treeview.setFixedWidth(200)
		self.treeview.setAnimated(False)
		self.treeview.setIndentation(20)
		self.treeview.setSortingEnabled(True)
		return self
	def setupContextMenu(self):
		'I believe this should setup the right click menu'
		self.addAction(self.cell_addAction)
		self.addAction(self.cell_subAction)
		self.addAction(self.cell_mulAction)
		self.addAction(self.cell_divAction)
		self.addAction(self.cell_sumAction)
		self.addAction(self.firstSeparator)
		self.addAction(self.colorAction)
		self.addAction(self.fontAction)
		self.addAction(self.secondSeparator)
		self.addAction(self.clearAction)
		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		return self
	def formulaBar(self):
		return self
	def functionBar(self):
		return self

class sample(object):
	def __init__(self):
		vars(self)['a'] = 10
		s = sample()
		print (s.a)
class Record(object):
	def __init__(self):
		r = Record()
		r.foo = 'oof'
		setattr(r, 'bar', 'rab')
		r.foo
		'oof'
		r.bar
		'rab'
		names = 'id description price'.split()
		values = [666, 'duct tape', 3.45]
		s = Record()
		for name, value in zip(names, values):
			setattr(s, name, value)
		s.__dict__ # If you are suffering from dict withdrawal symptoms
		{'price': 3.45, 'id': 666, 'description': 'duct tape'}
		return self
	def appToolBar(self, QToolBar, cfg):
		'Create a Toolbar from configurations file'
		pxcfg = here+'z-data_/desktop.yaml'
		self.config = config.instruct(pxcfg).select(
								'docAddToolBar').override(cfg)#	||
		self.createToolBar()
		for button, cfg in self.config['buttons'].items():
			self.createButton(button, cfg)
	def createToolBar(self):
		self.toolbar = QToolBar()
		self.toolbar.setMovable(True)
		self.toolbar.setFloatable(True)
		self.toolbar.setOrientation(Qt.Vertical)
		return self
	def createButton(self, button, cfg):
		''
		toolbutton = QToolButton()
		toolbutton.setText(cfg['DisplayName'])
		toolbutton.setCheckable(cfg['checkable'])
		toolbutton.setAutoExclusive(cfg['setAutoExclusive'])
		self.toolbar.addWidget(toolbutton)
		return self
