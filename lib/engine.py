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

	def populateActors(self,charsfn):
		def createActor(soupobject):
			a = models.actor(ident=soupobject['ident'],
				name=soupobject['name'],
				desc=soupobject['desc']
				)

			lines = soupobject.find_all('line')

			for i in lines:
				a.addLine({i['key']:i.text})

			return a

		try:
			charsFile = open(charsfn,'r')
		except:
			print "File "+charsfn+" does not exist"
			return -1

		charSoup = BeautifulSoup(charsFile)
		entries=map(createActor,charSoup.find_all('actor'))
		keys = map(enginescripts.extractKey,entries)
		self.allActors=dict(zip(keys,entries))


		charsFile.close()
		return self.allActors





	#def populateItems(self):

	#def populateRooms(self):

	#def save(self,name):

	#def load(self,name):

if __name__=='__main__':
	engie = engine()
	charsfn = "..\\content\\characters.html"

	e = engie.populateActors(charsfn)

	print engie.allActors

	print engie.allActors['pman'].lines['bonjour']