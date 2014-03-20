# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import models
import os
import enginescripts
class engine:
	def __init__(self):
		self.protagonist = models.player()
		self.allActors={}
		self.allRooms={}
		self.allItems={}

	def populateItems(self,itemsfn):
		def createItem(soupobject):
			return models.item(ident=soupobject['ident'],
				name=soupobject['name'],
				desc=soupobject['desc']
				)

		try:
			itemsFile = open(itemsfn,'r')
		except:
			print "File "+itemsfn+" does not exist"
			return -1

		itemSoup = BeautifulSoup(itemsFile)
		entries = map(createItem,itemSoup.find_all('item'))
		self.allItems = enginescripts.createDict(entries)

		itemsFile.close()
		return self.allItems

	def populateActors(self,charsfn):
		def createActor(soupobject):
			a = models.actor(ident=soupobject['ident'],
				name=soupobject['name'],
				desc=soupobject['desc']
				)

			lines = soupobject.find_all('line')

			for i in lines:
				a.addLine(i['key'],i['need'],i.text,i['gift'])

			items = soupobject.find_all('item')

			for i in items:
				if i['ident'] in self.allItems.keys():
					a.addItem({i['ident']:self.allItems[i['ident']]})
				else:
					print "Your allItems is incomplete. Ensure that it is defined in your itemsfile and that you ran populateItems first"
			return a

		try:
			charsFile = open(charsfn,'r')
		except:
			print "File "+charsfn+" does not exist"
			return -1

		charSoup = BeautifulSoup(charsFile)
		entries=map(createActor,charSoup.find_all('actor'))

		self.allActors = enginescripts.createDict(entries)


		charsFile.close()
		return self.allActors

	def populateRooms(self,roomsfn):
		def dig(soupObject):
			a = self.allRooms[soupObject['ident']]

			for i in soupObject.find_all('exit'):
				a.addDoor(i['door'],self.allRooms[i['target']])

			return 0

		def createRoom(soupobject):
			a = models.room(ident=soupobject['ident'],name=soupobject['name'],desc=soupobject['desc'])

			actors = soupobject.find_all('actor')
			for i in actors:
				if i['ident'] in self.allActors.keys():
					a.addActor({i['ident']:self.allActors[i['ident']]})
				else:
					print "Your allActors is incomplete. Make sure that it is defined in your actors file and that you ran populateActors first"

			items = soupobject.find_all('item')
			for i in items:
				if i['ident'] in self.allItems.keys():
					a.addItem({i['ident']:self.allItems[i['ident']]})
				else:
					print "Your allItems is incomplete."

			return a


		try:
			roomsFile = open(roomsfn,'r')
		except:
			print "File "+roomsfn+" does not exist"
			return -1

		roomSoup = BeautifulSoup(roomsFile)
		entries = map(createRoom,roomSoup.find_all('room'))
		self.allRooms = enginescripts.createDict(entries)

		map(dig,roomSoup.find_all('room'))
		roomsFile.close()
		return self.allRooms

	#def save(self,name):

	#def load(self,name):
def tester():
	engie = engine()
	rootfn = "..\\content\\"
	engie.populateItems(rootfn+"items.html")
	engie.populateActors(rootfn+"characters.html")
	engie.populateRooms(rootfn+"rooms.html")
	player = models.player(location=engie.allRooms['0'])
	return player

if __name__=='__main__':
	engie = tester()