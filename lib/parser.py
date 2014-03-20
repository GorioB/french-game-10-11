def adder(a,b):
	return a+b

def parse(query):
	verbs = {'allez':'lookTo',
		'parlez':'tell',
		'prenez':'takeItem',
		'donnez':'giveItem',
		'regardez':'lookTo'}

	verbChoices=['allez','parlez','prenez','donnez','regardez']

	def isOfType(verb):
		return verb in query

	verbChoices = filter(isOfType,verbChoices)
	if len(verbChoices)!=1:
		return -1

	if verbChoices[0]=='parlez':
		query = query.split("parlez")[1].strip(" ")
		if "bonjour" in query.lower() or "salut" in query.lower():
			return [verbs[parlez],"bonjour"]
		elif "appelle" in query.lower():
			return [verbs[parlez],"who"]
		elif "comment" in query.lower():
			return [verbs['parlez'],"how"]
		else:
			return -1

	else:
		return verbs[verbChoices[0]],query.split(verbChoices[0])[1].strip(" ")

	return -1
	