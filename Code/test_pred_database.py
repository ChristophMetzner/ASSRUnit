import pickle
import os.path

def loadObj(name):
	with open(name + '.pkl', 'rb') as f:
		return pickle.load(f)


db = loadObj('ASSR_schizophrenia_prediction_database')
print db
