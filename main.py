# -*- coding: utf-8 -*-

import lib.engine
import lib.models
import lib.langParser
import os
HELP ="Type I for inventory and quit to leave"
def initEngineFromFolder(folder):
	engie=lib.engine.engine()
	engie.populateItems(folder+"items.html")
	engie.populateActors(folder+"characters.html")
	engie.populateRooms(folder+"rooms.html")
	return engie

def initPlayerFromEngine(engine):
	return lib.models.player(location=engine.allRooms['0'])

def mainloop(player):
	os.system('cls')
	print "Je Ne Comprends Pas: Une Petite Aventure"
	print u"Pour Français Dix et Onze"
	print "Enter H for help\n\n\n"
	print player.location.lookAt()
	while 'hug' not in player.inventory:
		inp = raw_input("> ")
		parsed = lib.langParser.parse(inp)
		if parsed!=-1:
			print player.actions[parsed[0]](parsed[1])
		elif inp.lower()=='i':
			print player.showInventory()
		elif inp.lower()=='h':
			print HELP
		elif inp.lower()=='quit':
			return -1
		else:
			print "Je ne comprends pas"
	return 0

if __name__=="__main__":
	e = initEngineFromFolder("content\\")
	p = initPlayerFromEngine(e)
	mainloop(p)