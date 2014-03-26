# -*- coding: utf-8 -*-
DOOR_COMPLIMENTS={'north':'south','east':'west','west':'east','south':'north'}
DIRECTION_TRANS_TABLE= {'north':[u'tout droit'],'south':[u'derrière'],'east':[u'à droite'],'west':[u'à gauche']}


class room:
	def __init__(self,ident='',name='',desc='',doors=None,occupants=None,objects=None):
		self.ident=ident
		self.name=name
		self.desc=desc
		if doors==None:
			self.doors={}
		else:
			self.doors=doors
		if occupants==None:
			self.occupants={}
		else:
			self.occupants=occupants
		if objects==None:
			self.objects={}
		else:
			self.objects=objects

	def __str__(self):
		return "ROOM "+ident

	def lookAt(self):
		retVal = self.name+"\n\n"+self.desc
		if len(self.objects.keys()):
			retVal = retVal+"\nIl y a"
			for i in self.objects.keys():
				retVal = retVal+" "+self.objects[i].name+","
			if retVal[-1]==',':
				retVal = retVal[:-1]

		if len(self.occupants.keys()):
			retVal=retVal+"\n"
			for i in self.occupants.keys():
				retVal = retVal+self.occupants[i].name+", "
			retVal = retVal[:-2]
			if len(self.occupants.keys())==1:
				retVal = retVal+" est ici."
			else:
				retVal = retVal+" sont ici."

		if len(self.doors.keys()):
			retVal = retVal+"\nLes portes: "
			for i in self.doors.keys():
				if i in DIRECTION_TRANS_TABLE.keys():
					retVal = retVal+DIRECTION_TRANS_TABLE[i][0]+", "

			retVal = retVal[:-2]+"."
		return retVal

	def addDoor(self,doorName,target):
		if doorName not in self.doors.keys():
			self.doors.update({doorName:target})

	def addActor(self,actor):
		self.occupants.update(actor)

	def addItem(self,item):
		self.objects.update(item)

class item:
	def __init__(self,ident='',name='',desc='',consumable=False,uses=None):
		self.name=name
		self.desc=desc
		self.uses=uses
		self.ident = ident
		if consumable=='True':
			self.isConsumable=True
		else:
			self.isConsumable=False

		if self.uses==None:
			self.uses={}


class actorLine:
	def __init__(self,key='',need='',response='',gift=''):
		self.key=key
		self.need=need
		self.gift=gift
		self.response=response

class actor:
	def __init__(self,ident='',name='',desc='',inventory=None,lines=None):
		self.name=name
		self.desc=desc
		self.inventory=inventory
		self.lines=lines
		self.ident = ident
		if self.inventory==None:
			self.inventory={}

		if self.lines==None:
			self.lines=[]

	def addLine(self,key,need,response,gift):
		self.lines.append(actorLine(key,need,response,gift))
		return 0

	def addItem(self,item):
		self.inventory.update(item)
		return 0

	def giveItem(self,item,target):
		if item in self.inventory.keys():
			target.inventory[item]=self.inventory.pop(item)
			return 0
		else:
			return 1

	def tell(self,query):
		possibleResponses=[i for i in self.lines if i.key==query]
		trueResponses=[i for i in possibleResponses if i.need in self.inventory]
		if trueResponses==[]:
			return [i for i in possibleResponses if i.need==''][-1]
		return trueResponses[-1]


class player:
	def __init__(self,inventory=None,location=None):
		if inventory==None:
			self.inventory={}
		self.location=location
		self.actions={'lookTo':self.lookTo,'takeDoor':self.takeDoor,'takeItem':self.takeItem,'giveItem':self.giveItem,'tell':self.tell};
	
	def getKeyFromName(self,name,source):
		#print name,source,[i.name for i in source.values()]
		if name.lower() in [i.name.lower() for i in source.values()]:
			return source.keys()[[i.name.lower() for i in source.values()].index(name.lower())]
		else:
			return -1

	def lookTo(self,target):
		isObject = self.getKeyFromName(target,self.inventory)
		if isObject!=-1:
			return self.inventory[isObject].desc
		isObject = self.getKeyFromName(target,self.location.occupants)
		if isObject!=-1:
			return self.location.occupants[isObject].desc
		isObject = self.getKeyFromName(target,self.location.objects)
		if isObject!=-1:
			return self.location.objects[isObject].desc
		if target in self.location.doors.keys():
			return self.location.doors[target].lookAt()
		elif target.lower() in self.location.occupants.keys():
			return self.location.occupants[target.lower()].desc
		return self.location.lookAt()

	def showInventory(self):
		if len(self.inventory)==0:
			return "Vous n'avez rien"
		rstr = "Vouz avez: "
		for i in self.inventory.values():
			rstr = rstr+i.name+", "
		rstr = rstr[:-2]+"."
		return rstr

	def takeDoor(self,door):
		if door in self.location.doors:
			self.location=self.location.doors[door]
			return self.location.lookAt()
		else:
			return -30

	def takeItem(self,item):
		itemname=item
		item = self.getKeyFromName(item,self.location.objects)
		if item==-1:
			return -20
		self.inventory[item] = self.location.objects.pop(item)
		return "Vous avez "+itemname


	def giveItem(self,item):
		item = self.getKeyFromName(item,self.inventory)
		if item==-1:
			return -40
		self.location.occupants.values()[0].inventory[item]=self.inventory.pop(item)
		return self.tell('here')

	def tell(self,query):
		if self.location.occupants.keys():
			person = self.location.occupants.values()[0]
			if query in [i.key for i in person.lines]:
				response = person.tell(query)
				if response:
					if response.gift in person.inventory.keys():
						person.giveItem(response.gift,self)
					
					rstring = person.name+u" répond, "+"<<"+response.response+">>"
					if response.gift!='':
						rstring = rstring+" et vous donnez "+self.inventory[response.gift].name
					return rstring
				else:
					return "NORESPONSE"
			else:
				return "INVALIDQUERY"
		else:
			return "NOBODYTHERE"


	def use(self,thing,on):
		if thing not in self.inventory.keys() or on not in self.inventory.keys():
			return -2

		if thing not in self.inventory[on].uses.keys():
			return -1

		self.inventory[on]=self.inventory[on].uses[thing]
		if self.inventory[thing].isConsumable:
			return self.inventory.pop(thing)

		return 0



if __name__=='__main__':
	p = player(name='gorio')
	a = room(name='room1',desc='the initial room')
	a.addDoor('north',room(name='room2',desc='the second room'))
	a.doors['north'].addDoor('south',a)
	x = ''
	p.location=a
	print p.location.lookAt()
	print p.lookTo('north')
	p.takeDoor('north')
	print p.lookTo('south')
	p.takeDoor('south')
	p.location.lookAt()