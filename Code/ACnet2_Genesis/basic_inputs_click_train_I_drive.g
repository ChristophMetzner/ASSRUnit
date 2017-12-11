//===============================
//      Function Definitions
//===============================


/* Functions to create the MGBv cells that will provide the inputs 
   In this case the "cells" are spikegens controlled by pulsegens
*/

function make_MGBvcell(path)
    str path
    // The full MGBvcell model would have  MGBvcell parameters here

    // Pulsed spike generator -- for constant input, use pulsewidth >= tmax
    // these will get changed
    float pulse_width = {tmax}     // width of pulse
    float pulse_delay = 0          // delay before start of pulse
    float pulse_interval = {tmax}  // interval before next pulse
    float spikefreq = 110 // Hz.   // initial value of frequency

    // This parameter is used for the full MGBvcell model
    // float spike_weight = 8

    /* Create the basic cell as a container for the pulsegen and spikegen */
    create neutral {path}
    // add fields to keep the target row, frequency and weight
    addfield {path} input_row
    setfield {path} input_row 0 // just to initialize it
    addfield {path} dest_row
    setfield {path} dest_row 0 // just to initialize it
    addfield {path} input_freq
    setfield {path} input_freq {spikefreq}
    addfield {path} output_weight
    setfield {path} output_weight 1.0

    create pulsegen {path}/spikepulse // Make a periodic pulse to control spikes

        // create a spikegen with a refractory period = 1/freq
        create spikegen {path}/spikepulse/spike
        setfield {path}/spikepulse/spike thresh 0.5
        setfield {path}/spikepulse width1 {pulse_width} delay1 {pulse_delay}  \
          baselevel 0.0 trig_mode 0 delay2 {pulse_interval - pulse_delay} width2 0
        setfield {path}/spikepulse/spike abs_refract {1.0/spikefreq}
        addmsg {path}/spikepulse {path}/spikepulse/spike INPUT output
end // function make_MGBvcell


function set_input_freq(cell, input_freq)
    str cell; float freq, input_freq
    setfield {cell} input_freq {input_freq}
    freq = input_freq
    if ({input_freq} > 1000)
        freq = 1000
    end
    float abs_refract = 1e6 // A very low frequency
    if ({freq} > 1.0e-6)
       abs_refract = 1.0/freq
    end
        setfield {cell}/spikepulse/spike abs_refract {abs_refract}
end // set_input_freq(cell, freq)

// Set parameters for spike train pulses
function set_pulse_params(input_num, frequency, delay, width, interval)
    int input_num
    float frequency, delay, width, interval, abs_refract
    setfield {input_source}[{input_num}]/spikepulse width1 {width} delay1 \
        {delay} baselevel 0.0 trig_mode 0 delay2 {interval - delay} width2 0
    // free run mode with very long delay for 2nd pulse (non-repetitive)
    // level1 is set by GUI spiketoggle function, or by a batch mode command
    // set the abs_refract of the spikegen to spike every 1/frequency
    set_input_freq {input_source}[{input_num}] {frequency}
end

function set_spiketrain_weight(input_num, weight)
    int input_num
    float weight
    setfield {input_source}[{input_num}] output_weight {weight}
    // Now set the weights of all network cell targets (not Inh feedback)
    // The optional 2nd arg for target is useful here
    planarweight {input_source}[{input_num}]/spikepulse/spike  \
        /Ex_layer/{Ex_cell_name}[]/{Ex_drive_synpath} -fixed {weight}
    planarweight {input_source}[{input_num}]/spikepulse/spike  \
        /Inh_layer/{Inh_cell_name}[]/{Inh_drive_synpath} -fixed {weight}
end

function setall_driveweights(weight)
    int i
    float weight
    for (i=1; i <= {Ninputs}; i=i+1)
        set_spiketrain_weight {i} {weight}
    end
end

/* Set up the circuitry to provide spike trains to the network */
function make_input_src_dest(input_num, dest_row)
    int input_num, dest_row
    float x0, y0, z0
    // Set the separations of the vertical array of inputs to that of network
    x0 = 0; y0 = dest_row*Ex_SEP_Y; z0 = 0;
    make_MGBvcell {input_source}[{input_num}]
    setfield {input_source}[{input_num}] x {x0} y {y0} z {z0}
    setfield {input_source}[{input_num}] dest_row {dest_row}
end // function make_input_src_dest

/* make_inputs and connect_inputs are the two functions called by ACnet2
   to set up the inputs to the network
*/



function make_input_click_train_all(f0)
    // Special case for ACnet2 click train inputs - Ninputs = Ex_NY
    int first_row = 1
    int row_sep = 1 //
    int i
    float f0, freq
    f0 = 220.0
    if ({argc} == 1)
        f0 = {argv 1}
    end

    for (i=1; i <= {Ninputs}; i=i+1)
        // This assignment can be changed as needed
        freq = f0*i
        make_input_src_dest {i} {first_row + (i-1)*row_sep}
        set_pulse_params {i} {freq} {pulse_delay} {pulse_width} {pulse_interval}
    end
end // function make_inputs

function connect_inputs
    /* For input_pattern = "row", connections will be made to all
       cells on the specified row.  If input_spread > 0, connections
       with an exponentially decay probablility will be made to
       adjacent rows +/- input_spread.

       For special cases "line" or "box", I want connections from the one
       input channel to go to all cells in a rectangular block defined by
       (Ex_NX0_in, Ex_NY0_in, Ex_NXlen_in, Ex_NYlen_in)

       Note that the Inh cells are displaced from Ex by Ex_SEP_X/2,
       Ex_SEP_Y/2, with twice the spacing.

       The x coord of the Ex_cell apical1 compartment (Ex_drive_synpath)
       is displaced from the grid location by -125 um, as it is at the end
       of the oblique apical dendrite.  For the symmetric compartment version
       of the cell, it is at -75 um.

       For "row" input, all cells on the row will be targets, so
       apical1_x_offset is not needed.

       Also, note the that '-relative' option is not used here.

 */
    float apical1_x_offset = -125e-6
    float xmin, ymin, xmax, ymax


      /* Use code from MGBv_input2-5.g to provide input_spread */
      int i
      float target_y, y, ymin, ymax, prob
      // number of rows below and above "target row" of input spread
      /*  Target rows are numbered 1 through Ninputs, and cell rows are
          numbered 0 through Ex_NY - 1.  The first and last one-third
	  octave of the cell rows do not receive MGBv input, so the cell
	  row number is offset from the input row by input_offset.

          In addition, the y coord of the Ex_cell apical1 compartment
	  (Ex_drive_synpath) is displaced from the grid location by 17 um
	  for the symmetric compartment version of the cell, but not for
	  the asymmetric.

	  basic_inputs.g does not use input_offset, nor have a general
	  mapping between input number, frequency and pulse parameters, and
	  the destination row.
      */
      float apical1_offset = 0.0
      prob = 1.0 

      for (i=1; i <= {Ninputs}; i=i+1) // loop over inputs
        target_y = {getfield {input_source}[{i}] dest_row} * Ex_SEP_Y
        // Now set the input_row number for the source to target_y
        setfield {input_source}[{i}] input_row {i}
        // There will be no spread of inputs above or below target row
          y = target_y
          ymin = target_y - 0.2*Ex_SEP_Y
          ymax = target_y + 0.2*Ex_SEP_Y
          planarconnect {input_source}[{i}]/spikepulse/spike \
            /Ex_layer/{Ex_cell_name}[]/{Ex_drive_synpath} \
            -sourcemask box -1 -1 1 1 \
            -destmask box -1 {ymin + apical1_offset} 1 {ymax + apical1_offset} \
            -probability {prob}

          planarconnect {input_source}[{i}]/spikepulse/spike \
            /Inh_layer/{Inh_cell_name}[]/{Inh_drive_synpath} \
            -sourcemask box -1 -1 1 1 \ // be sure that I include the source
            -destmask box -1 {ymin } 1 {ymax} \
            -probability {0.65*{prob}} // {0.65*prob}
      end // for i
end // function connect_inputs
