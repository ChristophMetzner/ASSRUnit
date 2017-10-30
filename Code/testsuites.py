import sciunit

from sciunit.scores import BooleanScore  
from capabilities import Produce4040,Produce3030,Produce2020,Produce4020,Produce2040
from tests import Test4040,Test3030,Test2020,Test4020,Test2040












##################################################
#
# Instantiates a testsuite that covers for the main findings of the following two studies
#  Kwon et al., Gamma frequency range abnormalities to auditory stimulation in schizophrenia. Archives of General Psychiatry,1999
#  Vierling-Claassen et al., Modeling GABA alterations in schizophrenia: a link between impaired inhibition and altered gamma and beta range auditory entrainment.
#   Journal of Neurophysiology,2008
#
##################################################

# load database
observations = np.load()

observation_4040 =
observation_3030 =
observation_2020 =
observation_2040 =
observation_4020 =

test_4040 = Test4040(observation=observation_4040)
test_3030 = Test3030(observation=observation_3030)
test_2020 = Test2020(observation=observation_2020)
test_2040 = Test2040(observation=observation_2040)
test_4020 = Test4020(observation=observation_4020)

kwon_vierling_main_suite = sciunit.TestSuite('kwon_vierling_main',[test_4040,test_3030,test_2020,test_2040,test_4020])






##################################################
#
# Instantiates a testsuite that covers for a subset of findings from the following study
#  Krishnan et al., Steady state and induced auditory gamma deficits in schizophrenia, Neuroimage, 2009
# 
##################################################
