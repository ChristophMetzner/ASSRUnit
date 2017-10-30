import sciunit
import numpy as np

from capabilities import Produce4040,Produce3030,Produce2020,Produce2040,Produce4020

from models import VierlingSimpleModelRobust

#from tests import Test4040,Test3030,Test2020,Test2040,Test4020

from visualizations import boxplot


# Parameters
controlparams = {'n_ex': 20,'n_inh': 10,'eta': 5.0,'tau_R': 0.1,'tau_ex': 2.0,'tau_inh': 8.0,'g_ee': 0.015,'g_ei': 0.025,'g_ie': 0.015,'g_ii': 0.02,'g_de': 0.3,'g_di': 0.08,'dt': 0.05,'b_ex': -0.01,'b_inh': -0.01,'background_rate': 33.3,'A': 0.5,'filename': 'default','directory': '/'}

schizparams = {'n_ex': 20,'n_inh': 10,'eta': 5.0,'tau_R': 0.1,'tau_ex': 2.0,'tau_inh': 28.0,'g_ee': 0.015,'g_ei': 0.025,'g_ie': 0.015,'g_ii': 0.02,'g_de': 0.3,'g_di': 0.08,'dt': 0.05,'b_ex': -0.01,'b_inh': -0.01,'background_rate': 33.3,'A': 0.5,'filename': 'default','directory': '/'}

seeds = np.load('Seeds.npy')

# Model
test_model = VierlingSimpleModelRobust(controlparams,schizparams,seeds)

print 'Run simulations (this might take 15-20 minutes)'
print '\n 4040'
mcontrol4040,mschiz4040,control4040,schiz4040 = test_model.produce_4040_plus()
print '\n 3030'
mcontrol3030,mschiz3030,control3030,schiz3030 = test_model.produce_3030_plus()
print '\n 2020'
mcontrol2020,mschiz2020,control2020,schiz2020 = test_model.produce_2020_plus()
print '\n 2040'
mcontrol2040,mschiz2040,control2040,schiz2040 = test_model.produce_2040_plus()
print '\n 4020'
mcontrol4020,mschiz4020,control4020,schiz4020 = test_model.produce_4020_plus()


''' Test data 
control=[ 273.70874018,  272.29687814,  259.02873848,  263.16652506, 269.98480004,244.49154012,  259.88818885,  272.51683841,  271.44683391,  266.05781351, 266.44570049,  274.34722645,  266.60167892,  265.12893524,  245.49889625, 270.36819366,  277.94737605,  274.32056976,  272.6249043,   261.06052421]
schiz=[  95.06507187,  102.83793708,   77.6098936,    55.81005427,  101.9364996,82.79047348,   78.81260129,   96.5924012,    74.17096554,   81.01121989,101.98948378,  101.31284168,   91.58077201,   81.00782794,   85.26626513,100.84607923,   98.01196816,   96.37975389,   88.48082979,   98.89703685,]
'''



# Plot data as a boxplot
boxplot([control4040,schiz4040,control3030,schiz3030,control2020,schiz2020,control2040,schiz2040,control4020,schiz4020,],['control4040','schizophrenia4040','control3030','schizophrenia3030','control2020','schizophrenia2020','control2040','schizophrenia2040','control4020','schizophrenia4020'])















































