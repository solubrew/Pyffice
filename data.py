#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
''' #																	||
--- #																	||
<(META)>: #																||
	DOCid: <^[uuid]^> #													||
	name:  ngynFxSQuRIL#
	description: > #													||
		Routing Data Manipulations between inmem databases,
		stored databases, remote databases, etc
		Fractionally Executed SQL Queued Recursive Interaction Layer

#only one shared cache inmem db
#others must be private
#spin a process for each in memdb for each fileinmemdb needed
#use the single shared cache for the main app db have the name server
#communicate directly here

#osbrain named server?

#inmemdb
#bigtable

#cmd = "CREATE TABLE bgtbl col0-col49"#use machine learning here

#appdb...one per device running application

#multiple interaction pathways

#filedbs...unknown number

#max attach is like 25dbs

#how to determine when a fileDB should get its own bigtable

#increased security

#how to implement permissions effectively??

#reduced overhead for lots of small workbooks using a combined bigtable

process:
	load document
	get all sectn ids from file db and load into inmem big table
	map document table columns to bigtable columns
	read document
	check bigtable documents
	if no runs are connected to the current document...how to tell

	check m_run table
	check _run table

	once completed

	if not there:
		load document limit 0 to displaysize-y*(1+i%)
	if is there get first and lest seq
		compare against displaysize-y
			if not then grab additional
				check if first is 0 then get from bottom
				if not split gap and get from top first
				then from bottom
		also verify that full seq is available
			if not get
		next verify that all sectns are the most recent
	if there is not then

	expirary: <[expiration]> #											||
	version: <[version]> #												||
	path: <[LEXIvrs]>pheonix/elements/store/orgnql/sonql.py #			||
	outline: <[outline]> #												||
	authority: document|this #											||
	security: sec|lvl2 #												||
	<(WT)>: -32 #														||
''' #																	||
# -*- coding: utf-8 -*-
#=======================================================================||
import queue
#=======================================================================||
from osbrain import run_nameserver
from osbrain import run_agent
#=======================================================================||
class dataRTR(object):
	'Distribute Data between the inMemory DB and persistent Stores'
	def __init__(self, nameserver, cfg=None):
		'Data Router'
		self.config = config.instruct(pxcfg).override(cfg)
		self.nameserver = nameserver
		self.queue = queue.Queue()
		self.go = True
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

class fracExSQL(object):
	'Fractionally Executed Structure Query Language'
	version = '0.0.0.0.0.0'
	def __init(self, cmd, tblMap):
		''
		self.cmd = cmd
		self.tblMap = tblMap
	def refreshTableMap(self):
		''
		return self
	def cmdFractionalizer(self):
		'split cmd so that different sections can be pulled from different tables'
		'this is mainly intended to allow the use of the inmem database for active data'
		'and to take the same actions on stored data as well as moving the data between'
		'these states'
	def write(self):
		''
		return self
	def read(self):
		''
		return self
	def _write2inMemShare(self):
		''
		return True
	def _write2AppDB(self):
		''
		return True
	def _write2FileDB(self):
		''
		return True
	def _readinMemShare(self):
		''
		return self
	def _readAppDB(self):
		''
		return self
	def _readFileDB(self):
		''
		return self
class chunk(object):
	def __init__(self, chunk):
		self.chunk = chunk
		self.sectnUUID = chunk['sectnUUID']
		self.sectnSize = chunk['sectnSize']
		self.text = chunk['Text']
		self.dtid = chunk['DTID']
		self.tipe = chunk['Type']
		self.state = chunk['State']

class encoder(object):
	def __init__(self, text, size):
		''
		self.text = text
		self.size = size
	def decodeSeq(self):
		cols, rows= size.split([',','.','|'])

		nrow = [sectnUUID, seq]

		for col in cols:
			for row in rows:
				for line in text.split('\n'):
					tbl.append(line)




		return self
	def encodeSeq(self, cnt, seq):
		''

		return self
	def decodeText(self):
		''
		return self
	def encodeText(self, uuid=None):
		''
		if uuid == None:
			sectnUUID = thing.what().uuid

		return self

		return self
class memDB(db):
	def __init__(self, cfg=None):
		pxcfg = here+'/z-data_/FxSQuRIL.yaml'
		self.config = config.instruct(pxcfg).select('inmemdb').override(cfg)
		self.name = self.config.dikt['Name']
		self.path = 'file:'+self.name+':memory:?cache=shared'
	def _conx(self):
		''
		self.conn = sql3.connect(self.name, uri=True)
	def initBigTable(self, contentcols=None):
		''
		#need to check if bigtable exists and if so increment
		#create unioning view from incremented table
		#union current bigtable for immediate needs
		#replace original bigtable with new one
		idcols = self.config['tables']['bigtable']['size']['columns']['ids']
		ncols = self.config['tables']['bigtable']['size']['columns']['content']['min']
		cntcols = []
		for col in range(ncols):
			cntcols.append('col'+str(col))
		admincols = ['tables']['bigtable']['size']['columns']['admins']
		cols = idcols+cntcols+admincols
	def initFxTable(self):
		'load functions from any active languages'
		'Python, Excel, LEXI,....add as you go'
		return self
	def initMsgTable(self):
		''

		return self
	def initOpenDocsTable(self):
		'Used to translate state between inmembigtable and appdb/filedb'

		return self
	def initIsolatedTable(self):
		'An Isolated Table is used for a intensive datasets needing their own structure'
		return self
	def initRunTable(self):
		''
		return self
	def cacheTable(self):
		'write everything in memory db to a on disk cache table'
		'set startup flag to parse anything left on next start'
		'then parsing cache table and storing updates correctly'
		'this is intended to save data quickly to reduce data loss from unexpected closing'
		return self
class appDB(db):
	def __init__(self):
		''
	def manageDocDBs(self):
		''
		return self
	def initPerfTable(self):
		''
		return self
class fileDB(db):
	def __init__(self):
		''

class db(object):
	'Control I/O for relational database formats'#						||=>Describe class
	version = '0.0.0.0.0.0'#											||=>Set version
	def __init__(self, doc, kind=None, params=None, cfg=None):#			||=>
		self.doc = doc#													||set doc var
		pxcfg = here+'z-data_/ngynFxSQuRIL.yaml'#							||assign default config
		self.config = config.instruct(pxcfg).override(cfg)#				||load config
		self._findDBType()#												||
		db = {'server': '', 'database': self.doc}#						||
		self._conx(db)#													||
	def _conx(self, db=None):#											||
		'Connect to Database'#											||
		try:#														||
			dpath = calct.stuff(db).path()
			if not dpath.valid:
				os.makedirs(dpath.it)
			self.conn = sql3.connect(dbase)#						||assign db connection
		except Exception as e:#										||
			m = ['Database connection to',db,'failed due to',e]#	||
			log.WORKLOG(e,m,db)#									||
			comm.see(m)#											||
		return self#														||
	def read(self, fill=None, cfg={}, cmd={}):#						||
		'Return iterator object to pull data in chunks via offset'
		if 'adders' not in cfg.keys():
			cfg['adders'] = []
		if 'page' not in cfg.keys():
			cfg['page'] = 100
		if 'fill' not in cfg.keys():
			cfg['fill'] = {}
		if cmd in list(self.config[self.dbtype]['cmds'].keys()):
			cmd = self.config[self.dbtype]['cmds'][cmd]
		cfg['cmds'] = cmd
		cfg['fill']['<[limit]>'] = cfg['page']
		cfg['fill']['<[offset]>'] = 0
		if fill != None:
			for k in fill.keys():
				cfg['fill'][k] = fill[k]
		cfg['adders'].append(self.config['SQLT']['adders']['limitoffset'])
		self.build = {}
		if 'tables' in cfg.keys():
			for table in cfg['tables']:
				if table not in self.build.keys():
					self.build[table] = {}
		self.builder('SELECT', cfg['cmds'], cfg)
		while self.build != {}:
			self.execute('read', cfg)
			cfg['fill']['<[offset]>'] += cfg['page']
			print(cfg['fill']['<[offset]>'])
			self.dikt = self.build
			self.go = True
			yield self
		self.go = False
		yield self
	def write(self, data, ext='.sqlite', cfg=None):#							||
		self.build = data#											||{table: records}
		self.builder('CRE')#									||
		self.execute('cre')#										||
		self.builder('INS')#									||
		self.execute('write')#										||
	def fraqBuilder(self, how='SELECT', gcmd={}, cfg=None):#				||
		'Build Fractional Query to be executed across databases'#		||
		self.cmdr = {}#													||set sql cmd container
		self._admin()#													||get admin columns
		if gcmd == {}:#													||check for given cmd
			if self.build == {}:#										||
				self.getInfo()#											||get database info
			if self.build.keys() == {}:#								||
				self.getTables(self.build.keys())#						||
			for table in self.build.keys():#							||
				if 'columns' not in self.build[table]:#					||
					self.getTableColumns(table)#						||
				cols = self.build[table]['columns']
				cols = self.validateColumns(cols)#						||
				self.cmdr[table] = {'columns': cols}#					||
				if how == 'SELECT':#									||
					cmd = self.bldSELECT(cols, table, cfg)#					||
				elif how == 'CRE':#										||
					cmd = self.bldCRE(cols, table, cfg)#						||
				elif how == 'INS':#										||
					cmd = self.bldINS(cols, table, cfg)#						||
				elif how == 'DROP':#									||
					cmd = self.bldDROP(cols, table, cfg)
				elif how == 'REV':#										||
					cmd = self.bldREV(cols, table, cfg)
				else:
					e = 'STORE.ORGNQL.SONQL.doc.builder'
					m = 'No Command Built'
					d = {'table': table,'columns': cols,'config': cfg}#	||
					log.WORKLOG(e,m,d,c)
				self.cmdr[table]['cmd'] = cmd
		else:#															||
			sec = '--LOG.ALERT.SQLINJECTION'
			self.bldGIVEN(gcmd.replace(';',sec), cfg)#					||
		return self

class router(object):
	def __init__(self):

	def loadStores(self):
		''
		#connect to application config store
		#connect to user config store
		#this should hold all the active files being used by that user
		#accept
		return self
	def writeInMemDB(self):
		''
		return self
	def writeAppDB(self):
		''
		return self
	def writeFileDB(self):
		''
		return self
	def readInMemDB(self):
		''
		return self
	def readAppDB(self):
		''
		return self
	def readFileDB(self):
		''
		return self
