#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import hashlib
import requests
from character import Character, CharacterData

class Marvel(object):
	ROOT_DIRECTORY = os.path.dirname(__file__)
	RESOURCES = ('characters', 'comics', 'creators', 'events', 'series', 'stories')
	PUBLIC_KEY = 'your public key...'
	PRIVATE_KEY = 'your private key...'
	BASE_URL = 'http://gateway.marvel.com/v1/public/'
	API_VERSION = 'Cable'
	TIMESTAMP = time.time()

	string_to_hash = str(TIMESTAMP)+PRIVATE_KEY+PUBLIC_KEY
	hashed = hashlib.md5()
	hashed.update(string_to_hash)
	hashed = hashed.hexdigest()
	payload = {'apikey': PUBLIC_KEY,
			'ts': TIMESTAMP,
			'hash': hashed}

	@classmethod
	def start(cls, public_key, private_key):
		inst = cls()
		inst.PUBLIC_KEY = public_key
		inst.PRIVATE_KEY = private_key
		return inst
	
	def find_character(self, name = 'default'):
		""" return Character or CharacterList object 
		Keyword arguments:
		name -- Marvel character name. If empty, find all characters
		filter -- True if you want find name's start with
		"""
		image = []
		characterlist = []
		if name != 'default':
			self.payload['name'] = name
		r = requests.get(os.path.join(self.BASE_URL, self.RESOURCES[0]), params = self.payload)
		j = r.json()
		if j['code'] != 200:
			raise Exception("Server response's code is not 200")
		elif j['data']['total'] < 1:
			self.payload.pop('name')
			self.payload['nameStartsWith'] = name
			r = requests.get(os.path.join(self.BASE_URL, self.RESOURCES[0]), params = self.payload)
			j = r.json()
			if j['data']['total'] < 1:
				raise Exception("'"+name+"' is not in Marvel Database. Check it with another name")
		for caracter in j['data']['results']:
			id = caracter['id']
			name = caracter['name']
			description = caracter['description']
			modified = caracter['modified']
			resourceURI = caracter['resourceURI']
			urls = caracter['urls']
			image.append(caracter['thumbnail']['path'])
			image.append(caracter['thumbnail']['extension'])
			comics_list = caracter['comics']
			series_list = caracter['series']
			stories_list = caracter['stories']
			events_list = caracter['events']
			if j['data']['total'] == 1:
				return Character(id, name, description, modified, resourceURI, urls, image, comics_list, series_list, stories_list, events_list)
			else:
				characterlist.append(Character(id, name, description, modified, resourceURI, urls, image, comics_list, series_list, stories_list, events_list))
		return CharacterData(characterlist, j['data']['offset'], j['data']['limit'], j['data']['total'], j['data']['count'], os.path.join(self.BASE_URL, self.RESOURCES[0]), self.payload)
