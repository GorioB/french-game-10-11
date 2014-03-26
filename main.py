# -*- coding: utf-8 -*-

import lib.engine
import lib.models
import lib.langParser
import os
HELP ="Type i for inventory and quit to leave"
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
	print "Enter h for help\n\n\n"
	print player.location.lookAt()
	while 'hug' not in player.inventory:
		inp = raw_input(">")
		parsed = lib.langParser.parse(inp)
		if parsed!=-1:
			action = player.actions[parsed[0]](parsed[1])
			if action==-30:
				print "Vous ne pouvez pas aller."
			elif action==-40:
				print "Donnez quoi?"
			elif action==-20:
				print "Il n'y a pas \""+parsed[1]+"\""
			elif action!=0:
				print action
		elif inp.lower()=='i':
			print player.showInventory()
		elif inp.lower()=='h':
			print HELP
		elif inp.lower()=='quit':
			return -1
		else:
			print "Je ne comprends pas"
	print "Fin."
	return 0

if __name__=="__main__":
	e = initEngineFromFolder("content\\")
	p = initPlayerFromEngine(e)
	mainloop(p)
	raw_input("Press ENTER to close")