# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json


os.chdir( '..' )
with open('section_templates.json', encoding='UTF-8') as f:
	d = json.load( f, encoding='UTF-8' )

	store = []

	def scan( root, parent='' ):
		for k,v in root.items():
			if k.startswith( '{{syn' ):
				store.append( (parent, k) )
				print( (parent, k) )
			scan( v, parent+', '+k )

	scan( d )

	print( store )
