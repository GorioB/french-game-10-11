DOOR_COMPLIMENTS={'north':'south','east':'west','west':'east','south':'north'}
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
		return self.name+"\n"+self.desc+"\nobjects:\n"+str(self.objects)

	def addDoor(self,doorName,target):
		if doorName not in self.doors.keys():
			self.doors.update({doorName:target})

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
			self.lines={}

	def addLine(self,lines):
		self.lines.update(lines)
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

class player:
	def __init__(self,name='',desc='',inventory=None,location=None):
		self.name=name
		self.desc=desc
		if inventory==None:
			self.inventory={}
		self.location=location

	def update(self,name='',desc='',inventory=None,Location=None):
		if name!='':
			self.name=name
		if desc!='':
			self.desc=desc
		if inventory!=None:
			self.inventory=inventory
		if location!=None:
			self.location=location

	def lookTo(self,door):
		if door in self.location.doors:
			return self.location.doors[door].lookAt()
		else:
			return -1

	def takeDoor(self,door):
		if door in self.location.doors:
			self.location=self.location.doors[door]
			return 0
		else:
			return -1

	def takeItem(self,item):
		if item in self.location.objects:
			self.inventory[item] = self.location.objects.pop(item)
			return 0
		else:
			return -1

	def giveItem(self,item,target):
		if item in self.inventory:
			target.inventory[item]=self.intentory.pop(item)
			return 0
		else:
			return -1

	def tell(self,query,target):
		if target in self.location.occupants.keys():
			person = self.location.occupants[target]
			if query in person.lines.keys():
				response = person.lines[query]
				if response[0]=='say':
					return response[1]
				else:
					if not (person.giveItem(response[1],self)):
						return ['RECV',response[1],'FRM',person.name]
					else:
						return ['NOLONGER',person.name]
			else:
				return "NOTHOLDING"

		else:
			return "NOTINROOM"

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