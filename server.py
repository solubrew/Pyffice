#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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
from osbrain import run_agent
from osbrain import run_nameserver
#=======================================================================||
class appSRVR(object):
	def __init__(self):
		# System deployment
		self.ns = run_nameserver()
		self.agents = ['GUI', 'CalcEngine', 'FormatEngine',
						'UserEngine']
		self.initAgents()
	def initAgents(self):
		for agent in self.agents:
			self.birthAgent(agent)
	def initSRVRs(self):

	def stor(self):
		''
		self.birthAgent('librarian')
		agent = self.connectProxy('librarian')
		agent.db = workDB()
		#connect to fxsquril inmem db
		return self
	def gui(self):
		''
		return self
	def birthAgent(self, agent):
		run_agent(agent)
		return
	def connectProxy(self, agent):
		# Create a proxy to Agent1 and log a message
		agent = ns.proxy(agent)
		return agent
#		agent.log_info('Hello world!')
	def stop(self):
		ns.shutdown()
class ctrlSRVR(object):
	def __init__(self):
		# System deployment
		self.ns = run_nameserver()
		self.agents = ['appSRVRagent', 'dataSRVRagent', 'userSRVRagent']
		self.initAgents()
	def initAgents(self):
		for agent in self.agents:
			self.birthAgent(agent)
	def initSRVRs(self):
		'use agent to start its respective server'

	def stor(self):
		''
		self.birthAgent('librarian')
		agent = self.connectProxy('librarian')
		agent.db = workDB()
		#connect to fxsquril inmem db
		return self
	def gui(self):
		''
		return self
	def birthAgent(self, agent):
		run_agent(agent)
		return
	def connectProxy(self, agent):
		# Create a proxy to Agent1 and log a message
		agent = ns.proxy(agent)
		return agent
#		agent.log_info('Hello world!')
	def stop(self):
		ns.shutdown()
class dataSRVR(object):
	def __init__(self):# System deployment
		self.ns = run_nameserver()
		self.agents = ['inMemagent', 'appDBagent']
		self.initAgents()
	def initAgents(self):
		for agent in self.agents:
			self.birthAgent(agent)
	def stor(self):
		''
		self.birthAgent('librarian')
		agent = self.connectProxy('librarian')
		agent.db = workDB()#connect to fxsquril inmem db
		return self
	def gui(self):
		''
		return self
	def birthAgent(self, agent):
		run_agent(agent)
		return
	def connectProxy(self, agent):
		# Create a proxy to Agent1 and log a message
		agent = ns.proxy(agent)
		return agent
	def stop(self):
		ns.shutdown()
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
class commSRVR(object):
	def __init__(self):
		# System deployment
		self.ns = run_nameserver()
		self.agents = ['GUI', 'CalcEngine', 'FormatEngine',
						'UserEngine']
		self.initAgents()
	def initAgents(self):
		for agent in self.agents:
			self.birthAgent(agent)
	def stor(self):
		''
		self.birthAgent('librarian')
		agent = self.connectProxy('librarian')
		agent.db = workDB()
		#connect to fxsquril inmem db
		return self
	def gui(self):
		''
		return self
	def birthAgent(self, agent):
		run_agent(agent)
		return
	def connectProxy(self, agent):
		# Create a proxy to Agent1 and log a message
		agent = ns.proxy(agent)
		return agent
#		agent.log_info('Hello world!')
	def stop(self):
		ns.shutdown()
