import sciunit

from capabilities import Produce4040,Produce3030,Produce2020,Produce2040,Produce4020
from prediction_capabilities import PredictionProduce1010




import math,sys,os
import random
import numpy as np

import matplotlib.pylab as plt


#from Modules.NML2Files import singleRun

#from Modules.Genesis import genesisModelRun

from Modules.Vierling import simpleModel

### The model classes ###



# Simple test model class
class TestModel(sciunit.Model,Produce4040,Produce3030,Produce2020,Produce2040,Produce4020):
    """A simple test model that does nothing except giving back arbitrary values"""
    
    def __init__(self, name=None): 
        
        super(TestModel, self).__init__(name=name)

    def produce_4040(self):

	control4040 = 1.0
	schiz4040 = 0.4

        return [control4040,schiz4040]

    def produce_3030(self):

	control3030 = 1.0
	schiz3030 = 1.01

        return [control3030,schiz3030]

    def produce_2020(self):

	control2020 = 1.0
	schiz2020 = 0.4

        return [control2020,schiz2020]

    def produce_2040(self):

	control2040 = 1.0
	schiz2040 = 0.4

        return [control2040,schiz2040]

    def produce_4020(self):

	control4020 = 1.0
	schiz4020 = 0.4

        return [control4020,schiz4020]




# This will implement the ACnet2 model using pyNeuroML
# Since we have a model of a biomarker of schizophrenia, our 'model' has to implement
# two instances of the model, the control network and the 'schizophrenia-like' network (The 'model
# will be judged on differences between these networks; and it should also be checked that the control 
# network behaves reasonably!). Therefore, the model class takes two different sets of parameters.
class ACnet2NML2Model(sciunit.Model, 
                 Produce4040):
    """The ACnet2 model (NML2 version using the reduced model of the Hay et al. pyramidal cell) """


### TO DO: Get generation and simulation of NML2 version to run!! ###
    
    def __init__(self, controlparams, schizparams, time=500, name=None): # TO DO specifiy parameters!
        self.controlparams = controlparams
        self.schizparams = schizparams 
        super(ACnet2NML2Model, self).__init__(name=name, controlparams = controlparams, schizparams = schizparams)

    def produce_4040(self):
	'''
	
	'''
	# generate the control network and run simulation
	control4040 = singleRun(self.controlparams,40.0,'forty')

	# generate the schizophrenia-like network and run simulation
	schiz4040 = singleRun(self.schizparams,40.0,'forty')


        return [control4040,schiz4040]


class ACnet2GenesisModel(sciunit.Model, 
                 Produce4040):
    """The ACnet2 model (using a slightly modified version of the original Genesis model. For more details see Beeman (2013) and Metzner et al. (2016))"""


### TO DO: Get generation and simulation of Genesis version to run!! ###
    
    def __init__(self, controlparams, schizparams, name=None): 
	'''
	Constructor method. Both parameter sets, for the control and the schizophrenia-like network, have to be
	a dictionary containing the following parmaeters (Filename,Stimulation Frequency,Random Seed,E-E Weight,I-E Weight,E-I Weight,I-I Weight,Background Noise Weight,E-Drive Weight,I-Drive 	
	Weight,Background Noise Frequency)
	Parameters:
	controlparams: Parameters for the control network
	schizparams: Parameters for the schizophrenia-like network
	name: name of the instance
	'''
        self.controlparams = controlparams
        self.schizparams = schizparams 
        super(ACnet2GenesisModel, self).__init__(name=name, controlparams = controlparams, schizparams = schizparams)

    def produce_4040(self):
	'''
	
	'''
	# generate the control network and run simulation
	control4040 = genesisModelRun(self.controlparams,40.0,'forty')

	# generate the schizophrenia-like network and run simulation
	schiz4040 = genesisModelRun(self.schizparams,40.0,'forty')


        return [control4040,schiz4040]



class VierlingSimpleModel(sciunit.Model, 
                 Produce4040,Produce3030,Produce2020,Produce2040,Produce4020,PredictionProduce1010):
    """The simple model from Vierling-Claassen et al. (2008) """
    
    def __init__(self, controlparams, schizparams,seed=12345, time=500, name=None): 
        self.controlparams = controlparams
        self.schizparams = schizparams 
	self.time = time
	self.name = name
	self.seed = seed
        super(VierlingSimpleModel, self).__init__(name=name, controlparams = controlparams, schizparams = schizparams,time=time)

    def produce_4040(self):

	# generate the control network and run simulation
	control_model = simpleModel(self.controlparams)
	print 'Control model created'
	control_meg,_,_ = control_model.run(40.0,self.seed,self.time,0,0,0)
	print 'Control model simulated' 
	control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
	print 'Control PSD calculated'
	control4040 = np.sum(control_pxx[19:22]) # Frequency range from 38-42Hz 

	# generate the schizophrenia-like network and run simulation
	schiz_model = simpleModel(self.schizparams)
	print 'Schiz model created'
	schiz_meg,_,_ = schiz_model.run(40.0,self.seed,self.time,0,0,0)
	print 'Schiz model simulated' 
	schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
	print 'Schiz PSD calculated'
	schiz4040 = np.sum(schiz_pxx[19:22]) # Frequency range from 38-42Hz


        return [control4040,schiz4040]


    def produce_3030(self):

	# generate the control network and run simulation
	control_model = simpleModel(self.controlparams)
	print 'Control model created'
	control_meg,_,_ = control_model.run(30.0,self.seed,self.time,0,0,0)
	print 'Control model simulated' 
	control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
	print 'Control PSD calculated'
	control3030 = np.sum(control_pxx[14:17]) # Frequency range from 28-32Hz 

	# generate the schizophrenia-like network and run simulation
	schiz_model = simpleModel(self.schizparams)
	print 'Schiz model created'
	schiz_meg,_,_ = schiz_model.run(30.0,self.seed,self.time,0,0,0)
	print 'Schiz model simulated' 
	schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
	print 'Schiz PSD calculated'
	schiz3030 = np.sum(schiz_pxx[14:17]) # Frequency range from 28-32Hz


	#print freqs[14:18]*1000


        return [control3030,schiz3030]

    def produce_2020(self):

	# generate the control network and run simulation
	control_model = simpleModel(self.controlparams)
	print 'Control model created'
	control_meg,_,_ = control_model.run(20.0,self.seed,self.time,0,0,0)
	print 'Control model simulated' 
	control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
	print 'Control PSD calculated'
	control2020 = np.sum(control_pxx[9:12]) # Frequency range from 18-22Hz 

	# generate the schizophrenia-like network and run simulation
	schiz_model = simpleModel(self.schizparams)
	print 'Schiz model created'
	schiz_meg,_,_ = schiz_model.run(20.0,self.seed,self.time,0,0,0)
	print 'Schiz model simulated' 
	schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
	print 'Schiz PSD calculated'
	schiz2020 = np.sum(schiz_pxx[9:12]) # Frequency range from 28-32Hz


	#print freqs[9:12]*1000


        return [control2020,schiz2020]

    def produce_2040(self):

	# generate the control network and run simulation
	control_model = simpleModel(self.controlparams)
	print 'Control model created'
	control_meg,_,_ = control_model.run(40.0,self.seed,self.time,0,0,0)
	print 'Control model simulated' 
	control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
	print 'Control PSD calculated'
	control2040 = np.sum(control_pxx[9:12]) # Frequency range from 18-22Hz 

	# generate the schizophrenia-like network and run simulation
	schiz_model = simpleModel(self.schizparams)
	print 'Schiz model created'
	schiz_meg,_,_ = schiz_model.run(40.0,self.seed,self.time,0,0,0)
	print 'Schiz model simulated' 
	schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
	print 'Schiz PSD calculated'
	schiz2040 = np.sum(schiz_pxx[9:12]) # Frequency range from 28-32Hz


        return [control2040,schiz2040]

    def produce_4020(self):

	# generate the control network and run simulation
	control_model = simpleModel(self.controlparams)
	print 'Control model created'
	control_meg,_,_ = control_model.run(20.0,self.seed,self.time,0,0,0)
	print 'Control model simulated' 
	control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
	print 'Control PSD calculated'
	control4020 = np.sum(control_pxx[19:22]) # Frequency range from 18-22Hz 

	# generate the schizophrenia-like network and run simulation
	schiz_model = simpleModel(self.schizparams)
	print 'Schiz model created'
	schiz_meg,_,_ = schiz_model.run(20.0,self.seed,self.time,0,0,0)
	print 'Schiz model simulated' 
	schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
	print 'Schiz PSD calculated'
	schiz4020 = np.sum(schiz_pxx[19:22]) # Frequency range from 28-32Hz


        return [control4020,schiz4020]

    def prediction_produce_1010(self):

	# generate the control network and run simulation
	control_model = simpleModel(self.controlparams)
	print 'Control model created'
	control_meg,_,_ = control_model.run(10.0,self.seed,self.time,0,0,0)
	print 'Control model simulated' 
	control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
	print 'Control PSD calculated'
	control1010 = np.sum(control_pxx[9:12]) # Frequency range from 8-12Hz 

	# generate the schizophrenia-like network and run simulation
	schiz_model = simpleModel(self.schizparams)
	print 'Schiz model created'
	schiz_meg,_,_ = schiz_model.run(10.0,self.seed,self.time,0,0,0)
	print 'Schiz model simulated' 
	schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
	print 'Schiz PSD calculated'
	schiz1010 = np.sum(schiz_pxx[9:12]) # Frequency range from 28-32Hz



        return [control1010,schiz1010]


class VierlingSimpleModelRobust(sciunit.Model, 
                 Produce4040,Produce3030,Produce2020,Produce2040,Produce4020):
    """The simple model from Vierling-Claassen et al. (2008) """
    
    def __init__(self, controlparams, schizparams,seeds, time=500, name=None): 
        self.controlparams = controlparams
        self.schizparams = schizparams 
	self.time = time
	self.name = name
	self.seeds = seeds
        super(VierlingSimpleModelRobust, self).__init__(name=name, controlparams = controlparams, schizparams = schizparams,time=time,seeds=seeds)

    def produce_4040(self):
	'''
	 Simulates 40Hz drive to the control and the schizophrenia-like network for all random seeds, calculates a Fourier transform of the simulated MEG 
	 and extracts the power in the 40Hz frequency band for each simulation. Returns the mean power for the control and the schizophrenia-like network, respectively.
	'''
	control4040 = np.zeros((len(self.seeds),))
	schiz4040 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(40.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control4040[i] = np.sum(control_pxx[19:22]) # Frequency range from 38-42Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(40.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz4040[i] = np.sum(schiz_pxx[19:22]) # Frequency range from 38-42Hz

	mcontrol4040 = np.mean(control4040)
	mschiz4040 = np.mean(schiz4040)

        return [mcontrol4040,mschiz4040]

    def produce_4040_plus(self):
	'''
	 Simulates 40Hz drive to the control and the schizophrenia-like network for all random seeds, calculates a Fourier transform of the simulated MEG 
	 and extracts the power in the 40Hz frequency band for each simulation. Returns the mean power and the power for all individual simulations for the 
	 control and the schizophrenia-like network, respectively.
	'''
	control4040 = np.zeros((len(self.seeds),))
	schiz4040 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(40.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control4040[i] = np.sum(control_pxx[19:22]) # Frequency range from 38-42Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(40.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz4040[i] = np.sum(schiz_pxx[19:22]) # Frequency range from 38-42Hz

	mcontrol4040 = np.mean(control4040)
	mschiz4040 = np.mean(schiz4040)

        return [mcontrol4040,mschiz4040,control4040,schiz4040]

    def produce_3030(self):
	control3030 = np.zeros((len(self.seeds),))
	schiz3030 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(30.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control3030[i] = np.sum(control_pxx[14:17]) # Frequency range from 28-32Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(30.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz3030[i] = np.sum(schiz_pxx[14:17]) # Frequency range from 28-32Hz


	mcontrol3030 = np.mean(control3030)
	mschiz3030 = np.mean(schiz3030)


        return [mcontrol3030,mschiz3030]

    def produce_3030_plus(self):
	control3030 = np.zeros((len(self.seeds),))
	schiz3030 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(30.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control3030[i] = np.sum(control_pxx[14:17]) # Frequency range from 28-32Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(30.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz3030[i] = np.sum(schiz_pxx[14:17]) # Frequency range from 28-32Hz


	mcontrol3030 = np.mean(control3030)
	mschiz3030 = np.mean(schiz3030)


        return [mcontrol3030,mschiz3030,control3030,schiz3030]

    def produce_2020(self):
	control2020 = np.zeros((len(self.seeds),))
	schiz2020 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(20.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control2020[i] = np.sum(control_pxx[9:12]) # Frequency range from 18-22Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(20.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz2020[i] = np.sum(schiz_pxx[9:12]) # Frequency range from 28-32Hz

	mcontrol2020 = np.mean(control2020)
	mschiz2020 = np.mean(schiz2020)


        return [mcontrol2020,mschiz2020]

    def produce_2020_plus(self):
	control2020 = np.zeros((len(self.seeds),))
	schiz2020 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(20.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control2020[i] = np.sum(control_pxx[9:12]) # Frequency range from 18-22Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(20.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz2020[i] = np.sum(schiz_pxx[9:12]) # Frequency range from 28-32Hz

	mcontrol2020 = np.mean(control2020)
	mschiz2020 = np.mean(schiz2020)


        return [mcontrol2020,mschiz2020,control2020,schiz2020]

    def produce_2040(self):
	control2040 = np.zeros((len(self.seeds),))
	schiz2040 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(40.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control2040[i] = np.sum(control_pxx[9:12]) # Frequency range from 18-22Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(40.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz2040[i] = np.sum(schiz_pxx[9:12]) # Frequency range from 28-32Hz

	mcontrol2040 = np.mean(control2040)
	mschiz2040 = np.mean(schiz2040)


        return [mcontrol2040,mschiz2040]

    def produce_2040_plus(self):
	control2040 = np.zeros((len(self.seeds),))
	schiz2040 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(40.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control2040[i] = np.sum(control_pxx[9:12]) # Frequency range from 18-22Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(40.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz2040[i] = np.sum(schiz_pxx[9:12]) # Frequency range from 28-32Hz

	mcontrol2040 = np.mean(control2040)
	mschiz2040 = np.mean(schiz2040)


        return [mcontrol2040,mschiz2040,control2040,schiz2040]

    def produce_4020(self):
	control4020 = np.zeros((len(self.seeds),))
	schiz4020 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(20.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control4020[i] = np.sum(control_pxx[19:22]) # Frequency range from 18-22Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(20.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz4020[i] = np.sum(schiz_pxx[19:22]) # Frequency range from 28-32Hz


	mcontrol4020 = np.mean(control4020)
	mschiz4020 = np.mean(schiz4020)



        return [mcontrol4020,mschiz4020]

    def produce_4020_plus(self):
	control4020 = np.zeros((len(self.seeds),))
	schiz4020 = np.zeros((len(self.seeds),))

	for i,s in enumerate(self.seeds):
		print 'Seed number:',i
		# generate the control network and run simulation
		control_model = simpleModel(self.controlparams)
		print 'Control model created'
		control_meg,_,_ = control_model.run(20.0,s,self.time,0,0,0)
		print 'Control model simulated' 
		control_pxx,freqs = control_model.calculatePSD(control_meg,self.time)
		print 'Control PSD calculated'
		control4020[i] = np.sum(control_pxx[19:22]) # Frequency range from 18-22Hz 

		# generate the schizophrenia-like network and run simulation
		schiz_model = simpleModel(self.schizparams)
		print 'Schiz model created'
		schiz_meg,_,_ = schiz_model.run(20.0,s,self.time,0,0,0)
		print 'Schiz model simulated' 
		schiz_pxx,freqs = schiz_model.calculatePSD(schiz_meg,self.time)
		print 'Schiz PSD calculated'
		schiz4020[i] = np.sum(schiz_pxx[19:22]) # Frequency range from 28-32Hz


	mcontrol4020 = np.mean(control4020)
	mschiz4020 = np.mean(schiz4020)



        return [mcontrol4020,mschiz4020,control4020,schiz4020]
