####################################################################
# Interfaces with the NML2 version of the auditory cortex model of Beeman,
# BMC Neuroscience (Suppl. 1), 2013
#
# @author: Christoph Metzner, 10/11/2017
####################################################################
import math
import random
import os

import matplotlib.mlab as mlab
import neuroml.writers as writers
import numpy as np
import sciunit

from assrunit.constants import DATA_PATH
from assrunit.acnet2_nml2.controller import Controller
from assrunit.acnet2_nml2.helpers import add_connection
from assrunit.capabilities import ProduceXY
from neuroml import (
    ExplicitInput,
    IncludeType,
    Input,
    InputList,
    Instance,
    Location,
    Network,
    NeuroMLDocument,
    PoissonFiringSynapse,
    Population,
    Projection,
    SineGenerator,
)
from neuroml.utils import validate_neuroml2
from pyneuroml.lems.LEMSSimulation import LEMSSimulation


class NML2Model(object):
    """

    """

    def __init__(self, params, drive_period):
        # extract the model parameters from the params dictionary
        self.filename = params["Filename"]
        self.random_seed = params["Random Seed"]
        self.ee_weight = params["E-E Weight"]
        self.ie_weight = params["I-E Weight"]
        self.ei_weight = params["E-I Weight"]
        self.ii_weight = params["I-I Weight"]
        self.Edrive_weight = params["E-Drive Weight"]
        self.Idrive_weight = params["I-Drive Weight"]
        self.bg_weight = params["Background Noise Weight"]
        self.bg_noise_frequency = params["Background Noise Frequency"]
        self.sim_time = params["Simulation Time"]
        self.dt = params["Time Step"]
        self.Drive_period = drive_period

    def createModel(self):

        # File names of all components
        pyr_file_name = "../acnet2_nml2/cells/pyr_4_sym.cell.acnet2_nml2"
        bask_file_name = "../acnet2_nml2/cells/bask.cell.acnet2_nml2"

        exc_exc_syn_names = "../acnet2_nml2/synapses/AMPA_syn.synapse.acnet2_nml2"
        exc_inh_syn_names = "../acnet2_nml2/synapses/AMPA_syn_inh.synapse.acnet2_nml2"
        inh_exc_syn_names = "../acnet2_nml2/synapses/GABA_syn.synapse.acnet2_nml2"
        inh_inh_syn_names = "../acnet2_nml2/synapses/GABA_syn_inh.synapse.acnet2_nml2"
        bg_exc_syn_names = "../acnet2_nml2/synapses/bg_AMPA_syn.synapse.acnet2_nml2"

        nml_doc = NeuroMLDocument(id=self.filename + "_doc")
        net = Network(id=self.filename + "_net")
        nml_doc.networks.append(net)

        nml_doc.includes.append(IncludeType(pyr_file_name))
        nml_doc.includes.append(IncludeType(bask_file_name))
        nml_doc.includes.append(IncludeType(exc_exc_syn_names))
        nml_doc.includes.append(IncludeType(exc_inh_syn_names))
        nml_doc.includes.append(IncludeType(inh_exc_syn_names))
        nml_doc.includes.append(IncludeType(inh_inh_syn_names))
        nml_doc.includes.append(IncludeType(bg_exc_syn_names))

        # Create a LEMSSimulation to manage creation of LEMS file
        ls = LEMSSimulation(self.filename, self.sim_time, self.dt)

        # Point to network as target of simulation
        ls.assign_simulation_target(net.id)

        # The names of the cell type/component used in the Exc & Inh populations
        exc_group_component = "pyr_4_sym"
        inh_group_component = "bask"

        # The names of the Exc & Inh groups/populations
        exc_group = "pyramidals"  # "pyramidals48x48"
        inh_group = "baskets"  # "baskets24x24"

        # The names of the network connections
        net_conn_exc_exc = "pyr_pyr"
        net_conn_exc_inh = "pyr_bask"
        net_conn_inh_exc = "bask_pyr"
        net_conn_inh_inh = "bask_bask"

        # The names of the synapse types
        exc_exc_syn = "AMPA_syn"
        exc_exc_syn_seg_id = 3  # Middle apical dendrite
        exc_inh_syn = "AMPA_syn_inh"
        exc_inh_syn_seg_id = 1  # Dendrite
        inh_exc_syn = "GABA_syn"
        inh_exc_syn_seg_id = 6  # Basal dendrite
        inh_inh_syn = "GABA_syn_inh"
        inh_inh_syn_seg_id = 0  # Soma

        # aff_exc_syn = "AMPA_aff_syn"
        # aff_exc_syn_seg_id = 5  # proximal apical dendrite

        bg_exc_syn = "bg_AMPA_syn"
        bg_exc_syn_seg_id = 7  # Basal dendrite

        # Excitatory Parameters
        XSCALE_ex = 24  # 48
        ZSCALE_ex = 24  # 48
        xSpacing_ex = 40  # 10^-6m
        zSpacing_ex = 40  # 10^-6m

        # Inhibitory Parameters
        XSCALE_inh = 12  # 24
        ZSCALE_inh = 12  # 24
        xSpacing_inh = 80  # 10^-6m
        zSpacing_inh = 80  # 10^-6m

        numCells_ex = XSCALE_ex * ZSCALE_ex
        numCells_inh = XSCALE_inh * ZSCALE_inh

        # Connection probabilities (initial value)
        connection_probability_ex_ex = 0.15
        connection_probability_ex_inh = 0.45
        connection_probability_inh_ex = 0.6
        connection_probability_inh_inh = 0.6

        # Generate excitatory cells

        exc_pop = Population(
            id=exc_group,
            component=exc_group_component,
            type="populationList",
            size=XSCALE_ex * ZSCALE_ex,
        )
        net.populations.append(exc_pop)

        exc_pos = np.zeros((XSCALE_ex * ZSCALE_ex, 2))

        for i in range(0, XSCALE_ex):
            for j in range(0, ZSCALE_ex):
                # create cells
                x = i * xSpacing_ex
                z = j * zSpacing_ex
                index = i * ZSCALE_ex + j

                inst = Instance(id=index)
                exc_pop.instances.append(inst)

                inst.location = Location(x=x, y=0, z=z)

                exc_pos[index, 0] = x
                exc_pos[index, 1] = z

        # Generate inhibitory cells

        inh_pop = Population(
            id=inh_group,
            component=inh_group_component,
            type="populationList",
            size=XSCALE_inh * ZSCALE_inh,
        )
        net.populations.append(inh_pop)

        inh_pos = np.zeros((XSCALE_inh * ZSCALE_inh, 2))

        for i in range(0, XSCALE_inh):
            for j in range(0, ZSCALE_inh):
                # create cells
                x = i * xSpacing_inh
                z = j * zSpacing_inh
                index = i * ZSCALE_inh + j

                inst = Instance(id=index)
                inh_pop.instances.append(inst)

                inst.location = Location(x=x, y=0, z=z)

                inh_pos[index, 0] = x
                inh_pos[index, 1] = z

        proj_exc_exc = Projection(
            id=net_conn_exc_exc,
            presynaptic_population=exc_group,
            postsynaptic_population=exc_group,
            synapse=exc_exc_syn,
        )
        net.projections.append(proj_exc_exc)
        proj_exc_inh = Projection(
            id=net_conn_exc_inh,
            presynaptic_population=exc_group,
            postsynaptic_population=inh_group,
            synapse=exc_inh_syn,
        )
        net.projections.append(proj_exc_inh)
        proj_inh_exc = Projection(
            id=net_conn_inh_exc,
            presynaptic_population=inh_group,
            postsynaptic_population=exc_group,
            synapse=inh_exc_syn,
        )
        net.projections.append(proj_inh_exc)
        proj_inh_inh = Projection(
            id=net_conn_inh_inh,
            presynaptic_population=inh_group,
            postsynaptic_population=inh_group,
            synapse=inh_inh_syn,
        )
        net.projections.append(proj_inh_inh)

        # Generate exc -> *  connections

        exc_exc_conn = np.zeros((numCells_ex, numCells_ex))
        exc_inh_conn = np.zeros((numCells_ex, numCells_inh))

        count_exc_exc = 0
        count_exc_inh = 0
        for i in range(0, XSCALE_ex):
            for j in range(0, ZSCALE_ex):
                x = i * xSpacing_ex
                y = j * zSpacing_ex
                index = i * ZSCALE_ex + j
                # print("Looking at connections for exc cell at (%i, %i)"%(i,j))

                # exc -> exc  connections
                # conn_type = net_conn_exc_exc
                for k in range(0, XSCALE_ex):
                    for l in range(0, ZSCALE_ex):

                        # calculate distance from pre- to post-synaptic neuron
                        xk = k * xSpacing_ex
                        yk = l * zSpacing_ex
                        distance = math.sqrt((x - xk) ** 2 + (y - yk) ** 2)
                        connection_probability = (
                            connection_probability_ex_ex
                            * math.exp(-((distance / (10.0 * xSpacing_ex)) ** 2))
                        )

                        # create a random number between 0 and 1,
                        # if it is <= connection_probability
                        # accept connection otherwise refuse
                        a = random.random()
                        if 0 < a <= connection_probability:
                            index2 = k * ZSCALE_ex + l
                            count_exc_exc += 1

                            add_connection(
                                proj_exc_exc,
                                count_exc_exc,
                                exc_group,
                                exc_group_component,
                                index,
                                0,
                                exc_group,
                                exc_group_component,
                                index2,
                                exc_exc_syn_seg_id,
                            )

                            exc_exc_conn[index, index2] = 1

                # exc -> inh  connections
                # conn_type = net_conn_exc_inh
                for k in range(0, XSCALE_inh):
                    for l in range(0, ZSCALE_inh):

                        # calculate distance from pre- to post-synaptic neuron
                        xk = k * xSpacing_inh
                        yk = l * zSpacing_inh
                        distance = math.sqrt((x - xk) ** 2 + (y - yk) ** 2)
                        connection_probability = (
                            connection_probability_ex_inh
                            * math.exp(-((distance / (10.0 * xSpacing_ex)) ** 2))
                        )

                        # create a random number between 0 and 1,
                        # if it is <= connection_probability
                        # accept connection otherwise refuse
                        a = random.random()
                        if 0 < a <= connection_probability:
                            index2 = k * ZSCALE_inh + l
                            count_exc_inh += 1

                            add_connection(
                                proj_exc_inh,
                                count_exc_inh,
                                exc_group,
                                exc_group_component,
                                index,
                                0,
                                inh_group,
                                inh_group_component,
                                index2,
                                exc_inh_syn_seg_id,
                            )

                            exc_inh_conn[index, index2] = 1

        inh_exc_conn = np.zeros((numCells_inh, numCells_ex))
        inh_inh_conn = np.zeros((numCells_inh, numCells_inh))

        count_inh_exc = 0
        count_inh_inh = 0
        for i in range(0, XSCALE_inh):
            for j in range(0, ZSCALE_inh):

                x = i * xSpacing_inh
                y = j * zSpacing_inh
                index = i * ZSCALE_inh + j
                # print("Looking at connections for inh cell at (%i, %i)"%(i,j))

                # inh -> exc  connections
                # conn_type = net_conn_inh_exc
                for k in range(0, XSCALE_ex):
                    for l in range(0, ZSCALE_ex):

                        # calculate distance from pre- to post-synaptic neuron
                        xk = k * xSpacing_ex
                        yk = l * zSpacing_ex
                        distance = math.sqrt((x - xk) ** 2 + (y - yk) ** 2)
                        connection_probability = (
                            connection_probability_inh_ex
                            * math.exp(-((distance / (10.0 * xSpacing_ex)) ** 2))
                        )

                        # create a random number between 0 and 1,
                        # if it is <= connection_probability
                        # accept connection otherwise refuse
                        a = random.random()
                        if 0 < a <= connection_probability:
                            index2 = k * ZSCALE_ex + l
                            count_inh_exc += 1

                            add_connection(
                                proj_inh_exc,
                                count_inh_exc,
                                inh_group,
                                inh_group_component,
                                index,
                                0,
                                exc_group,
                                exc_group_component,
                                index2,
                                inh_exc_syn_seg_id,
                            )

                            inh_exc_conn[index, index2] = 1

                # inh -> inh  connections
                # conn_type = net_conn_inh_inh
                for k in range(0, XSCALE_inh):
                    for l in range(0, ZSCALE_inh):

                        # calculate distance from pre- to post-synaptic neuron
                        xk = k * xSpacing_inh
                        yk = l * zSpacing_inh
                        distance = math.sqrt((x - xk) ** 2 + (y - yk) ** 2)
                        connection_probability = (
                            connection_probability_inh_inh
                            * math.exp(-((distance / (10.0 * xSpacing_ex)) ** 2))
                        )

                        # create a random number between 0 and 1,
                        # if it is <= connection_probability
                        # accept connection otherwise refuse
                        a = random.random()
                        if 0 < a <= connection_probability:
                            index2 = k * ZSCALE_inh + l
                            count_inh_inh += 1

                            add_connection(
                                proj_inh_inh,
                                count_inh_inh,
                                inh_group,
                                inh_group_component,
                                index,
                                0,
                                inh_group,
                                inh_group_component,
                                index2,
                                inh_inh_syn_seg_id,
                            )

                            inh_inh_conn[index, index2] = 1

        print(
            "Generated network with %i exc_exc, %i exc_inh, %i inh_exc, %i inh_inh connections"
            % (count_exc_exc, count_exc_inh, count_inh_exc, count_inh_inh)
        )

        # Create Input
        # Create a sine generator
        sgE = SineGenerator(
            id="sineGen_0",
            phase="0",
            delay="0ms",
            duration=str(self.sim_time) + "ms",
            amplitude=str(self.Edrive_weight) + "nA",
            period=str(self.Drive_period) + "ms",
        )
        sgI = SineGenerator(
            id="sineGen_1",
            phase="0",
            delay="0ms",
            duration=str(self.sim_time) + "ms",
            amplitude=str(self.Idrive_weight) + "nA",
            period=str(self.Drive_period) + "ms",
        )

        nml_doc.sine_generators.append(sgE)
        nml_doc.sine_generators.append(sgI)
        # Create an input object for each excitatory cell
        for i in range(0, XSCALE_ex):
            exp_input = ExplicitInput(target="%s[%i]" % (exc_pop.id, i), input=sgE.id)
            net.explicit_inputs.append(exp_input)

        # Create an input object for a percentage of inhibitory cells
        input_probability = 0.65
        for i in range(0, XSCALE_inh):
            ran = random.random()
            if 0 < ran <= input_probability:
                inh_input = ExplicitInput(
                    target="%s[%i]" % (inh_pop.id, i), input=sgI.id
                )
                net.explicit_inputs.append(inh_input)

        # Define Poisson noise input

        # Ex

        # nml_doc.includes.append(IncludeType('synapses/bg_AMPA_syn.synapse.acnet2_nml2'))

        pfs1 = PoissonFiringSynapse(
            id="poissonFiringSyn1",
            average_rate=str(self.bg_noise_frequency) + "Hz",
            synapse=bg_exc_syn,
            spike_target="./%s" % bg_exc_syn,
        )
        nml_doc.poisson_firing_synapses.append(pfs1)

        pfs_input_list1 = InputList(
            id="pfsInput1", component=pfs1.id, populations=exc_pop.id
        )
        net.input_lists.append(pfs_input_list1)
        for i in range(0, numCells_ex):
            pfs_input_list1.input.append(
                Input(
                    id=i,
                    target="../%s/%i/%s" % (exc_pop.id, i, exc_group_component),
                    segment_id=bg_exc_syn_seg_id,
                    destination="synapses",
                )
            )

        # Write to file
        print("Saving to file...")
        nml_file = "../acnet2_nml2/" + self.filename + "_doc" + ".net.acnet2_nml2"
        writers.NeuroMLWriter.write(nml_doc, nml_file)

        print("Written network file to: " + nml_file)

        # Validate the NeuroML

        validate_neuroml2(nml_file)
        print("-----------------------------------")

        # Output

        # Output membrane potential
        # Ex population
        Ex_potentials = "V_Ex"
        ls.create_output_file(Ex_potentials, "../acnet2_nml2/results/v_exc.dat")
        for j in range(numCells_ex):
            quantity = "%s[%i]/v" % (exc_pop.id, j)
            v = "v" + str(j)
            ls.add_column_to_output_file(Ex_potentials, v, quantity)

        # Inh population
        # Inh_potentials = 'V_Inh'
        # ls.create_output_file(Inh_potentials, "../acnet2_nml2/results/v_inh.dat")
        # for j in range(numCells_inh):
        # 	quantity = "%s[%i]/v"%(inh_pop.id, j)
        # 	v = 'v'+str(j)
        # 	ls.add_column_to_output_file(Inh_potentials,v, quantity)

        # include generated network
        ls.include_neuroml2_file(nml_file)

        # Save to LEMS XML file
        # lems_file_name = ls.save_to_file(
        #     file_name="../acnet2_nml2/LEMS_" + self.filename + ".xml"
        # )

    def singleRun(self):
        nml_file = os.path.join(DATA_PATH, "acnet2_nml2", self.filename, "_doc.net.acnet2_nml2")
        lems_file = os.path.join(DATA_PATH, "acnet2_nml2", "LEMS_", self.filename, ".xml")

        target = self.filename + "_net"
        simulator = "jNeuroML_NEURON"
        generate_dir = os.path.join(DATA_PATH, "acnet2_nml2")

        sim_vars = {}
        # set up Controller
        cont = Controller(
            self.filename,
            nml_file,
            lems_file,
            target,
            self.sim_time,
            self.dt,
            simulator,
            generate_dir=generate_dir,
        )

        cont.run_individual(sim_vars, show=False)
        print("\n\n\n")
        print("Have run individual instance...")
        print("\n\n\n")

    def analyse(self, powerfrequency):
        data = np.genfromtxt("../acnet2_nml2/results/v_exc.dat", dtype=np.float)

        avg_data = np.mean(data, axis=1)

        nfft = len(avg_data)
        fs = 1.0 / self.dt
        pxx, freqs = mlab.psd(
            avg_data, NFFT=nfft, Fs=fs, noverlap=0, window=mlab.window_none
        )
        pxx[0] = 0.0
        freqs = freqs * 1000  # adjusting for ms timescale
        step_size = freqs[1] - freqs[0]
        lbound = np.floor(powerfrequency / step_size)
        ubound = np.ceil(powerfrequency / step_size)

        power = np.sum(pxx[lbound:ubound])

        return power


class BeemanNML2Model(sciunit.Model, ProduceXY):
    """NeuroML2 of the auditory cortex model from Beeman (2013)"""

    def __init__(self, controlparams, schizparams):
        """
        Constructor method. Both parameter sets, for the control and the schizophrenia-like
        network, have to be a dictionary containing the following parmaeters
        (Filename,Stimulation Frequency,Random Seed,E-E Weight,I-E Weight,E-I Weight,I-I Weight,
        Background Noise Weight,E-Drive Weight,I-Drive
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
        Simulates Y Hz drive to the control and the schizophrenia-like network for all
        random seeds, calculates a Fourier transform of the simulated MEG
        and extracts the power in the X Hz frequency band for each simulation.
        Returns the mean power for the control and the schizophrenia-like network, respectively.
        """
        drive_period = (
            1.0 / stimfrequency
        ) * 1000  # calculate drive period (in ms) from stimulation frequency
        # generate the control network and run simulation
        print("Generating control model")
        ctrl_model = NML2Model(self.controlparams, drive_period)
        ctrl_model.createModel()
        print("Running control model")
        ctrl_model.singleRun()
        print("Analysing control model")
        controlXY = ctrl_model.analyse(powerfrequency)

        # generate the schizophrenia-like network and run simulation
        print("Generating schizophrenia model")
        schiz_model = BeemanNML2Model(self.schizparams, drive_period)
        schiz_model.createModel()
        print("Running control model")
        schiz_model.singleRun()
        print("Analysing control model")
        schizXY = schiz_model.analyse(powerfrequency)

        return [controlXY, schizXY]
