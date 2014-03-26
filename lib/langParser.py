def adder(a,b):
	return a+b

def parse(query):
	ordinals = {'a gauche':'west','a droite':'east','tout droit':'north','derriere':'south'}
	verbs = {'allez':'takeDoor',
		'parlez':'tell',
		'prenez':'takeItem',
		'donnez':'giveItem',
		'regardez':'lookTo'}

	verbChoices=['allez','parlez','prenez','donnez','regardez']

	if 'parlez' in query.lower():
		query = query[query.lower().index('parlez')+len('parlez'):].strip(" ").strip("\"").strip("<<").strip(">>")
		#query = query.split("parlez")[1].strip(" ").strip("\"").strip("<<").strip(">>")
		if "bonjour" in query.lower() or "salut" in query.lower():
			return [verbs['parlez'],"bonjour"]
		elif "appelle" in query.lower():
			return [verbs['parlez'],"who"]
		elif 'appelez' in query.lower():
			return [verbs['parlez'],"who"]
		elif "comment" in query.lower():
			return [verbs['parlez'],"how"]
		else:
			return -1

	def isOfType(verb):
		return verb.lower() in query.lower()

	verbChoices = filter(isOfType,verbChoices)
	if len(verbChoices)!=1:
		return -1


	if query.lower().split(verbChoices[0])[1].strip(" ") in ordinals.keys():
		return verbs[verbChoices[0]],ordinals[query[query.lower().index(verbChoices[0])+len(verbChoices[0]):].strip(" ").lower()]
		#return verbs[verbChoices[0]],ordinals[query.split(verbChoices[0])[1].strip(" ")]
	else:
		return verbs[verbChoices[0]],query[query.lower().index(verbChoices[0])+len(verbChoices[0]):].strip(" ")
		#return verbs[verbChoices[0]],query.split(verbChoices[0])[1].strip(" ")

	return -1
