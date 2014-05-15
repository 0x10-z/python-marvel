#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests

class CharacterData:
	itemlist = []
	offset = ''
	limit = ''
	total = ''
	count = ''
	url = ""
	payload = {}
	first = True

	def __init__(self, itemlist, offset, limit, total, count, url, payload):
		self.itemlist = itemlist
		self.offset = offset
		self.limit = limit
		self.total = total
		self.count = count
		self.url = url
		self.payload = payload

	def hasNext(self,):
		"""
		if has next, return true with items updated
		else, return false
		"""
		if self.first:
			self.first = False
			return True
		elif self.offset+self.limit < self.total:
			image = []
			self.itemlist[:] = []
			self.payload['offset'] = self.offset + self.limit
			r = requests.get(self.url, params = self.payload)
			j = r.json()
			for caracter in j['data']['results']:
				id = caracter['id']
				name = caracter['name'].encode('utf-8')
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
				self.itemlist.append(Character(id, name, description, modified, resourceURI, urls, image, comics_list, series_list, stories_list, events_list))
			self.offset = j['data']['offset']
			self.limit = j['data']['limit']
			self.total = j['data']['total']
			self.count = j['data']['count']
			return True
		else:
			return False

class Character:
	id = ""
	name = ""
	description = ""
	modified = ""
	resourceURI = ""
	urls = ""
	image = []
	comics_list = []
	series_list = []
	stories_list = []
	events_list = []

	def __init__(self, id, name, description, modified, resourceURI, urls, image, comics_list, series_list, stories_list, events_list):
		self.id = id
		self.name = name
		self.description = description
		self.modified = modified
		self.resourceURI = resourceURI
		self.urls = urls
		self.image = image
		self.comics_list = comics_list
		self.series_list = series_list
		self.stories_list = stories_list
		self.events_list = events_list

	""" default save a portrait_uncanny image of character """
	def save_image(self, image_type = 'portrait', image_size = 'uncanny'):
		image_variant = {'portrait': {'small':'portrait_small',
									'medium': 'portrait_medium',
									'xlarge': 'portrait_xlarge',
									'fantastic': 'portrait_fantastic',
									'uncanny': 'portrait_uncanny',
									'incredible': 'portrait_incredible'},
						'standard': {'small',
									'medium',
									'large',
									'xlarge',
									'fantastic',
									'amazing'},
						'landscape': {'small',
									'medium',
									'large',
									'xlarge',
									'amazing',
									'incredible'},
						}
		content = requests.get(os.path.join(self.image[0],image_variant[image_type][image_size])+'.'+self.image[1]).content
		a = open(os.path.join(self.ROOT_DIRECTORY, self.name+"."+self.image[1]), 'wb')
		a.writelines(content)
		a.close()

	""" return a ComicList object with 'resourceURI' and 'name' of each comic """
	def get_comics(self,):
		return ComicList(self.comics_list['items'], self.comics_list['collectionURI'], self.comics_list['returned'], self.comics_list['available'])
		
	""" return a StoryList object with 'resourceURI' and 'name' attribute """
	def get_stories(self,):
		return StoryList(self.stories_list['items'], self.stories_list['collectionURI'], self.stories_list['returned'], self.stories_list['available'])

	""" return a EventList object with 'resourceURI' and 'name' attribute """
	def get_events(self,):
		return EventList(self.events_list['items'], self.events_list['collectionURI'], self.events_list['returned'], self.events_list['available'])

	""" return a SeriesList object with 'resourceURI' and 'name' attribute """
	def get_series(self,):
		return SeriesList(self.series_list['items'], self.series_list['collectionURI'], self.series_list['returned'], self.series_list['available'])

class List:
	available = ""
	returned = ""
	collectionURI = ""
	items = []

	def __init__(self,items, collectionURI, returned, available):
		self.available = available
		self.returned = returned
		self.collectionURI = collectionURI
		self.items = items


class ComicList(List):
	pass

class StoryList(List):
	pass

class EventList(List):
	pass

class SeriesList(List):
	pass

class Summary:
	resourceURI = ""
	name = ""

	def __init__(self, resourceURI, name):
		self.resourceURI = resourceURI
		self.name = name

class ComicSummary(Summary):
	pass

class SeriesSummary(Summary):
	pass

class StorySummary(Summary):
	type_summary = ""

	def __init__(self, type_summary, resourceURI, name):
		self.type_summary = type_summary
		super.resourceURI = resourceURI
		super.name = name
