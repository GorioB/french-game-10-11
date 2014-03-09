def extractKey(item):
	return item.ident

def createDict(entries):
	keys = map(extractKey,entries)
	return dict(zip(keys,entries))