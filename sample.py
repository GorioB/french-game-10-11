class node:
	def __init__(self,name='',neighbors={}):
		self.name=name
		self.neighbors=neighbors

	def addNeighbor(self,neighborTag,neighbor):
		if neighborTag not in self.neighbors.keys():
			self.neighbors[neighborTag] = neighbor
