from neuroml import NeuroMLDocument
from neuroml import Network
from neuroml import Population
from neuroml import Location
from neuroml import Instance
from neuroml import Projection
from neuroml import Connection
from neuroml import PulseGenerator
from neuroml import ExplicitInput


import math
import random
import numpy as np

import neuroml.writers as writers

def ellipse(x,y):



	a = 0.004 
	b = 0.0015

	inside = 0
	res = ((x**2)/(a**2)+(y**2)/(b**2))

	if (((x*x)/(a*a)+(y*y)/(b*b)) < 1):
 
		inside = 1

	return inside



def add_connection(projection, id, pre_pop, pre_component, pre_cell_id, pre_seg_id, post_pop, post_component, post_cell_id, post_seg_id):
    
    connection = Connection(id=id, \
                            pre_cell_id="../%s/%i/%s"%(pre_pop, pre_cell_id, pre_component), \
                            pre_segment_id=pre_seg_id, \
                            pre_fraction_along=0.5,
                            post_cell_id="../%s/%i/%s"%(post_pop, post_cell_id, post_component), \
                            post_segment_id=post_seg_id,
                            post_fraction_along=0.5)

    projection.connections.append(connection)


def getDAPCNumber(xscale,yscale):
	xSpacing = 0.008/xscale 
	ySpacing = 0.003/yscale
	
	print xSpacing
	print ySpacing

	vapcNumber = 0
	dapcNumber = 0


	for i in range(0, xscale/2) :
	    for j in range(0, yscale):
		# create cells
		x = i*xSpacing
		y = j*ySpacing


		if(ellipse(x,y)):
			vapcNumber += 1
		else:
	    	        dapcNumber += 1


	

	return dapcNumber, vapcNumber

