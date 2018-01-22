import pickle
import os.path

def saveObj(obj,name):
	with open(name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, protocol=2)


def loadObj(name):
	with open(name + '.pkl', 'rb') as f:
		return pickle.load(f)



def addObservation(measurenames_full,measures_full,measurenames_qual,measures_qual,meta,name,dbname):
	# create dictionary

	# two different versions (quantitative and qualitative!)
	data_full = {}
	for i,m in enumerate(measures_full):
		data_full = data_full.update({measuresnames_full[i]: measures[i]})
	name_full = name + '_full'
	entry_full = {'Data': data_full, 'Meta':meta['Full']}
	
	data_qual = {}
	for i,m in enumerate(measures_qual):
		data_qual = data_qual.update({measuresnames_qual[i]: measures[i]})
	name_qual = name + '_qual'
	entry_qual = {'Data': data_qual, 'Meta':meta['Qual']}

	entry = {name:{'Full':entry_full, 'Full_qual':entry_qual}}
	database = entry
	# if database exists, load it and add pentry
	if os.path.exists(dbname+ '.pkl'):
		print 'updating database'
		database = loadObj(dbname)
		database.update(entry)
	# if it doesn't exist, just save the newly created dictionary
	saveObj(database,dbname)
