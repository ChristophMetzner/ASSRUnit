####################################################################
# Interfaces with the GENESIS version of the auditory cortex model of Beeman, 
# BMC Neuroscience (Suppl. 1), 2013 (i.e. a slightly modified version
# as used in Metzner et al., Front Comp Neu, 2016) 
#
# @author: Christoph Metzner, 02/11/2017
####################################################################
import math,sys,os
import numpy as np
import shutil 
import subprocess 
import multiprocessing
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


class beemanGenesisModel(object):
    '''

    '''

    def __init__(self,params):
	# extract the model parameters from the params dictionary
	self.filename		= params['Filename']
	self.random_seed    	= params['Random Seed']
	self.ee_weight		= params['E-E Weight']	
	self.ie_weight		= params['I-E Weight']	
	self.ei_weight		= params['E-I Weight']	
	self.ii_weight		= params['I-I Weight']	
	self.bg_weight		= params['Background Noise Weight']	
	self.edrive_weight	= params['E-Drive Weight']	
	self.idrive_weight	= params['I-Drive Weight']	
	self.bg_noise_frequency	= params['Background Noise Frequency']



    def genesisModelRun(self,stimfrequency,power_band):
	'''
	Runs the simulation, calculates the power spectrum
	and returns the power in the specified the frequency band (Note: so far only 3 frequency bands are possible; 20, 30 and 40 Hz).
	Parameters:
	stimfrequency:	the frequency at which the network is driven
	power_band:	the frequency band of interest
	'''

	# put the execution string together
	os.chdir('ACnet2-Genesis/')
	execstring = ' genesis ACnet2-batch-new-standard.g ' + self.filename+ ' ' + str(stimfrequency)+ ' ' + str(self.random_seed)+ ' ' + str(self.ee_weight)+ ' ' + str(self.ie_weight)+ ' ' + str(self.ei_weight)+ ' ' + str(self.ii_weight)+ ' ' + str(self.bg_weight)+ ' ' + str(self.edrive_weight)+ ' ' + str(self.idrive_weight)+ ' ' + str(self.bg_noise_frequency)
	
	# execute the simulation
	self._runProcess(execstring)


	# load and analyse the data
	datafile = 'EPSC_sum_' + self.filename + '.txt'
	pxx,freqs = self._calculatePSD(datafile)
	os.chdir('../')

	fig = plt.figure()
	ax = fig.add_subplot(111)
	pxx[0] = 0.0
	ax.plot(1000*freqs,pxx)
    	ax.axis(xmin = 0, xmax = 100)
	plt.savefig(self.filename+'-PSD.png')
	
	# extract power at the frequency band of interest

	lbounds = {'forty': 93 ,'thirty': 69,'twenty': 44}
	ubounds = {'forty': 103,'thirty': 78,'twenty': 54}

	lb = lbounds[power_band]
	ub = ubounds[power_band]

	power = np.sum(pxx[lb:ub])


	return power 

    def _runProcess(self,execstring):
	'''
	This function executes the Genesis simulation in a shell.
	Parameters:
	execstring : the command which executes the Genesis model with all its parameters
	'''

	return subprocess.call(execstring, shell=True)

    def _calculatePSD(self,datafile):
	'''
	Calculates the power spectral density of the simulated EEG/MEG signal
	'''
	i = 0
	if len(datafile) > 0:
		fp = open(datafile, 'r')
		count = len(fp.readlines())

		fp.close()
		fp = open(datafile,'r')

		tn = np.zeros(count)
		yn = np.zeros(count)
		i=0
		for line in fp.readlines():
			data = line.split(" ")
		      	# Note that tn[i] is replaced, and yn[i] is addded to
		      	tn[i] = float(data[0]); yn[i] = float(data[1])
		      	i += 1

		  
	else:
	    	print "No files were specified for plotting!"
	    	sys.exit()     
	  

	# Now do the plotting of the  array data
	dt = tn[1] - tn[0]
	# fourier sample rate
	fs = 1. / dt


	npts = len(yn)
	startpt = int(0.2*fs)

	if (npts - startpt)%2!=0:
		startpt = startpt + 1

	yn = yn[startpt:]
	tn = tn[startpt:]
	nfft = len(tn)//4
	overlap = nfft//2


	pxx,freqs=mlab.psd(yn,NFFT=nfft,Fs=fs,noverlap=overlap,window=mlab.window_none)
	pxx[0] = 0.0

	
	return pxx, freqs



