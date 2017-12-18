'''

 Class that controls a single simulation

 @author: Christoph Metzner

 builds on NeuroMLController from the PyNeuroML package
    
'''

import os.path
import sys
import shutil

from collections import OrderedDict
from pyneuroml.pynml import read_neuroml2_file, write_neuroml2_file, print_comment_v
from pyneuroml.pynml import read_lems_file,write_lems_file

from Simulator import Simulation

class Controller():

    def __init__(self, 
                 ref,  
                 neuroml_file,
		 lems_file, 
                 target, 
                 sim_time=1000, 
                 dt=0.05, 
                 simulator='jNeuroML_NEURON', 
                 generate_dir = './'):
        

        self.ref = ref
        self.neuroml_file = neuroml_file
	self.lems_file = lems_file
        self.target = target
        self.sim_time = sim_time
        self.dt = dt
        self.simulator = simulator
        self.generate_dir = generate_dir if generate_dir.endswith('/') else generate_dir+'/'
        
        self.count = 0


    def run_individual(self, sim_var, show=False):
        """
        Run an individual simulation.

        The candidate data has been flattened into the sim_var dict. The
        sim_var dict contains parameter:value key value pairs, which are
        applied to the model before it is simulated.

        """
        
        nml_doc = read_neuroml2_file(self.neuroml_file, 
                                     include_includes=True,
                                     verbose = True,
                                     already_included = [])

        
                             
        for var_name in sim_var.keys():
            words = var_name.split('/')
            type, id1 = words[0].split(':')
            if ':' in words[1]:
                variable, id2 = words[1].split(':')
            else:
                variable = words[1]
                id2 = None
            
            units = words[2]
            value = sim_var[var_name]
            
            print_comment_v('  Changing value of %s (%s) in %s (%s) to: %s %s'%(variable, id2, type, id1, value, units))
            
            if type == 'cell':
                cell = None
                for c in nml_doc.cells:
                    if c.id == id1:
                        cell = c
                        
                if variable == 'channelDensity':
                    
                    chanDens = None
                    for cd in cell.biophysical_properties.membrane_properties.channel_densities:
                        if cd.id == id2:
                            chanDens = cd
                            
                    chanDens.cond_density = '%s %s'%(value, units)
                    
                elif variable == 'erev_id': # change all values of erev in channelDensity elements with only this id
                    
                    chanDens = None
                    for cd in cell.biophysical_properties.membrane_properties.channel_densities:
                        if cd.id == id2:
                            chanDens = cd
                            
                    chanDens.erev = '%s %s'%(value, units)
                    
                elif variable == 'erev_ion': # change all values of erev in channelDensity elements with this ion
                    
                    chanDens = None
                    for cd in cell.biophysical_properties.membrane_properties.channel_densities:
                        if cd.ion == id2:
                            chanDens = cd
                            
                    chanDens.erev = '%s %s'%(value, units)
                    
                elif variable == 'specificCapacitance': 
                    
                    specCap = None
                    for sc in cell.biophysical_properties.membrane_properties.specific_capacitances:
                        if (sc.segment_groups == None and id2 == 'all') or sc.segment_groups == id2 :
                            specCap = sc
                            
                    specCap.value = '%s %s'%(value, units)
                    
                else:
                    print_comment_v('Unknown variable (%s) in variable expression: %s'%(variable, var_name))
                    exit()
                
            elif type == 'izhikevich2007Cell':
                izhcell = None
                for c in nml_doc.izhikevich2007_cells:
                    if c.id == id1:
                        izhcell = c
                        
                izhcell.__setattr__(variable, '%s %s'%(value, units))
            elif type == 'pulseGenerator':
		pg = None
                for p in nml_doc.pulse_generators:
                    if p.id == id1:
                        pg = p
		if variable == 'amplitude':	
			pg.amplitude = 	'%s %s'%(value, units)
            elif type == 'synapse':
		print '\n\n\n yes \n\n\n'
		syn = None
                for s in nml_doc.exp_two_synapses:
			#print '\n\n\n'+str(s.id)+'\n\n\n'
			#print '\n\n\n id1:'+id1+'\n\n\n'
                    	if s.id == id1:
                        	syn = s
		if variable == 'gbase':	
			#print '\n\n\n'+str(syn.gbase)+'\n\n\n'
			syn.gbase = 	'%s %s'%(value, units)
			#print '\n\n\n'+str(syn.gbase)+'\n\n\n'
            elif type == 'NMDAsynapse':
		print '\n\n\n yes \n\n\n'
		syn = None
                for s in nml_doc.blocking_plastic_synapses:
			#print '\n\n\n'+str(s.id)+'\n\n\n'
			#print '\n\n\n id1:'+id1+'\n\n\n'
                    	if s.id == id1:
                        	syn = s
		if variable == 'gbase':	
			#print '\n\n\n'+str(syn.gbase)+'\n\n\n'
			syn.gbase = 	'%s %s'%(value, units)
			#print '\n\n\n'+str(syn.gbase)+'\n\n\n'
            else:
                print_comment_v('Unknown type (%s) in variable expression: %s'%(type, var_name))
       
                            
                                     
        #new_neuroml_file =  '%s/%s'%(self.generate_dir,os.path.basename(self.neuroml_file))
	new_lems_file    =  '%s/%s'%(self.generate_dir,os.path.basename(self.lems_file))
        #if new_neuroml_file == self.neuroml_file:
        #    print_comment_v('Cannot use a directory for generating into (%s) which is the same location of the NeuroML file (%s)!'% \
        #              (self.neuroml_file, self.generate_dir))
                      
        #write_neuroml2_file(nml_doc, new_neuroml_file)

	# copy LEMS file
        #shutil.copy(self.lems_file,new_lems_file) # that doesn't work, because the paths for the included files are wrong
    
            
        sim = Simulation(self.ref, 
                             neuroml_file = self.neuroml_file,
			     lems_file = self.lems_file,
                             target = self.target,
                             sim_time = self.sim_time, 
                             dt = self.dt, 
                             simulator = self.simulator, 
                             generate_dir = self.generate_dir)
        
        sim.go()
