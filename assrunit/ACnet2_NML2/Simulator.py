"""

 A class for running a single instance of a NeuroML model and its  
 LEMS file by using pyNeuroML to run in a chosen simulator

 @author: Christoph Metzner

 builds on NeuroMLSimulation from the PyNeuroML package
    
"""

import sys
import time

from pyneuroml import pynml


class Simulation(object):
    def __init__(
        self,
        reference,
        neuroml_file,
        lems_file,
        target,
        sim_time=1000,
        dt=0.05,
        simulator="jNeuroML_NEURON",
        generate_dir="./",
    ):

        self.sim_time = sim_time
        self.dt = dt
        self.simulator = simulator
        self.generate_dir = (
            generate_dir if generate_dir.endswith("/") else generate_dir + "/"
        )

        self.reference = reference
        self.target = target
        self.neuroml_file = neuroml_file
        self.lems_file = lems_file

        self.already_run = False

    def go(self):

        pynml.print_comment_v(
            "Running a simulation of %s ms with timestep %s ms: %s"
            % (self.sim_time, self.dt, self.lems_file)
        )

        self.already_run = True

        print self.simulator

        start = time.time()
        if self.simulator == "jNeuroML":
            results = pynml.run_lems_with_jneuroml(
                self.lems_file,  # _name,
                nogui=True,
                load_saved_data=True,
                plot=False,
                exec_in_dir=self.generate_dir,
                verbose=False,
            )
        elif self.simulator == "jNeuroML_NEURON":
            results = pynml.run_lems_with_jneuroml_neuron(
                self.lems_file,
                nogui=True,
                load_saved_data=False,
                plot=False,
                exec_in_dir=self.generate_dir,
                verbose=False,
            )
        else:
            pynml.print_comment_v("Unsupported simulator: %s" % self.simulator)
            exit()

        secs = time.time() - start

        pynml.print_comment_v(
            "Ran simulation in %s in %f seconds (%f mins)\n\n"
            % (self.simulator, secs, secs / 60.0)
        )
