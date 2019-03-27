import numpy as np
import matplotlib.pylab as plt
import pickle
import pprint

def boxplot(data,labels):
	'''Simple box plot function.

 	Parameters
	-----------------
	data   : ndarray
		nD array containing the data.
	labels : list 
		A list containing the axis labels.
	'''
	plt.boxplot(data,labels=labels,showmeans=True)
	#plt.show()

def experimental_overview(studies=[],observations=[],  entrytype='Full',meta=False  ,dbname='Databases/ASSR_schizophrenia_experimental_database',plotting=True):
	'''Gives an overview of the experimental observations in the database.
	   Should make possible to query for specific studies, observation types
	   and meta-data.

 	Parameters
	-----------------
	
	Returns
	-----------------
	
	'''
	# load database
	
	database = _load_obj(dbname)
  
	rowLabels = []
    
	if entrytype == 'Full':
		if not studies: # full overview!
			if not observations: # full overview!
				# go through all studies and all observations
				keys      = database.keys()
				colLabels = keys
				for k in keys:
					obs = database[k][entrytype].keys()
					des = []
					for ob in obs:
						if not ob=='Meta':
							des.append(database[k][entrytype][ob]['description'])
					observations = list(set(observations+obs))
					rowLabels = list(set(rowLabels + des)) # this creates a list of unique(!) observations	
				observations.remove('Meta')
				nrows = len(rowLabels)
				ncols = len(colLabels)
				values =  [['not tested' for _ in range(ncols)] for _ in range(nrows)] 
				for i,k in enumerate(colLabels):
					for j,o in enumerate(observations):
						if o in database[k][entrytype].keys(): 
							string = ""
							key1 = 'groups'
							groups = database[k][entrytype][o][key1]
							key2 = 'values'
							vals = database[k][entrytype][o][key2]	
							for t in range(len(groups)):
								string = string + str(groups[t]) + ' : ' + str(vals[t]) + ' '
							values[j][i] = string
					if meta:
						if meta==True:
							print k
							pp = pprint.PrettyPrinter(indent=4)
							pp.pprint(database[k][entrytype]['Meta'])  
						else:
							print k
							pp = pprint.PrettyPrinter(indent=4)
							pp.pprint(database[k][entrytype]['Meta'][meta])
				if plotting:		
					_plot_table(values,rowLabels,colLabels)


			else:                # only display specific observations
				# go through all studies 
				keys      = database.keys()
				colLabels = keys
				for o in observations:
					for k in keys:
						des = []
						des.append(database[k][entrytype][o]['description'])
					rowLabels = list(set(rowLabels+des))
				nrows = len(rowLabels)
				ncols = len(colLabels)
				values =  [['not tested' for _ in range(ncols)] for _ in range(nrows)] 
				for i,k in enumerate(colLabels):
					for j,o in enumerate(observations):
						if o in database[k][entrytype].keys(): 
							string = ""
							key1 = 'groups'
							groups = database[k][entrytype][o][key1]
							key2 = 'values'
							vals = database[k][entrytype][o][key2]
							for t in range(len(groups)):
								string = string + str(groups[t]) + ' : ' + str(vals[t]) + ' '
							values[j][i] = string
					if meta:
						print k
						pp = pprint.PrettyPrinter(indent=4)
						pp.pprint(database[k][entrytype]['Meta'])
				if plotting:		
					_plot_table(values,rowLabels,colLabels)

		else:           # only display specific studies
			if not observations: # full overview!
				colLabels = studies
				for k in colLabels:
					obs      = database[k][entrytype].keys()
					des = []
					for ob in obs:
						if not ob=='Meta':
							des.append(database[k][entrytype][ob]['description'])
					observations = list(set(observations+obs))
					rowLabels = list(set(rowLabels + des)) # this creates a list of unique(!) observations
				observations.remove('Meta')	
				nrows = len(rowLabels)
				ncols = len(colLabels)
				values =  [['not tested' for _ in range(ncols)] for _ in range(nrows)] 
				for i,k in enumerate(colLabels):
					for j,o in enumerate(observations):
						if o in database[k][entrytype].keys(): 
							string = ""
							key1 = 'groups'
							groups = database[k][entrytype][o][key1]
							key2 = 'values'
							vals = database[k][entrytype][o][key2]	
							for t in range(len(groups)):
								string = string + str(groups[t]) + ' : ' + str(vals[t]) + ' '
							values[j][i] = string
					if meta:
						print k
						pp = pprint.PrettyPrinter(indent=4)
						pp.pprint(database[k][entrytype]['Meta'])
				if plotting:		
					_plot_table(values,rowLabels,colLabels)
			else:                # only display specific observations
				# go through all studies 
				colLabels = studies
				for o in observations:
					for k in studies:
						des = []
						des.append(database[k][entrytype][o]['description'])
					rowLabels = list(set(rowLabels+des))
				nrows = len(rowLabels)
				ncols = len(colLabels)
				values =  [['not tested' for _ in range(ncols)] for _ in range(nrows)] 
				for i,k in enumerate(colLabels):
					for j,o in enumerate(observations):
						if o in database[k][entrytype].keys(): 
							string = ""
							key1 = 'groups'
							groups = database[k][entrytype][o][key1]
							key2 = 'values'
							vals = database[k][entrytype][o][key2]	
							for t in range(len(groups)):
								string = string + str(groups[t]) + ' : ' + str(vals[t]) + ' '
							values[j][i] = string
					if meta:
						print k
						pp = pprint.PrettyPrinter(indent=4)
						pp.pprint(database[k][entrytype]['Meta'])
				if plotting:		
					_plot_table(values,rowLabels,colLabels)

	else :
		if not studies: # full overview!
			if not observations: # full overview!
				# go through all studies and all observations
				keys      = database.keys()
				colLabels = keys
				for k in keys:
					obs = database[k][entrytype].keys()
					des = []
					for ob in obs:
						if not ob=='Meta':
							des.append(database[k][entrytype][ob]['description'])
					observations = list(set(observations+obs))
					rowLabels = list(set(rowLabels + des)) # this creates a list of unique(!) observations	
				observations.remove('Meta')
				nrows = len(rowLabels)
				ncols = len(colLabels)
				values =  [['not tested' for _ in range(ncols)] for _ in range(nrows)] 
				for i,k in enumerate(colLabels):
					for j,o in enumerate(observations):
						if o in database[k][entrytype].keys(): 
							key = 'value'
							values[j][i] = database[k][entrytype][o][key]	
					if meta:
						if meta==True:
							print k
							pp = pprint.PrettyPrinter(indent=4)
							pp.pprint(database[k][entrytype]['Meta'])
						else:
							print k
							pp = pprint.PrettyPrinter(indent=4)
							pp.pprint(database[k][entrytype]['Meta'][meta])
				if plotting:		
					_plot_table(values,rowLabels,colLabels)

			else:                # only display specific observations
				# go through all studies 
				keys      = database.keys()
				colLabels = keys
				for o in observations:
					for k in keys:
						des = []
						des.append(database[k][entrytype][o]['description'])
					rowLabels = list(set(rowLabels+des))
				nrows = len(rowLabels)
				ncols = len(colLabels)
				values =  [['not tested' for _ in range(ncols)] for _ in range(nrows)] 
				for i,k in enumerate(colLabels):
					for j,o in enumerate(observations):
						if o in database[k][entrytype].keys(): 
							key = 'value'
							values[j][i] = database[k][entrytype][o][key]	
					if meta:
						print k
						pp = pprint.PrettyPrinter(indent=4)
						pp.pprint(database[k][entrytype]['Meta'])
				if plotting:		
					_plot_table(values,rowLabels,colLabels)

		else:           # only display specific studies
			if not observations: # full overview!
				colLabels = studies
				for k in colLabels:
					obs      = database[k][entrytype].keys()
					des = []
					for ob in obs:
						if not ob=='Meta':
							des.append(database[k][entrytype][ob]['description'])
					observations = list(set(observations+obs))
					rowLabels = list(set(rowLabels + des)) # this creates a list of unique(!) observations
				observations.remove('Meta')	
				nrows = len(rowLabels)
				ncols = len(colLabels)
				values =  [['not tested' for _ in range(ncols)] for _ in range(nrows)] 
				for i,k in enumerate(colLabels):
					for j,o in enumerate(observations):
						if o in database[k][entrytype].keys(): 
							key = 'value'
							values[j][i] = database[k][entrytype][o][key]
					if meta:
						print k
						pp = pprint.PrettyPrinter(indent=4)
						pp.pprint(database[k][entrytype]['Meta'])	
				if plotting:		
					_plot_table(values,rowLabels,colLabels)
			else:                # only display specific observations
				# go through all studies 
				colLabels = studies
				for o in observations:
					for k in studies:
						des = []
						des.append(database[k][entrytype][o]['description'])
					rowLabels = list(set(rowLabels+des))
				nrows = len(rowLabels)
				ncols = len(colLabels)
				values =  [['not tested' for _ in range(ncols)] for _ in range(nrows)] #np.zeros((nrows,ncols))
				for i,k in enumerate(colLabels):
					for j,o in enumerate(observations):
						if o in database[k][entrytype].keys(): 
							key = 'value'
							values[j][i] = database[k][entrytype][o][key]	
					if meta:
						print k
						pp = pprint.PrettyPrinter(indent=4)
						pp.pprint(database[k][entrytype]['Meta'])
				if plotting:		
					_plot_table(values,rowLabels,colLabels)
                  
                   
	return values,rowLabels,colLabels
		
def plot_statistics(stats,rowLables,colLabels):
	'''

 	Parameters
	-----------------
	
	Returns
	-----------------
	
	'''
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.table(cellText=stats,rowLabels=rowLabels,colLabels=colLabels,loc='center')
	ax.axis('off')


def _plot_table(cellText,rowLabels,colLabels):
	'''

 	Parameters
	-----------------
	
	Returns
	-----------------
	
	'''
	fig = plt.figure(figsize=(10,20))
	ax = fig.add_subplot(111)
	ax.table(cellText=cellText,rowLabels=rowLabels,colLabels=colLabels,loc='center')
	ax.axis('off')

def _load_obj(name ):
	with open(name + '.pkl', 'rb') as f:
		return pickle.load(f)

def get_studies(dbname='Databases/ASSR_schizophrenia_experimental_database'):
	'''Gives a list of all study identifiers in the database.

 	Parameters
	-----------------
	
	Returns
	-----------------
	
	'''
	# load database
	
	database = _load_obj(dbname)

	studies = database.keys()

	return studies

def get_observations(entrytype='Full',dbname='Databases/ASSR_schizophrenia_experimental_database'):
	'''Gives a list of all observation identifiers in the database.

 	Parameters
	-----------------
	
	Returns
	-----------------
	
	'''
	# load database
	
	database = _load_obj(dbname)

	keys = database.keys()
	observations = []
	for k in keys:
		obs = database[k][entrytype].keys()
		for ob in obs:
			if not ob=='Meta':
				des=database[k][entrytype][ob]['description']
				observations = list(set(observations + [ob+' :'+des])) # this creates a list of unique(!) observations
	return observations



def get_meta(item,dbname='Databases/ASSR_schizophrenia_experimental_database'):      
	'''Gives a list of all study identifiers in the database.
 	Parameters
	-----------------
	
	Returns
	-----------------
	'''
	'''
	# load database
	database = _load_obj(dbname)
	keys = database.keys()
	itema = []
	for k in keys:
		trele = database[k][entrytype].keys()
		mes=database[k][entrytype][trele]['Meta['+item+']']
		itema = list(set([trele +' :'+mes])) # this creates a list of unique(!) '''
        

                
	return item



        
