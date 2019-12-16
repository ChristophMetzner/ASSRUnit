####################################################################
# Interfaces with the GENESIS version of the auditory cortex model of Beeman,
# BMC Neuroscience (Suppl. 1), 2013 (i.e. a slightly modified version
# as used in Metzner et al., Front Comp Neu, 2016)
#
# @author: Christoph Metzner, 02/11/2017
####################################################################
import os
import subprocess
import sys

import matplotlib.mlab as mlab
import numpy as np
import sciunit
from assrunit.capabilities import ProduceXY
from assrunit.constants import ACNET2_GENESIS_PATH


class GenesisModel(object):
    def __init__(self, params):
        # extract the model parameters from the params dictionary
        self.filename = params["Filename"]
        self.random_seed = params["Random Seed"]
        self.ee_weight = params["E-E Weight"]
        self.ie_weight = params["I-E Weight"]
        self.ei_weight = params["E-I Weight"]
        self.ii_weight = params["I-I Weight"]
        self.bg_weight = params["Background Noise Weight"]
        self.edrive_weight = params["E-Drive Weight"]
        self.idrive_weight = params["I-Drive Weight"]
        self.bg_noise_frequency = params["Background Noise Frequency"]

    def genesisModelRun(self, stimfrequency, power_band):
        """
        Runs the simulation, calculates the power spectrum
        and returns the power in the specified the frequency band (Note: so far only 3 frequency
        bands are possible; 20, 30 and 40 Hz).
        Parameters:
        stimfrequency:	the frequency at which the network is driven
        power_band:	the frequency band of interest
        """

        # put the execution string together
        execstring = "/usr/local/genesis-2.4/genesis/genesis -nosimrc -batch {} {} {} {} {} {} {} {} {} {} {} {}".format(
            os.path.join(ACNET2_GENESIS_PATH, "ACnet2-batch-new-standard.g"),
            self.filename,
            str(stimfrequency),
            str(self.random_seed),
            str(self.ee_weight),
            str(self.ie_weight),
            str(self.ei_weight),
            str(self.ii_weight),
            str(self.bg_weight),
            str(self.edrive_weight),
            str(self.idrive_weight),
            str(self.bg_noise_frequency),
        )

        print("running simulation")
        # execute the simulation
        self._runProcess(execstring)
        print("finished simulation")

        # load and analyse the data
        datafile = "EPSC_sum_" + self.filename + ".txt"
        pxx, freqs = self._calculate_psd(datafile)
        os.chdir("../notebooks/")

        # extract power at the frequency band of interest

        lbounds = {"forty": 93, "thirty": 69, "twenty": 44}
        ubounds = {"forty": 103, "thirty": 78, "twenty": 54}

        lb = lbounds[power_band]
        ub = ubounds[power_band]

        power = np.sum(pxx[lb:ub])

        return power

    def _runProcess(self, execstring):
        """
        This function executes the Genesis simulation in a shell.
        Parameters:
        execstring : the command which executes the Genesis model with all its parameters
        """

        return subprocess.call(execstring, shell=True)

    def _calculate_psd(self, datafile):
        """
        Calculates the power spectral density of the simulated EEG/MEG signal
        """
        i = 0
        if not datafile:
            print("No files were specified for plotting!")
            sys.exit()

        with open(datafile, "r") as fp:
            lines = fp.readlines()
            count = len(lines)

            tn = np.zeros(count)
            yn = np.zeros(count)
            i = 0
            for line in lines:
                # Note that tn[i] is replaced, and yn[i] is addded to,
                tn[i] = float(line[0])
                yn[i] = float(line[1])
                i += 1

        # Now do the plotting of the  array data
        dt = tn[1] - tn[0]
        # fourier sample rate
        fs = 1.0 / dt

        npts = len(yn)
        startpt = int(0.2 * fs)

        if (npts - startpt) % 2 != 0:
            startpt = startpt + 1

        yn = yn[startpt:]
        tn = tn[startpt:]
        nfft = len(tn) // 4
        overlap = nfft // 2

        pxx, freqs = mlab.psd(
            yn, NFFT=nfft, Fs=fs, noverlap=overlap, window=mlab.window_none
        )
        pxx[0] = 0.0

        return pxx, freqs


class BeemanGenesisModel(sciunit.Model, ProduceXY):
    """The auditory cortex model from Beeman (2013) [using a slightly modified version of the
    original Genesis model; For more details see Metzner et al. (2016)]"""

    def __init__(self, controlparams, schizparams):
        """
        Constructor method. Both parameter sets, for the control and the
        schizophrenia-like network, have to be a dictionary containing the following
        parmaeters (Filename,Stimulation Frequency,Random Seed,
        E-E Weight,I-E Weight,E-I Weight,I-I Weight,Background Noise Weight,E-Drive Weight,I-Drive
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
        Simulates Y Hz drive to the control and the schizophrenia-like network for all random
        seeds, calculates a Fourier transform of the simulated MEG
        and extracts the power in the X Hz frequency band for each simulation. Returns the mean
        power for the control and the schizophrenia-like network, respectively.
        Note: So far, only three power bands [20,30,40] are possible.
        """
        powerband = "forty"  # default frequency band
        if powerfrequency == 30.0:
            powerband = "thirty"
        elif powerfrequency == 20.0:
            powerband = "twenty"
        # generate the control network and run simulation
        print("Generating control model")
        ctrl_model = GenesisModel(self.controlparams)
        print("Running control model")
        controlXY = ctrl_model.genesisModelRun(stimfrequency, powerband)

        # generate the schizophrenia-like network and run simulation
        print("Generating schizophrenia model")
        schiz_model = BeemanGenesisModel(self.schizparams)
        print("Running schizophrenia model")
        schizXY = schiz_model.genesisModelRun(stimfrequency, powerband)

        return [controlXY, schizXY]
