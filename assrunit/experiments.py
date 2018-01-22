################################################	  
# Database of experimental observations	       #  	
#					       #
# The idea is to create database entries here  #
# and save everything, so that the database    #
# can be loaded whenever needed.               #
################################################


import pickle

# Each study is represented by 3 (or in the end maybe even more) different entries:
# ..._full: contains all observations from this study
# ..._full_qual: contains the same observations as ..._full, however, does not quantify differences (such as a ratio between controls and patients mean power values)
#           Instead only qualitative differences are described (so far, 3 levels [lower, equal, higher], maybe eventually 5 or more levels?) TODO: this should now be calculated from full



# Kwon et al., J?, 1999  

kwon_full = {'Data':{'4040' : {'groups': ['control','schiz'],'values' : [13.8,6.21] , 'description':'40 Hz power at 40 Hz drive'}, '3030' : {'groups': ['control','schiz'],'values' : [8.63,8.97] , 'description':'30 Hz power at 30 Hz drive'}, '2020' : {'groups': ['control','schiz'],'values' : [4.83,9.66] , 'description':'20 Hz power at 20 Hz drive'}, '2040' : {'groups': ['control','schiz'],'values' : [1.38,4.49] , 'description':'20 Hz power at 40 Hz drive'}, '4020' : {'groups': ['control','schiz'],'values' : [5.52,3.11] , 'description':'40 Hz power at 20 Hz drive'}}, 'Meta': {'Measure':{'Value': 'Mean Absolute Power','Location':'Midline frontal electrode','Modality':'EEG','Processing':'Butterworth bandpass-filtered time averages followed by Fourier transform'},'Subjects': 'Schizophrenia vs Control','Number of subjects':'15 (Ctrl) and 15 (Scz)', 'Paradigm': 'Click-train','Comments':'Values estimated from figures, since values are not provided'  } }

kwon_full_qual = {'Data':'4040' : {'groups': 'control vs. schiz','value' : 'lower' , 'description':'40 Hz power at 40 Hz drive'}, '3030' : {'groups': 'control vs. schiz','value' :'equal', 'description':'30 Hz power at 30 Hz drive' }, '2020' : {'groups': 'control vs. schiz','value' : 'higher', 'description':'20 Hz power at 20 Hz drive' }, '2040' : {'groups': 'control vs. schiz','value' : 'higher' , 'description':'20 Hz power at 40 Hz drive'}, '4020' : {'groups': 'control vs. schiz','value' : 'lower' , 'description':'40 Hz power at 20 Hz drive'}}, 'Meta': {'Measure':{'Value': 'Mean Absolute Power','Location':'Midline frontal electrode','Modality':'EEG','Processing':'Butterworth bandpass-filtered time averages followed by Fourier transform'},'Subjects': 'Schizophrenia vs Control','Number of subjects':'15 (Ctrl) and 15 (Scz)', 'Paradigm': 'Click-train','Comments':'Values estimated from figures, since values are not provided'  } }

kwon = {'Full':kwon_full,'Full_qual':kwon_full_qual}

# Vierling-Claassen et al., J ?, 2008

vierling_full = {'Data':'4040' : {'groups': ['control','schiz'],'values' : [1.2*10e-19,0.42*10e-19] , 'description':'40 Hz power at 40 Hz drive'}, '3030' : {'groups': ['control','schiz'],'values' : [0.75*10e-19,0.99*10e-19] , 'description':'30 Hz power at 30 Hz drive'}, '2020' : {'groups': ['control','schiz'],'values' : [0.36*10e-19,0.78*10e-19] , 'description':'20 Hz power at 20 Hz drive'}, '2040' : {'groups': ['control','schiz'],'values' : [0.21*10e-19,0.51*10e-19] , 'description':'20 Hz power at 40 Hz drive'}, '4020' : {'groups': ['control','schiz'],'values' : [0.51*10e-19,0.18*10e-19] , 'description':'40 Hz power at 20 Hz drive'}}, 'Meta': {'Measure':{'Value': 'Mean Absolute Power','Location':'Left hemisphere','Modality':'MEG','Processing':'Time-averaging followed by PSD using Welch`s method'},'Subjects': 'Schizophrenia vs Control','Number of Subjects': '12 (Ctrl) and 12 (Scz)', 'Paradigm': 'Click-train','Comments':'Values estimated from figures, since values are not provided'  } }

vierling_full_qual = {'Data':'4040' : {'groups': 'control vs. schiz','value' : 'lower' , 'description':'40 Hz power at 40 Hz drive'}, '3030' : {'groups': 'control vs. schiz','value' :'equal', 'description':'30 Hz power at 30 Hz drive' }, '2020' : {'groups': 'control vs. schiz','value' : 'higher', 'description':'20 Hz power at 20 Hz drive' }, '2040' : {'groups': 'control vs. schiz','value' : 'higher' , 'description':'20 Hz power at 40 Hz drive'}, '4020' : {'groups': 'control vs. schiz','value' : 'lower' , 'description':'40 Hz power at 20 Hz drive'}},  'Meta': {'Measure':{'Value': 'Mean Absolute Power','Location':'Left hemisphere','Modality':'MEG','Processing':'Time-averaging followed by PSD using Welch`s method'},'Subjects': 'Schizophrenia vs Control','Number of Subjects': '12 (Ctrl) and 12 (Scz)', 'Paradigm': 'Click-train'  ,'Comments':'Values estimated from figures, since values are not provided' } }

vierling = {'Full':vierling_full,'Full_qual':vierling_full_qual}

# Krishnan et al., Neuroimage, 2009

#### Data not complete!!! ####

krishnan_full = {'Data':{'0505' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'5 Hz power at 5 Hz drive'}, '1010' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'10 Hz power at 10 Hz drive'}, '1515' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'15 Hz power at 15 Hz drive'}, '2020' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'20 Hz power at 20 Hz drive'},'2525' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'25 Hz power at 25 Hz drive'},'3030' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'30 Hz power at 30 Hz drive'},'3535' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'35 Hz power at 35 Hz drive'},'4040' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'40 Hz power at 40 Hz drive'},'4545' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'45 Hz power at 45 Hz drive'},'5050' : {'groups': ['control','schiz'],'values' : [1.0,1.0] , 'description':'50 Hz power at 50 Hz drive'}},'Meta': {'Measure':{'Value':'Mean baseline corrected power','Electrode/Position':'?'},'Subjects': 'Schizophrenia', 'Paradigm': 'Amplitude-modulated tones', 'Number of subjects': 0   }}

krishnan_full_qual = {'Data':{'0505' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'5 Hz power at 5 Hz drive'}, '1010' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'10 Hz power at 10 Hz drive'}, '1515' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'15 Hz power at 15 Hz drive'}, '2020' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'20 Hz power at 20 Hz drive'},'2525' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'25 Hz power at 25 Hz drive'},'3030' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'30 Hz power at 30 Hz drive'},'3535' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'35 Hz power at 35 Hz drive'},'4040' : {'groups': 'control vs. schiz','value' : 'lower' , 'description':'40 Hz power at 40 Hz drive'},'4545' : {'groups': 'control vs. schiz','value' : 'lower' , 'description':'45 Hz power at 45 Hz drive'},'5050' : {'groups': 'control vs. schiz','value' : 'lower' , 'description':'50 Hz power at 50 Hz drive'},'2040' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'20 Hz power at 40 Hz drive'}, '4020' : {'groups': 'control vs. schiz','value' : 'equal' , 'description':'40 Hz power at 20 Hz drive'}},'Meta': {'Measure':{'Value':'Mean baseline corrected power','Location':'Cz in a 10-20 setting','Modality':'EEG','Processing':'Least square linear FIR filtered and Hilbert transformed'},'Subjects': 'Schizophrenia vs Control', 'Paradigm': 'Amplitude-modulated tones; carrier freqeuncy 1kHz', 'Number of subjects': '21 (Ctrl) vs 21 (Scz)'   }}

krishnan = {'Full':krishnan_full,'Full_qual':krishnan_full_qual}

# Brenner et al., American Journal of Psychiatry, 2003

# Hong et al., , 2004


# Combine all dictionaries
database = {'Kwon_1999': kwon,'Vierling_2008': vierling,'Krishnan_2009': krishnan}



def saveObj(obj, name ):
	with open(name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, protocol=2)


saveObj(database,'Databases/ASSR_schizophrenia_experimental_database')




