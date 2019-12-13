import sciunit

from capabilities import ProduceXY

from Modules.Vierling import simpleModel
from Modules.Genesis import beemanGenesisModel
from Modules.NML2 import beemanNML2Model


import numpy as np

### The model classes ###


class VierlingSimpleModel(sciunit.Model, ProduceXY):
    """The simple model from Vierling-Claassen et al. (2008) """

    def __init__(
        self,
        controlparams,
        schizparams,
        seed=12345,
        time=500,
        name="VierlingSimpleModel",
    ):
        self.controlparams = controlparams
        self.schizparams = schizparams
        self.time = time
        self.name = name
        self.seed = seed
        super(VierlingSimpleModel, self).__init__(
            name=name,
            controlparams=controlparams,
            schizparams=schizparams,
            seed=seed,
            time=time,
        )

    def produce_XY(self, stimfrequency=40.0, powerfrequency=40.0):

        lbound = (powerfrequency / 2) - 1
        ubound = (powerfrequency / 2) + 2

        # generate the control network and run simulation
        control_model = simpleModel(self.controlparams)
        print "Control model created"
        control_meg, _, _ = control_model.run(
            stimfrequency, self.seed, self.time, 0, 0, 0
        )
        print "Control model simulated"
        control_pxx, freqs = control_model.calculatePSD(control_meg, self.time)
        print "Control PSD calculated"
        controlXY = np.sum(control_pxx[lbound:ubound])  # Frequency range from 38-42Hz

        # generate the schizophrenia-like network and run simulation
        schiz_model = simpleModel(self.schizparams)
        print "Schiz model created"
        schiz_meg, _, _ = schiz_model.run(stimfrequency, self.seed, self.time, 0, 0, 0)
        print "Schiz model simulated"
        schiz_pxx, freqs = schiz_model.calculatePSD(schiz_meg, self.time)
        print "Schiz PSD calculated"
        schizXY = np.sum(schiz_pxx[lbound:ubound])  # Frequency range from 38-42Hz

        return [controlXY, schizXY]


class VierlingSimpleModelRobust(sciunit.Model, ProduceXY):
    """The simple model from Vierling-Claassen et al. (2008) """

    def __init__(self, controlparams, schizparams, seeds, time=500, name=None):
        self.controlparams = controlparams
        self.schizparams = schizparams
        self.time = time
        self.name = name
        self.seeds = seeds
        super(VierlingSimpleModelRobust, self).__init__(
            name=name,
            controlparams=controlparams,
            schizparams=schizparams,
            time=time,
            seeds=seeds,
        )

    def produce_XY(self, stimfrequency=40.0, powerfrequency=40.0):
        """
	 Simulates Y Hz drive to the control and the schizophrenia-like network for all random seeds, calculates a Fourier transform of the simulated MEG
	 and extracts the power in the X Hz frequency band for each simulation. Returns the mean power for the control and the schizophrenia-like network, respectively.
	"""

        lbound = (powerfrequency / 2) - 1
        ubound = (powerfrequency / 2) + 2

        controlXY = np.zeros((len(self.seeds),))
        schizXY = np.zeros((len(self.seeds),))

        for i, s in enumerate(self.seeds):
            print ("Seed number:", i)
            # generate the control network and run simulation
            control_model = simpleModel(self.controlparams)
            print "Control model created"
            control_meg, _, _ = control_model.run(stimfrequency, s, self.time, 0, 0, 0)
            print "Control model simulated"
            control_pxx, freqs = control_model.calculatePSD(control_meg, self.time)
            print "Control PSD calculated"
            controlXY[i] = np.sum(control_pxx[lbound:ubound])

            # generate the schizophrenia-like network and run simulation
            schiz_model = simpleModel(self.schizparams)
            print "Schiz model created"
            schiz_meg, _, _ = schiz_model.run(stimfrequency, s, self.time, 0, 0, 0)
            print "Schiz model simulated"
            schiz_pxx, freqs = schiz_model.calculatePSD(schiz_meg, self.time)
            print "Schiz PSD calculated"
            schizXY[i] = np.sum(schiz_pxx[lbound:ubound])

        mcontrolXY = np.mean(controlXY)
        mschizXY = np.mean(schizXY)

        return [mcontrolXY, mschizXY]

    def produce_XY_plus(self, stimfrequency=40.0, powerfrequency=40.0):
        """
	 Simulates Y Hz drive to the control and the schizophrenia-like network for all random seeds, calculates a Fourier transform of the simulated MEG
	 and extracts the power in the X Hz frequency band for each simulation. Returns the mean power and the power for all individual simulations for the
	 control and the schizophrenia-like network, respectively.
	"""

        lbound = (powerfrequency / 2) - 1
        ubound = (powerfrequency / 2) + 2

        controlXY = np.zeros((len(self.seeds),))
        schizXY = np.zeros((len(self.seeds),))

        for i, s in enumerate(self.seeds):
            print "Seed number:", i
            # generate the control network and run simulation
            control_model = simpleModel(self.controlparams)
            print "Control model created"
            control_meg, _, _ = control_model.run(stimfrequency, s, self.time, 0, 0, 0)
            print "Control model simulated"
            control_pxx, freqs = control_model.calculatePSD(control_meg, self.time)
            print "Control PSD calculated"
            controlXY[i] = np.sum(control_pxx[lbound:ubound])

            # generate the schizophrenia-like network and run simulation
            schiz_model = simpleModel(self.schizparams)
            print "Schiz model created"
            schiz_meg, _, _ = schiz_model.run(stimfrequency, s, self.time, 0, 0, 0)
            print "Schiz model simulated"
            schiz_pxx, freqs = schiz_model.calculatePSD(schiz_meg, self.time)
            print "Schiz PSD calculated"
            schizXY[i] = np.sum(schiz_pxx[lbound:ubound])

        mcontrolXY = np.mean(controlXY)
        mschizXY = np.mean(schizXY)

        return [mcontrolXY, mschizXY, controlXY, schizXY]


class BeemanGenesisModel(sciunit.Model, ProduceXY):
    """The auditory cortex model from Beeman (2013) [using a slightly modified version of the original Genesis model; For more details see Metzner et al. (2016)]"""

    def __init__(self, controlparams, schizparams):
        """
	Constructor method. Both parameter sets, for the control and the schizophrenia-like network, have to be
	a dictionary containing the following parmaeters (Filename,Stimulation Frequency,Random Seed,E-E Weight,I-E Weight,E-I Weight,I-I Weight,Background Noise Weight,E-Drive Weight,I-Drive
	Weight,Background Noise Frequency)
	Parameters:
	controlparams: Parameters for the control network
	schizparams: Parameters for the schizophrenia-like network
	name: name of the instance
	"""
        self.controlparams = controlparams
        self.schizparams = schizparams
        super(BeemanGenesisModel, self).__init__(
            controlparams=controlparams, schizparams=schizparams
        )

    def produce_XY(self, stimfrequency=40.0, powerfrequency=40.0):
        """
	 Simulates Y Hz drive to the control and the schizophrenia-like network for all random seeds, calculates a Fourier transform of the simulated MEG
	 and extracts the power in the X Hz frequency band for each simulation. Returns the mean power for the control and the schizophrenia-like network, respectively.
	 Note: So far, only three power bands [20,30,40] are possible.
	"""
        powerband = "forty"  # default frequency band
        if powerfrequency == 30.0:
            powerband = "thirty"
        elif powerfrequency == 20.0:
            powerband = "twenty"
        # generate the control network and run simulation
        print "Generating control model"
        ctrl_model = beemanGenesisModel(self.controlparams)
        print "Running control model"
        controlXY = ctrl_model.genesisModelRun(stimfrequency, powerband)

        # generate the schizophrenia-like network and run simulation
        print "Generating schizophrenia model"
        schiz_model = beemanGenesisModel(self.schizparams)
        print "Running schizophrenia model"
        schizXY = schiz_model.genesisModelRun(stimfrequency, powerband)

        return [controlXY, schizXY]


class BeemanNML2Model(sciunit.Model, ProduceXY):
    """NeuroML2 of the auditory cortex model from Beeman (2013)"""

    def __init__(self, controlparams, schizparams):
        """
	Constructor method. Both parameter sets, for the control and the schizophrenia-like network, have to be
	a dictionary containing the following parmaeters (Filename,Stimulation Frequency,Random Seed,E-E Weight,I-E Weight,E-I Weight,I-I Weight,Background Noise Weight,E-Drive Weight,I-Drive
	Weight,Background Noise Frequency)
	Parameters:
	controlparams: Parameters for the control network
	schizparams: Parameters for the schizophrenia-like network
	name: name of the instance
	"""
        self.controlparams = controlparams
        self.schizparams = schizparams
        super(BeemanNML2Model, self).__init__(
            controlparams=controlparams, schizparams=schizparams
        )

    def produce_XY(self, stimfrequency=40.0, powerfrequency=40.0):
        """
	 Simulates Y Hz drive to the control and the schizophrenia-like network for all random seeds, calculates a Fourier transform of the simulated MEG
	 and extracts the power in the X Hz frequency band for each simulation. Returns the mean power for the control and the schizophrenia-like network, respectively.
	"""
        drive_period = (
            1.0 / stimfrequency
        ) * 1000  # calculate drive period (in ms) from stimulation frequency
        # generate the control network and run simulation
        print "Generating control model"
        ctrl_model = beemanNML2Model(self.controlparams, drive_period)
        ctrl_model.createModel()
        print "Running control model"
        ctrl_model.singleRun()
        print "Analysing control model"
        controlXY = ctrl_model.analyse(powerfrequency)

        # generate the schizophrenia-like network and run simulation
        print "Generating schizophrenia model"
        schiz_model = beemanNML2Model(self.schizparams, drive_period)
        schiz_model.createModel()
        print "Running control model"
        schiz_model.singleRun()
        print "Analysing control model"
        schizXY = schiz_model.analyse(powerfrequency)

        return [controlXY, schizXY]
