#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: <^(UUID)^>
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
#=======================================================================||
from PyQt4.QtCore import Qt, QModelIndex, QAbstractItemModel
from node import Node
from PyQt4.QtGui import QApplication, QTreeView
from node import Node
from model import FileSystemTreeModel
#=======================================================================||
import app
#================Common Globals=========================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
qss = os.path.join(there,'beaver/ngynPyffice/pyffice/pyffice.qss')#		||
#=======================================================================||
class Node(object):
	def __init__(self, name, path=None, parent=None):
		super(Node, self).__init__()
		self.name = name
		self.children = []
		self.parent = parent
		self.is_dir = False
		self.path = path
		self.is_traversed = False
		if parent is not None:
			parent.add_child(self)
	def add_child(self, child):
		self.children.append(child)
		child.parent = self
	def insert_child(self, position, child):
		if position < 0 or position > self.child_count():
			return False
		self.children.insert(position, child)
		child.parent = self
		return True
	def child(self, row):
		return self.children
	def child_count(self):
		return len(self.children)
	def row(self):
		if self.parent is not None:
			return self.parent.children.index(self)
		return 0
class tableND(Node)
	def __init__(self):
		''
	def tableNode(self):
		self.table = QTableWidget()
		self.table.setRowCount(100)
		self.table.setColumnCount(25)
		self.table.move(0,0)
		return self
class textND(Node):
	def __init__(self):
		''
	def plain(self):
		''
		self.editor = QTextEdit()
		self.editor.setPlaceholderText("Apply Text Syntax Coloring")
		return self
	def rich(self):
		''
		self.editor = TextEdit()
		# Setup the QTextEdit editor configuration
		self.editor.setAcceptRichText(False)
		self.editor.setAutoFormatting(QTextEdit.AutoAll)
		self.editor.selectionChanged.connect(self.update_format)
		# Initialize default font size.
		font = QFont('Times', 12)
		self.editor.setFont(font)
		# We need to repeat the size to init the current format.
		self.editor.setFontPointSize(12)
		# self.path holds the path of the currently open file.
		# If none, we haven't got a file open yet (or creating new).
		self.path = None
		layout.addWidget(self.editor)
		return self
class treeND(QAbstractItemModel, Node):
	FLAG_DEFAULT = Qt.ItemIsEnabled | Qt.ItemIsSelectable
	def __init__(self, root, path='c:/', parent=None):
		super(FileSystemTreeModel, self).__init__()
		self.root = root
		self.parent = parent
		self.path = path
		# generate root node children
		for file in os.listdir(path):
			file_path = os.path.join(path, file)
			node = Node(file, file_path, parent=self.root)
			if os.path.isdir(file_path):
				node.is_dir = True
		# takes a model index and returns the related Python node
	def getNode(self, index):
		if index.isValid():
			return index.internalPointer()
		else:
			return self.root
		# check if the note has data that has not been loaded yet
	def canFetchMore(self, index):
		node = self.getNode(index)
		if node.is_dir and not node.is_traversed:
			return True
		return False
		# called if canFetchMore returns True, then dynamically inserts nodes required for
		# directory contents
	def fetchMore(self, index):
		parent = self.getNode(index)
		nodes = []
		for file in os.listdir(parent.path):
			file_path = os.path.join(parent.path, file)
			node = Node(file, file_path)
			if os.path.isdir(file_path):
				node.is_dir = True
				nodes.append(node)
				self.insertNodes(0, nodes, index)
				parent.is_traversed = True
		# returns True for directory nodes so that Qt knows to check if there is more to load
	def hasChildren(self, index):
		node = self.getNode(index)
		if node.is_dir:
			return True
		return super(FileSystemTreeModel, self).hasChildren(index)
		# should return 0 if there is data to fetch (handled implicitly by check length of child list)
	def rowCount(self, parent):
		node = self.getNode(parent)
		return node.child_count()
	def columnCount(self, parent):
		return 1
	def flags(self, index):
		return FileSystemTreeModel.FLAG_DEFAULT
	def parent(self, index):
		node = self.getNode(index)
		parent = node.parent
		if parent == self.root:
			return QModelIndex()
		return self.createIndex(parent.row(), 0, parent)
	def index(self, row, column, parent):
		node = self.getNode(parent)
		child = node.child(row)
		if not child:
			return QModelIndex()
		return self.createIndex(row, column, child)
	def headerData(self, section, orientation, role):
		return self.root.name
	def data(self, index, role):
		if not index.isValid():
			return None
		node = index.internalPointer()
		if role == Qt.DisplayRole:
			return node.name
		else:
			return None
	def insertNodes(self, position, nodes, parent=QModelIndex()):
		node = self.getNode(parent)
		self.beginInsertRows(parent, position, position + len(nodes) - 1)
		for child in nodes:
			success = node.insert_child(position, child)
			self.endInsertRows()
		return True
#	data = [("Alice", [("Keys", []),("Purse", [("Cellphone", [])])]),
#		("Bob", [("Wallet", [("Credit card", []),("Money", [])])])]
#	def createTreeModel(self):
#		model = QFileSystemModel()
#		model.setRootPath(QDir.homePath())
#==========================Source Materials=============================||
'''
http://blog.tjwakeham.com/lazy-loading-pyqt-data-models/
'''
#============================:::DNA:::==================================||
'''
<(DNA)>:

'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||