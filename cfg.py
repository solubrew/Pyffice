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



def calcERNsymbol(gvn):
	'Calculate the Extended Roman Numeral Symbol with Subtractive Notation'
	nsys = config.instruct(here+'cfg.yaml').load().dikt['column']
	keys = list(nsys.keys()).sort()
	for val in reversed(keys):
		if gvn > int(val):
			lval = val
			continue
		else:
			qs = int(gvn / int(val))
			gvn = (gvn % int(val)) * int(val)
		for i in range(qs):
			ern += nsys[val]























