//genesis

/**********************************************************************
** This simulation script and the files included in this package
** are Copyright (C) 2013 by David Beeman (dbeeman@colorado.edu)
** and are made available under the terms of the
** GNU Lesser General Public License version 2.1
** See the file copying.txt for the full notice.
*********************************************************************/

/*======================================================================

  Version 2.5 of a 'simple yet realistic' model of primary auditory layer
  4, described in:

  Beeman D (2013) A modeling study of cortical waves in primary auditory
  cortex. BMC Neuroscience, 14(Suppl 1):P23 doi:10.1186/1471-2202-14-S1-P23
  (http://www.biomedcentral.com/1471-2202/14/S1/P23)

  This model is based on the earlier simple cortical model
  dualexpVA-HHnet.g:

  The GENESIS implementation of the dual exponential conductance version of
  the Vogels-Abbott (J. Neurosci. 25: 10786--10795 (2005)) network model
  with Hodgkin-Huxley neurons.  Details are given in Brett et al. (2007)
  Simulation of networks of spiking neurons: A review of tools and
  strategies.  J. Comput. Neurosci. 23: 349-398.
  http://senselab.med.yale.edu/SenseLab/ModelDB/ShowModel.asp?model=83319

  A network of simplified Regular Spiking neocortical neurons providing
  excitatory connections and Fast Spiking interneurons providing inhibitory
  connections.  Further description is given with the RSnet.g example from
  the GENESIS Neural Modeling Tutorials
  (http://genesis-sim.org/GENESIS/UGTD/Tutorials/)

  New version adapted to auditory click train stimulations! (Christoph Metzner 20/1/15)
  ======================================================================*/


str script_name = "ACnet2-batch-new-standard"
str RUNID = {argv {1}}         // default ID string for output file names


int hsolve_chanmode = 4  // chanmode to use 

float tmax = 10.0      	  // max simulation run time (sec) 
float dt = 20e-6	  // simulation time step
float out_dt = 0.0001     // output every 0.1 msec
float netview_dt = 0.0002 // slowest clock for netview display

float ct_frequency = {argv {2}} //set_ct_frequency_marker



/****** the seed is set here *****/
int seed = {argv {3}} //1369497795   //set_seed_marker

setrand -sprng

randseed {seed}


/* Cell files */
str Ex_cellfile = "pyr_4_asym_AIS.p"  // name of the excitatory cell parameter file
str Inh_cellfile = "bask.p"  // name of the inhibitory cell parameter file
str protodefs_file = "protodefs.g" // file that creates prototypes in /library

/* Names */
str Ex_cell_name = "pyr"   // name of the excitatory cell
str Inh_cell_name = "bask" // name of the inhibitory cell



// Paths to synapses on cells: cell_synapse = compartment-name/synchan-name
// e.g. Ex_inh_synpath is path to inhibitory synapse on excitatory cell
str Ex_ex_synpath = "apical3/AMPA_pyr" // pyr middle apical dendrite AMPA
str Ex_inh_synpath = "basal0/GABA_pyr" // pyr prox basal GABA
str Inh_ex_synpath = "dend/AMPA_bask"  // bask dend AMPA
str Inh_inh_synpath = "soma/GABA_bask" // bask soma GABA
str Ex_bg_synpath = "basal1/AMPA_pyr"  // synchan for background input


// Excitatory drive inputs - path to synapse on Ex and Inh cells to apply drive
str Ex_drive_synpath = "apical1/AMPA_pyr" // drive -> pyr prox oblique apical
str Inh_drive_synpath = "dend/AMPA_bask_drive"  // drive -> bask dendrite




// Label to appear on the graph
str graphlabel = "Vm of row center cell"
str net_efile = "Results/Ex_netview"  // filename prefix for Ex_netview data
str net_ifile = "Results/Inh_netview" // filename prefix for Inh_netview data
str net_EPSC_file = "Results/EPSC_netview" // filename prefix for Ex_ex_synpath Ik (EPSCs)
str EPSC_sum_file = "Results/EPSC_sum" // filename prefix for summed Ex_ex_synpath Ik
str sum_file = "Results/run_summary"    // text file prefix for summary of run params

str data_source = "/EPSCsummer" // data_source sums Ex_cell ex currents

int Ex_NX = 24; int Ex_NY = 24
int Inh_NX = 12; int Inh_NY = 12

int Ninputs = Ex_NY


// Cell spacing
float Ex_SEP_X = 40e-6
float Ex_SEP_Y = 40e-6 
float Inh_SEP_X = 2*Ex_SEP_X  // There are 1/4 as many inihibitory neurons
float Inh_SEP_Y = 2*Ex_SEP_Y 

/* "SEP_Z" should be set to the actual layer thickness, in order to allow
   possible random displacements of cells from the 2-D lattice.  Here, it
   needs to be large enough that any connections to distal dendrites will
   be within the range -SEP_Z to SEP_Z.
*/

float Ex_SEP_Z = 1.0
float Inh_SEP_Z = Ex_SEP_Z





float drive_weight = 1.0 // Default weight of all input drive connections

float input_delay, input_jitter // used in simple-inputs.g or MGBv_input.g
float input_delay = 0.0
float input_jitter = 0.0

// float spike_jitter = 0.0005 // 0.5 msec jitter in thalamic inputs
float spike_jitter = 0.0  //default is no jitter in arrival time


/* parameters for synaptic connections */

float syn_weight = 1.0 // synaptic weight, effectively multiplies gmax


float prop_delay = 0.0 //12.5 //  delay per meter, or 1/cond_vel

float Ex_ex_gmax = {argv {4}} //30e-9   // Ex_cell ex synapse
float Ex_inh_gmax = {argv {5}} //0.6e-9  // Ex_cell inh synapse //set_gmax_Ex_inh_marker
float Inh_ex_gmax = {argv {6}} //0.10e-9 //0.15e-9 // Inh_cell ex synapse (Use 0.10e-9, because otherwise Inh cells fire at 80Hz instead of 40Hz for 40Hz drive!)
float Inh_inh_gmax = {argv {7}} //0.15e-9 //0.15e-9 //Inh_cell inh synapse //set_gmax_Inh_inh_marker
float Ex_bg_gmax = {argv {8}} //80e-9  // Ex_cell background excitation



float Ex_drive_gmax = {argv {9}} //50e-9 // Ex_cell thalamic input
float Inh_drive_gmax = {argv {10}} //1.5e-9 // Inh_cell thalamic input


// Poisson distributed random excitation frequency of Ex_cells
// NOTE: For use with hsolve, the synchan frequency must be set to a non-zero
// value before the solver setup.  Then it may be set to any value, including zero.

float frequency = {argv {11}} //8.0
echo {frequency}

// time constants for dual exponential synaptic conductance

float tau1_ex = 0.001     // rise time for excitatory synapses
float tau2_ex =  0.003    // decay time for excitatory synapses
float Inh_tau1_ex = 0.003 // make a special case for Inh cell excitatory channels
float Inh_tau2_ex = 0.003
float tau1_inh = 0.001    // rise time for inhibitory synapses  
float tau2_inh =  0.006  // decay time for inhibitory synapses  //set_tau2_Inh_inh_marker
float Ex_tau1_inh = 0.001    // rise time for inhibitory synapses
float Ex_tau2_inh =  0.006  // decay time for inhibitory synapses  //set_tau2_Ex_inh_marker


/* Give a range of tau2_inh from tau2_inh*(1-tau2_inh_spreadfactor)
   to tau2_inh*(1+tau2_inh_spreadfactor) - set to zero for a single value
   Set to 0.6 for a range of 8 +/- 4.8 msec, or 25 +/- 15 msec
*/

float tau2_inh_spreadfactor = 0.6

/* Input parameters */
str input_source = "/MGBv" // Name of the array of input elements


// Pulsed spike generator -- for constant input, use pulsewidth >= tmax
float pulse_width =  100.0    // width of pulse (100 >= tmax => constant input!)
float pulse_delay = 0.05        // delay before start of pulse
float pulse_interval = 0.15 // time from start of pulse to next (period)




// Connectivity reduction factors
float Ex_ex_red = 1.0 //set_Ex_ex_red_marker
float Ex_inh_red = 1.0 //set_Ex_inh_red_marker
float Inh_ex_red = 1.0 //set_Inh_ex_red_marker
float Inh_inh_red = 1.0 //set_Inh_inh_red_marker

//===============================
//    Main simulation section
//===============================

setclock  0  {dt}		// set the simulation clock

/* Including the protodefs file creates prototypes of the channels,
   and other cellular components under the neutral element '/library'.
   Calling the function 'make_prototypes', defined earlier in this
   script, uses these and the cell reader to add the cells.
*/
include protodefs.g
include functions_standard.g // contains all functions to setup the network and its connections
// Now /library contains prototype channels, compartments, spikegen

make_prototypes // This adds the prototype cells to /library

make_network // Copy cells into network layers





// make_network should do some of this, but set all synchan gmax values
set_all_gmax

/* synchan tau values should not be changed after hsolve SETUP */
// Change the synchan tau1 and tau2 from the values used in protodefs
set_all_taus

set_inh_tau2 {tau2_inh}

// set the random background excitation frequency
set_frequency {frequency}


/* Setting up hsolve for a network requires setting up a solver for
   one cell of each type in the network and then duplicating the
   solvers.  The procedure is described in the advanced tutorial
   'Simulations with GENESIS using hsolve by Hugo Cornelis' from
   genesis-sim.org/GENESIS/UGTD/Tutorials/advanced-tutorials
*/

pushe /Ex_layer/pyr[0]
create hsolve solver
setmethod . 11 // Use Crank-Nicholson
setfield solver chanmode {hsolve_chanmode} path "../[][TYPE=compartment]"
call solver SETUP
int i
for (i = 1 ; i < {Ex_NX*Ex_NY} ; i = i + 1)
        call solver DUPLICATE \
            /Ex_layer/pyr[{i}]/solver  ../##[][TYPE=compartment]
        setfield /Ex_layer/pyr[{i}]/solver \
            x {getfield /Ex_layer/pyr[{i}]/soma x} \
            y {getfield /Ex_layer/pyr[{i}]/soma y} \
            z {getfield /Ex_layer/pyr[{i}]/soma z}
end
pope
pushe /Inh_layer/bask[0]
create hsolve solver
setmethod . 11 // see if this works
setfield solver chanmode  {hsolve_chanmode} path "../[][TYPE=compartment]"
call solver SETUP
int i
for (i = 1 ; i < {Inh_NX*Inh_NY} ; i = i + 1)
  	call solver DUPLICATE \
            /Inh_layer/bask[{i}]/solver	 ../##[][TYPE=compartment]
    setfield /Inh_layer/bask[{i}]/solver \
        x {getfield /Inh_layer/bask[{i}]/soma x} \
        y {getfield /Inh_layer/bask[{i}]/soma y} \
        z {getfield /Inh_layer/bask[{i}]/soma z}
end
pope

// Now connect them
echo "Starting connection set up: " {getdate}
connect_cells {Ex_ex_red} {Ex_inh_red} {Inh_ex_red} {Inh_inh_red} // connect up the cells in the network layers
echo "Finished connection set up: " {getdate}

// set weights and delays
set_weights {syn_weight}

/* If the delay is zero, set it as the fixed delay, else use the conduction
  velocity and calculate delays based on radial distance to target
*/
if (prop_delay == 0.0)
    planardelay /Ex_layer/{Ex_cell_name}[]/axon/spike -fixed {prop_delay}
    planardelay /Inh_layer/{Inh_cell_name}[]/soma/spike -fixed {prop_delay}
else
    planardelay /Ex_layer/{Ex_cell_name}[]/axon/spike -radial {1/prop_delay}
    planardelay /Inh_layer/{Inh_cell_name}[]/soma/spike -radial {1/prop_delay}
end


/* Set up the inputs to the network.  Depending on
   the type of input to be used, include the appropriate
   file for defining the functions make_inputs and connect_inputs
*/

echo "Using simple pulsed spiketrain input"

include basic_inputs_click_train_I_drive.g


make_input_click_train_all 220// Create array of network inputs 
connect_inputs // Connect the inputs to the network
setall_driveweights {drive_weight} // Initialize the weights of input drive

// Create disk_out elements /output/{net_efile}, {net_ifile}, {net_EPSC_file}
//do_network_out
// if (calc_EPSCsum), set up the calculator, messages, and file for summed EPSCs
do_EPSCsum_out



//do_AMPAExnoisesum_out


echo "Network of "{Ex_NX} " by " {Ex_NY}" excitatory cells "
echo "Network of "{Inh_NX} " by " {Inh_NY}" inhibitory cells "
echo "Random number generator seed initialized to: " {seed}

print_avg_syn_number 


set_frequency {frequency}
int i 	
for (i=1; i <= {Ninputs}; i=i+1)
    	setfield /MGBv[{i}]/spikepulse level1 1.0 
    	setfield /MGBv[{i}]/spikepulse/spike abs_refract {1.0/{ct_frequency}}  
end	
reset
reset
step_tmax 
exit


