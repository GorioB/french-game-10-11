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
		return self.name+"\n"+self.desc

	def addDoor(self,doorName,target,targetDoor=''):
		if doorName not in self.doors.keys():
			self.doors.update({doorName:target})
			if targetDoor=='':
				if DOOR_COMPLIMENTS[doorName] not in self.doors[doorName].doors:
					self.doors[doorName].doors[DOOR_COMPLIMENTS[doorName]] = self

class player:
	def __init__(self,name='',desc='',inventory=None,location=None):
		self.name=name
		self.desc=desc
		if inventory==None:
			self.inventory=[]
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



if __name__=='__main__':
	p = player(name='gorio')
	a = room(name='room1',desc='the initial room')
	a.addDoor('north',room(name='room2',desc='the second room'))
	x = ''
	p.location=a
	print p.lookTo('north')
	p.takeDoor('north')
	print p.lookTo('south')