import sciunit

from capabilities import Produce4040,Produce3030,Produce2020,Produce2040,Produce4020

from models import VierlingSimpleModel

from tests import Test4040,Test3030,Test2020,Test2040,Test4020



# Parameters
controlparams = {'n_ex': 20,'n_inh': 10,'eta': 5.0,'tau_R': 0.1,'tau_ex': 2.0,'tau_inh': 8.0,'g_ee': 0.015,'g_ei': 0.025,'g_ie': 0.015,'g_ii': 0.02,'g_de': 0.3,'g_di': 0.08,'dt': 0.05,'b_ex': -0.01,'b_inh': -0.01,'background_rate': 33.3,'A': 0.5,'seed': 12345,'filename': 'default','directory': '/'}

schizparams = {'n_ex': 20,'n_inh': 10,'eta': 5.0,'tau_R': 0.1,'tau_ex': 2.0,'tau_inh': 28.0,'g_ee': 0.015,'g_ei': 0.025,'g_ie': 0.015,'g_ii': 0.02,'g_de': 0.3,'g_di': 0.08,'dt': 0.05,'b_ex': -0.01,'b_inh': -0.01,'background_rate': 33.3,'A': 0.5,'seed': 12345,'filename': 'default','directory': '/'}

# Model
test_model = VierlingSimpleModel(controlparams,schizparams)

# Tests (note that the observations are not correct!)
test_4040 = Test4040(observation={'ratio':0.5})
#score_4040 = test_4040.judge(test_model)
#print score_4040

test_3030 = Test3030(observation={'ratio':1.0})
#score_3030 = test_3030.judge(test_model)
#print score_3030

test_2020 = Test2020(observation={'ratio':1.0})
#score_2020 = test_2020.judge(test_model)
#print score_2020

test_2040 = Test2040(observation={'ratio':1.0})
#score_2040 = test_2040.judge(test_model)
#print score_2040

test_4020 = Test4020(observation={'ratio':1.0})
#score_4020 = test_4020.judge(test_model)
#print score_4020


# Test suite
kwon_vierling_main_suite = sciunit.TestSuite('kwon_vierling_main',[test_4040,test_3030,test_2020,test_4020,test_2040])
score_matrix = kwon_vierling_main_suite.judge(test_model)
print score_matrix


















































