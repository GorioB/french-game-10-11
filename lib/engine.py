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
				a.addLine({i['key']:(i['method'],i.text)})

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

	#def populateItems(self):

	#def populateRooms(self):

	#def save(self,name):

	#def load(self,name):

if __name__=='__main__':
	engie = engine()
	charsfn = "..\\content\\characters.html"
	engie.populateItems("..\\content\\items.html")

	e = engie.populateActors(charsfn)

	print engie.allActors

	print engie.allActors['pman'].lines['bonjour'][1]


	print engie.allItems

	print engie.allActors['bman'].inventory