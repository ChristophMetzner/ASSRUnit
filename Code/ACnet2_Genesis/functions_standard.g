// =============================
//   Function definitions
// =============================

function set_inh_tau2(tau2)
    float tau2, tau2_min, tau2_max
    tau2_inh = tau2
    if (tau2_inh_spreadfactor != 0.0)
        tau2_min = tau2*(1-tau2_inh_spreadfactor)
        tau2_max = tau2*(1+tau2_inh_spreadfactor)
        setrandfield /Ex_layer/{Ex_cell_name}[]/{Ex_inh_synpath} \
            tau2 -uniform {tau2_min} {tau2_max}
        setrandfield /Inh_layer/{Inh_cell_name}[]/{Inh_inh_synpath} \
            tau2 -uniform {tau2_min} {tau2_max}
    else
        setfield /Ex_layer/{Ex_cell_name}[]/{Ex_inh_synpath} tau2 {tau2}
        setfield /Inh_layer/{Inh_cell_name}[]/{Inh_inh_synpath} tau2 {tau2}
    end 
end


/***** functions to connect network *****/ 

/* This is a specialized version of planarconnect where the connection
   probability is weighted with a probability prob0*exp(-r*r/(sigma*sigma))
   where r is the radial distance between source and destination
   in the x-y plane.

   Unlike the more general version, it is assumed that all cells in the
   source network are used as sources.  The destination region is defined
   as a ring between a radius rmin and rmax in the destination network.
   The sources are all assumed to be spikegen objects, and the destinations
   to be synchans, or variants such as facsynchans.
   
   An example of the ith cell in the source network would be:

   {src_cell_path}[{i}]{src_spikepath}

   with

   src_cell_path = /Ex_layer/{Ex_cell_name}
   src_spikepath = "axon/spike"

   An example destination would use:

   dst_cell_path = /Inh_layer/{Inh_cell_name}
   dst_synpath = {Inh_ex_synpath}

   For example:

   planarconnect_probdecay /Ex_layer/{Ex_cell_name} "axon/spike" {Ex_NX*Ex_NY} \
      /Inh_layer/{Inh_cell_name} {Inh_ex_synpath} {Inh_NX*Inh_NY} \
      0.0 {pyr_range} {Ex2Inh_prob} {Ex_sigma}

*/

function set_frequency(value) // set Ex_ex average random firing freq
    float value
    frequency = value
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_bg_synpath} frequency {frequency}
end


function planarconnect_probdecay(src_cell_path, src_spikepath, n_src, \
    dst_cell_path, dst_synpath, n_dst, \
    rmin, rmax, prob0, sigma)

    str src, src_cell_path, src_spikepath, dst, dst_cell_path, dst_synpath

    int n_src, n_dst, i, j
    float rmin, rmax, prob0, sigma, x, y, dst_x, dst_y, prob, rsqr

    float decay = 1.0/(sigma*sigma)
    float rminsqr = rmin*rmin
    float rmaxsqr = rmax*rmax

    /* loop over all source cells - this will be all cells in layer */
    for (i = 0 ; i < {n_src} ; i = i + 1)

       src = {src_cell_path} @ "[" @ {i} @ "]/" @ {src_spikepath}
       x = {getfield {src} x}
       y = {getfield {src} y}

        /* loop over all possible destination cells - all in dest layer */
        for (j = 0 ; j < {n_dst} ; j = j + 1)
            dst = {dst_cell_path} @ "[" @ {j} @ "]/" @ {dst_synpath}
            dst_x = {getfield {dst} x}
            dst_y = {getfield {dst} y}

            rsqr = (dst_x - x)*(dst_x - x) + (dst_y - y)*(dst_y - y)
            if( ({rsqr} >= {rminsqr}) && ({rsqr} <= {rmaxsqr}) )
                prob = {prob0}*{exp {-1.0*{rsqr*decay}}}
                if ({rand 0 1} <= prob)
                  addmsg {src} {dst} SPIKE
                end
            end
        end // dst loop
    end // src loop
end

/**** functions to output results ****/

function make_output(rootname) // asc_file to {rootname}_{RUNID}.txt
    str rootname, filename
    if ({exists {rootname}})
        call {rootname} RESET // this closes and reopens the file
        delete {rootname}
    end
    filename = {rootname} @ "_" @ {RUNID} @ ".txt"
    create asc_file {rootname}
    setfield ^    flush 1    leave_open 1 filename {filename}
    setclock 1 {out_dt}
    useclock {rootname} 1
end



/* This function returns a string to be used for a one-line header at the
   beginning of an ascii file that contains values of Vm or Ik for each
   cell in the network, at time steps netview_dt. When binary file output
   is used with the disk_out object, the file contains information on the
   network dimensions that are needed for the xview object display.  When
   asc_file is used to generate the network data, this information is
   provided in a header of the form:

   #optional_RUNID_string Ntimes start_time dt NX NY SEP_X SEP_Y x0 y0 z0

   This header may be read by a data analysis script, such as netview.py.

   The line must start with "#" and can optionally be followed immediately
   by any string.  Typically this is some identification string generated
   by the simulation run.  The following parameters, separated by blanks or
   any whitespace, are:

   * Ntimes - the number of lines in the file, exclusive of the header

   * start_time - the simulation time for the first data line (default 0)

   * dt - the time step used for output (netview_dt)

   * NX, NY - the integer dimensions of the network

   *  SEP_X, SEP_Y - the x,y distances between cells (optional)

   * x0, y0, z0 - the location of the compartment (data source) relative to
     the cell origin (often ignored)

   A typical header generated by this simulation is:

   #B0003	5000 0.0 0.0002	 48 48 4e-05  4e-05 0.0	 0.0	0.0
*/

function make_header(diskpath)
    str diskpath
    int Ntimes = {round {tmax/netview_dt}} // outputs t = 0 thru tmax - netview_dt
    str header_str = "#" @ {RUNID} @ "  " @ {Ntimes} @ " 0.0 " @ {netview_dt} @ "  "
    if(diskpath == {net_efile})
        header_str = {header_str} @ {Ex_NX} @ " " @ {Ex_NY} @ " " @ {Ex_SEP_X} @ \
        "  " @ {Ex_SEP_Y} @ " 0.0  0.0  0.0"
    elif(diskpath == {net_ifile})
        header_str = {header_str} @ {Inh_NX} @ " " @ {Inh_NY} @ " " @ {Inh_SEP_X} @ \
        "  " @ {Inh_SEP_Y} @ " 0.0  0.0  0.0"
    elif(diskpath == {net_EPSC_file})
	header_str = {header_str} @ {Ex_NX} @ " " @ {Ex_NY} @ " " @ {Ex_SEP_X} @ \
	"  " @ {Ex_SEP_Y} @ " 0.0  0.0	0.0"
    else
        echo "Wrong file name root!"
        header_str = ""
    end    
    return {header_str}
end

/* Create disk_out element to write netview data to a binary or ascii  file */
function do_disk_out(diskpath,srcpath, srcelement, field)
    	str name, diskpath, srcpath, srcelement, field, filename
    	if ({exists /output/{diskpath}})
            delete /output/{diskpath}
    	end

	filename = {diskpath}  @ "_" @ {RUNID} @ ".txt"
    	create asc_file /output/{diskpath}
        setfield /output/{diskpath} leave_open 1 flush 0 filename {filename}
        setfield /output/{diskpath} float_format %.3g notime 1

        setfield /output/{diskpath} append 1
        call /output/{diskpath} OUT_OPEN
        call /output/{diskpath} OUT_WRITE {make_header {diskpath}}
        reset

	foreach name ({getelementlist {srcpath}})
            addmsg {name}/solver /output/{diskpath} SAVE \
		{findsolvefield {name}/solver {name}/{srcelement} {field}}
	end
end

function do_network_out

      setclock 2 {netview_dt}
      do_disk_out {net_efile} /Ex_layer/{Ex_cell_name}[] soma Vm
      useclock /output/{net_efile} 2
      do_disk_out {net_ifile} /Inh_layer/{Inh_cell_name}[] soma Vm
      useclock /output/{net_ifile} 2

      do_disk_out {net_EPSC_file} /Ex_layer/{Ex_cell_name}[] {Ex_ex_synpath} Ik
      setclock 2 {netview_dt}
      useclock /output/{net_EPSC_file} 2

end


/* ------------------------------------------------------------------
 Create a calculator object to hold summed Ex_ex currents, and then
 send all Ex_ex synaptic currents to it for summation

  NOTE:  Previous versions of make_EPSCsummer also summed the excitatory
  currents from the thalamic input drive. Here, the effect of any input
  drive would be indirect through propagation of its effect from cell to
  cell via synaptic connections.
------------------------------------------------------------------- */



function make_EPSCsummer // data_source sums Ex_cell ex currents
    int i
    create calculator {data_source}
    useclock {data_source} 1 // the clock for out_dt
    for (i=0; i < Ex_NX*Ex_NY; i = i + 1)
            addmsg /Ex_layer/{Ex_cell_name}[{i}]/solver {data_source} SUM \
              {findsolvefield /Ex_layer/{Ex_cell_name}[{i}]/solver \
              {Ex_ex_synpath} Ik}
    end
end

function do_EPSCsum_out
        if (! {exists {data_source}})
            make_EPSCsummer
        end
        make_output {EPSC_sum_file}
        addmsg {data_source} {EPSC_sum_file} SAVE output
end



function do_run_summary
    str filename = {sum_file} @ "_" @ {RUNID} @ ".txt"
    openfile {filename} w
    writefile {filename} "Script:" {script_name} "  RUNID:" {RUNID} "  seed:" {seed} \
        "  date:" {getdate}
    writefile {filename} "tmax:" {tmax} " dt:" {dt} " out_dt:" {out_dt} \
        " netview_dt:" {netview_dt} 
    writefile {filename} "Ex_NX:" {Ex_NX} " Ex_NY:" {Ex_NY} " Inh_NX:" \
        {Inh_NX} "  Inh_NY:" {Inh_NY}
    writefile {filename} "Ex_SEP_X:" {Ex_SEP_X} " Ex_SEP_Y:" {Ex_SEP_Y} \
        "  Inh_SEP_X:" {Inh_SEP_X}  "  Inh_SEP_Y:" {Inh_SEP_Y}
    writefile {filename} "Ninputs:" {Ninputs} " bg Ex freq:" {frequency} \
        " bg Ex gmax:" {Ex_bg_gmax}
    writefile {filename} "================== Network parameters ================="
    writefile {filename} "Ex_ex_gmax:" {Ex_ex_gmax} " Ex_inh_gmax:" {Ex_inh_gmax} \
        "  Inh_ex_gmax:" {Inh_ex_gmax} "  Inh_inh_gmax:" {Inh_inh_gmax}
    writefile {filename} "tau1_ex:" {tau1_ex} "  tau2_ex:" {tau2_ex}  \
        "  tau1_inh:" {tau1_inh} "  tau2_inh:" {tau2_inh}
    writefile {filename} "syn_weight: " {syn_weight} \
        " prop_delay:" {prop_delay} " default drive weight:" {drive_weight}
    writefile {filename} "Ex_drive_gmax: " {Ex_drive_gmax} \
        "  Inh_drive_gmax: " {Inh_drive_gmax}
    /* The code below is specific to the input model -- see MGBv_input.g */
    writefile {filename} "MGBv input delay: " {input_delay} \
	"  MGBv input jitter :" {input_jitter}
    writefile {filename} "================== Thalamic inputs ================="
    writefile {filename} "Input" " Row " "Frequency" "    State" "   Weight" \
        "    Delay" "    Width" " Period"
    int input_num, input_row
    str  input_source = "/MGBv" // Name of the array of input elements
    float input_freq, delay, width, interval, drive_weight
    str pulse_src, spike_out
    str toggle_state
    floatformat %10.3f
    /* 	
    for (input_num = 1; input_num <= {Ninputs}; input_num= input_num +1)
        pulse_src = {input_source} @ "[" @ {input_num} @ "]" @ "/spikepulse"
        spike_out = {input_source} @ "[" @ {input_num} @ "]" @ "/soma/spike"
        input_row  = \
          {getfield {{input_source} @ "[" @ {input_num} @ "]"} input_row}
        input_freq  = \
          {getfield {{input_source} @ "[" @ {input_num} @ "]"} input_freq}
        drive_weight = \
          {getfield {{input_source} @ "[" @ {input_num} @ "]"} output_weight}
        delay = {getfield {pulse_src} delay1 }
        width = {getfield {pulse_src} width1}
        interval = {getfield {pulse_src} delay1} + {getfield {pulse_src} delay2}
        // get the spiketoggle state
        toggle_state = "OFF"
        if ({getfield {pulse_src} level1} > 0.5)
            toggle_state = "ON"
        end
        writefile {filename} {input_num} {input_row} -n -format "%5s"
        writefile {filename} {input_freq} {toggle_state} {drive_weight} \
            {delay} {width} {interval}  -format %10s
    end */
    writefile {filename} "----------------------------------------------------------"
    writefile {filename} "Notes:"
    closefile {filename}
    floatformat %0.10g
end


function step_tmax
    echo "dt = "{getclock 0}"   tmax = "{tmax}
    echo "RUNID: " {RUNID}
    echo "START: " {getdate}
    step {tmax} -time
    echo "END  : " {getdate}
    //do_run_summary
end

//=============================================================
//    Functions to set up the network
//=============================================================

function make_prototypes
  /* Step 1: Assemble the components to build the prototype cell under the
     neutral element /library.  This is done by including "protodefs.g"
     before using the function make_prototypes.
  */
  
  /* Step 2: Create the prototype cell specified in 'cellfile', using readcell.
     This should set up the apropriate synchans in specified compartments,
     with a spikegen element "spike" attached to the soma.  This will be
     done in /library, where it will be available to be copied into a network

     In this case there are the types of cells.
  */

  readcell {Ex_cellfile} /library/{Ex_cell_name}
  readcell {Inh_cellfile} /library/{Inh_cell_name}


  // In this case, use different values from the defaults in 'cellfile'
  setfield /library/{Ex_cell_name}/{Ex_ex_synpath} gmax {Ex_ex_gmax}
  setfield /library/{Ex_cell_name}/{Ex_inh_synpath} gmax {Ex_inh_gmax}
  setfield /library/{Ex_cell_name}/{Ex_drive_synpath} gmax {Ex_drive_gmax}
  setfield /library/{Ex_cell_name}/axon/spike thresh 0 abs_refract 0.002 \
	output_amp 1
  // Note: the Ex-cell has wider and slower spikes, so use larger abs_refract

  setfield /library/{Inh_cell_name}/{Inh_ex_synpath} gmax {Inh_ex_gmax}
  setfield /library/{Inh_cell_name}/{Inh_inh_synpath} gmax {Inh_inh_gmax}
  setfield /library/{Inh_cell_name}/{Inh_drive_synpath} gmax {Inh_drive_gmax}
  setfield /library/{Inh_cell_name}/soma/spike thresh 0  abs_refract 0.001 \
	 output_amp 1

end

/***** functions to set up the network *****/

function make_network // For the standard network with 1 Exc population and 1 Inh population
  /* Step 3 - make a 2D array of cells with copies of /library/cell */
  // usage: createmap source dest Nx Ny -delta dx dy [-origin x y]

  /* There will be NX cells along the x-direction, separated by SEP_X,
     and  NY cells along the y-direction, separated by SEP_Y.
     The default origin is (0, 0).  This will be the coordinates of cell[0].
     The last cell, cell[{NX*NY-1}], will be at (NX*SEP_X -1, NY*SEP_Y-1).
  */
  createmap /library/{Ex_cell_name} /Ex_layer {Ex_NX} {Ex_NY} \
      -delta {Ex_SEP_X} {Ex_SEP_Y}

  // Displace the /Inh_layer origin to be in between Ex_cells
  createmap /library/{Inh_cell_name} /Inh_layer {Inh_NX} {Inh_NY} \
      -delta {Inh_SEP_X} {Inh_SEP_Y} -origin {Ex_SEP_X/2}  {Ex_SEP_Y/2}

end // function make_network





function connect_cells(Ex_ex_red,Ex_inh_red,Inh_ex_red,Inh_inh_red)
  /* Step 4: Now connect them up with planarconnect.  Usage:
   * planarconnect source-path destination-path
   *               [-relative]
   *               [-sourcemask {box,ellipse} xmin ymin xmax ymax]
   *               [-sourcehole {box,ellipse} xmin ymin xmax ymax]
   *               [-destmask   {box,ellipse} xmin ymin xmax ymax]
   *               [-desthole   {box,ellipse} xmin ymin xmax ymax]
   *               [-probability p]
   */

  /* Connect each source spike generator to target synchans within the
     specified range.  Set the ellipse axes or box size just higher than the
     cell spacing, to be sure cells are included.  To connect to nearest
     neighbors and the 4 diagonal neighbors, use a box:
       -destmask box {-SEP_X*1.01} {-SEP_Y*1.01} {SEP_X*1.01} {SEP_Y*1.01}
     For all-to-all connections with a 10% probability, set both the sourcemask
     and the destmask to have a range much greater than NX*SEP_X using options
       -destmask box -1 -1  1  1 \
       -probability 0.1
     Set desthole to exclude the source cell, to prevent self-connections.

     In an earlier version, the destination was divided into three rings, with
     decreasing connection probabilities.  The same function is used
     for both Ex_cells and Inh_cells.

     In this version, with the flag 'use_prob_decay = 1', the  connection
     probability is weighted with a probability exp(-d*d/(sigma*sigma))
     where r is the radial distance between source and destination
     in the x-y plane.
  */

  /*
  Typical values from experiment are:

  float Ex2Ex_prob = 0.1
  float Ex2Inh_prob = 0.3
  float Inh2Ex_prob = 0.4
  float Inh2Inh_prob = 0.4  // (a guess, data not available)
  */

  float Ex_ex_red,Ex_inh_red,Inh_ex_red,Inh_inh_red

  /* Default values used in this simulation */
  float Ex2Ex_prob = {0.15 * {Ex_ex_red}}
  float Ex2Inh_prob = {0.45* {Inh_ex_red}}
  float Inh2Ex_prob = {0.6* {Ex_inh_red}}
  float Inh2Inh_prob = {0.6* {Inh_inh_red}}  // (a guess, data not available)

  // distance at which number of target cells becomes very small
  float pyr_range = 25*Ex_SEP_X 
  float bask_range = 25*Ex_SEP_X




    float Ex_sigma = 10.0*Ex_SEP_X // values from K Yaun SfN 2008 poster fit
    float Inh_sigma = 10.0*Ex_SEP_X


    planarconnect_probdecay /Ex_layer/{Ex_cell_name} "axon/spike" {Ex_NX*Ex_NY} \
      /Ex_layer/{Ex_cell_name} {Ex_ex_synpath} {Ex_NX*Ex_NY} \
      {0.5*Ex_SEP_X} {pyr_range} {Ex2Ex_prob} {Ex_sigma}

    // Inh_ex connections don't need an intial desthole, so rmin = 0.0
    planarconnect_probdecay /Ex_layer/{Ex_cell_name} "axon/spike" {Ex_NX*Ex_NY} \
      /Inh_layer/{Inh_cell_name} {Inh_ex_synpath} {Inh_NX*Inh_NY} \
      0.0 {pyr_range} {Ex2Inh_prob} {Ex_sigma}

    planarconnect_probdecay /Inh_layer/{Inh_cell_name} "soma/spike" \
      {Inh_NX*Inh_NY} /Ex_layer/{Ex_cell_name} {Ex_inh_synpath} {Ex_NX*Ex_NY} \
      0.0 {bask_range} {Inh2Ex_prob} {Inh_sigma}

    planarconnect_probdecay /Inh_layer/{Inh_cell_name} "soma/spike" {Inh_NX*Inh_NY} \
      /Inh_layer/{Inh_cell_name} {Inh_inh_synpath} {Inh_NX*Inh_NY} \
      {Inh_SEP_X*0.5} {bask_range} {Inh2Inh_prob} {Inh_sigma}


end // function connect_cells

// Utility functions to calculate statistics
function print_avg_syn_number
    int n
    int num_Ex_ex = 0
    int num_Ex_inh = 0
    for (n=0; n < Ex_NX*Ex_NY; n=n+1)
        num_Ex_ex = num_Ex_ex + {getsyncount \
            /Ex_layer/{Ex_cell_name}[{n}]/{Ex_ex_synpath}}
        num_Ex_inh = num_Ex_inh + {getsyncount \
            /Ex_layer/{Ex_cell_name}[{n}]/{Ex_inh_synpath}}
    end
    num_Ex_ex = num_Ex_ex/(Ex_NX*Ex_NY)
    num_Ex_inh = num_Ex_inh/(Ex_NX*Ex_NY)
    int num_Inh_ex = 0
    int num_Inh_inh = 0
    for (n=0; n < Inh_NX*Inh_NY; n=n+1)
        num_Inh_ex = num_Inh_ex + {getsyncount \
            /Inh_layer/{Inh_cell_name}[{n}]/{Inh_ex_synpath}}
        num_Inh_inh = num_Inh_inh + {getsyncount \
            /Inh_layer/{Inh_cell_name}[{n}]/{Inh_inh_synpath}}
    end
    num_Inh_ex = num_Inh_ex/(Inh_NX*Inh_NY)
    num_Inh_inh = num_Inh_inh/(Inh_NX*Inh_NY)
    echo "Average number of Ex_ex synapses per cell: " {num_Ex_ex}
    echo "Average number of Ex_inh synapses per cell: " {num_Ex_inh}
    echo "Average number of Inh_ex synapses per cell: " {num_Inh_ex}
    echo "Average number of Inh_inh synapses per cell: " {num_Inh_inh}
end // print_avg_syn_number


/**** set synchan parameters ****/

function set_Ex_ex_gmax(value)  // excitatory synchan gmax in Ex_cell
   float value                  // value in nA
   Ex_ex_gmax = {value}*1e-9	// use this for driver input also
   setfield /Ex_layer/{Ex_cell_name}[]/{Ex_ex_synpath} gmax {Ex_ex_gmax}
end

function set_Ex_drive_gmax(value)  // thalamic drive synchan gmax in Ex_cell
   float value                  // value in nA
   Ex_drive_gmax = {value}*1e-9
   setfield /Ex_layer/{Ex_cell_name}[]/{Ex_drive_synpath} gmax {Ex_drive_gmax}
end

function set_Ex_bg_gmax(value)  // background ex  synchan gmax in Ex_cell
   float value                  // value in nA
   Ex_bg_gmax = {value}*1e-9
   setfield /Ex_layer/{Ex_cell_name}[]/{Ex_bg_synpath} gmax {Ex_bg_gmax}
end

function set_Inh_ex_gmax(value)   // excitatory synchan gmax in Inh_cell
   float value			  // value in nA
   Inh_ex_gmax = {value}*1e-9	  // use this for driver input also
   setfield /Inh_layer/{Inh_cell_name}[]/{Inh_ex_synpath} gmax {Inh_ex_gmax}
end

function set_Inh_drive_gmax(value) // thalamic drive synchan gmax in Inh_cell
   float value			  // value in nA
   Inh_drive_gmax = {value}*1e-9
   setfield /Inh_layer/{Inh_cell_name}[]/{Inh_drive_synpath} gmax {Inh_drive_gmax}
end

function set_Ex_inh_gmax(value)  // inhibitory synchan gmax in Ex_cell
   float value			  // value in nA
   Ex_inh_gmax = {value}*1e-9
   setfield /Ex_layer/{Ex_cell_name}[]/{Ex_inh_synpath} gmax {Ex_inh_gmax}
end

function set_Inh_inh_gmax(value)  // inhibitory synchan gmax in Inh_cell
   float value			  // value in nA
   Inh_inh_gmax = {value}*1e-9
   setfield /Inh_layer/{Inh_cell_name}[]/{Inh_inh_synpath} gmax {Inh_inh_gmax}
end

function set_all_gmax // set all gmax to Ex_ex_gmax, ..., Ex_bg_gmax
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_ex_synpath} gmax \
        {Ex_ex_gmax}
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_inh_synpath} gmax \
        {Ex_inh_gmax}
    setfield /Inh_layer/{Inh_cell_name}[]/{Inh_ex_synpath} gmax \
        {Inh_ex_gmax}
    setfield /Inh_layer/{Inh_cell_name}[]/{Inh_inh_synpath}  gmax \
        {Inh_inh_gmax}
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_drive_synpath} gmax \
        {Ex_drive_gmax}
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_bg_synpath} gmax \
        {Ex_bg_gmax}
    setfield /Inh_layer/{Inh_cell_name}[]/{Inh_drive_synpath}  gmax \
        {Inh_drive_gmax}
end

/* NOTE: Functions to set synchan tau1 and tau2 values should be called
   only prior to hsolve SETUP.  Unlike the case with gmax, which may be
   changed if followed by a reset, changing the taus of hsolved synchans
   causes erroneous results.
*/
function set_all_taus  // assume all synchans of one type have same taus
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_ex_synpath} tau1 {tau1_ex} \
        tau2 {tau2_ex}
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_drive_synpath} tau1 {tau1_ex} \
        tau2 {tau2_ex}
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_inh_synpath} tau1 {tau1_inh} \
        tau2 {tau2_inh}
    setfield /Inh_layer/{Inh_cell_name}[]/{Inh_ex_synpath} tau1 {Inh_tau1_ex} \
        tau2 {Inh_tau2_ex}
    setfield /Inh_layer/{Inh_cell_name}[]/{Inh_drive_synpath} tau1 {tau1_ex}\
        tau2 {tau2_ex}
    setfield /Inh_layer/{Inh_cell_name}[]/{Inh_inh_synpath} tau1 {tau1_inh} \
        tau2 {tau2_inh}
    setfield /Ex_layer/{Ex_cell_name}[]/{Ex_bg_synpath} tau1 {tau1_ex} \
        tau2 {tau2_ex}
end

/***** functions to set weights and delays *****/

function set_weights(weight)
    float weight
    syn_weight = weight  // set the global variable to the new weight
    // use fixed weights  // The defualt
    volumeweight /Ex_layer/{Ex_cell_name}[]/axon/spike \
                /Ex_layer/{Ex_cell_name}[]/{Ex_ex_synpath} \
                -fixed {syn_weight}
    volumeweight /Ex_layer/{Ex_cell_name}[]/axon/spike \
                /Inh_layer/{Inh_cell_name}[]/{Inh_ex_synpath} \
                -fixed {syn_weight}
    volumeweight /Inh_layer/{Inh_cell_name}[]/soma/spike  \
            /Ex_layer/{Ex_cell_name}[]/{Ex_inh_synpath} \
                -fixed {syn_weight}
    volumeweight /Inh_layer/{Inh_cell_name}[]/soma/spike  \
                /Inh_layer/{Inh_cell_name}[]/{Inh_inh_synpath} \
                -fixed {syn_weight}
    echo "All maxium synaptic weights set to "{weight}
end

// TO DO: Finish!!!!
function make_AMPAExnoisesummer // data_source sums Ex_cell drive currents
    int i
    create calculator "/Noise"
    useclock "/Noise" 1 // the clock for out_dt
    for (i=0; i < Ex_NX*Ex_NY; i = i + 1)
            addmsg /Ex_layer/{Ex_cell_name}[{i}]/solver "/Noise" SUM \
              {findsolvefield /Ex_layer/{Ex_cell_name}[{i}]/solver \
              {Ex_bg_synpath} Ik}
    end
end

function do_AMPAExnoisesum_out
        if (! {exists "/Noise"})
            make_AMPAExnoisesummer
        end
        make_output "Noise_test"
        addmsg "/Noise" "Noise_test" SAVE output
end

