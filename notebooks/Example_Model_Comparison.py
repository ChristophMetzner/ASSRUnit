#!/usr/bin/env python
# coding: utf-8

# ## Example_Model_Comparison2
# This notebook demonstrates how two different models can be compared against each other
# and against experimental data.

# ### Note:
# It is important here to stress the difference between conceptual/theoretical models and implementations of network models. In the example below, we will compare two conceptual models against each other
#
# Conceptual Model 1: Prolonged decay times at inhibitory synapses result in schizophrenia-like ASSRs in the gamma and beta band.
#
# Conceptual Model 2: Reduced excitation of inhibitory neurons results in schizophrenia-like ASSRs in the gamma and beta band.
#
# However, both conceptual models are implemented using the same network model implementation, although, obviously, with different parameters.
#

# In[3]:


get_ipython().run_line_magic("matplotlib", "inline")
import sciunit
import sys

sys.path.append("/home/cm15acr/ASSRUnit/Code")

from capabilities import ProduceXY

from models import VierlingSimpleModel

from testsAndPredictionTests import Test4040, Test3030, Test2020, Test2040, Test4020


# ### Parameters

# In[4]:


# Conceptual/theoretical model 1
controlparams_model_1 = {
    "n_ex": 20,
    "n_inh": 10,
    "eta": 5.0,
    "tau_R": 0.1,
    "tau_ex": 2.0,
    "tau_inh": 8.0,
    "g_ee": 0.015,
    "g_ei": 0.025,
    "g_ie": 0.015,
    "g_ii": 0.02,
    "g_de": 0.3,
    "g_di": 0.08,
    "dt": 0.05,
    "b_ex": -0.01,
    "b_inh": -0.01,
    "background_rate": 33.3,
    "A": 0.5,
    "seed": 12345,
    "filename": "default",
    "directory": "/",
}
schizparams_model_1 = {
    "n_ex": 20,
    "n_inh": 10,
    "eta": 5.0,
    "tau_R": 0.1,
    "tau_ex": 2.0,
    "tau_inh": 28.0,
    "g_ee": 0.015,
    "g_ei": 0.025,
    "g_ie": 0.015,
    "g_ii": 0.02,
    "g_de": 0.3,
    "g_di": 0.08,
    "dt": 0.05,
    "b_ex": -0.01,
    "b_inh": -0.01,
    "background_rate": 33.3,
    "A": 0.5,
    "seed": 12345,
    "filename": "default",
    "directory": "/",
}

controlparams_model_2 = {
    "n_ex": 20,
    "n_inh": 10,
    "eta": 5.0,
    "tau_R": 0.1,
    "tau_ex": 2.0,
    "tau_inh": 8.0,
    "g_ee": 0.015,
    "g_ei": 0.025,
    "g_ie": 0.015,
    "g_ii": 0.02,
    "g_de": 0.3,
    "g_di": 0.08,
    "dt": 0.05,
    "b_ex": -0.01,
    "b_inh": -0.01,
    "background_rate": 33.3,
    "A": 0.5,
    "seed": 12345,
    "filename": "default",
    "directory": "/",
}
schizparams_model_2 = {
    "n_ex": 20,
    "n_inh": 10,
    "eta": 5.0,
    "tau_R": 0.1,
    "tau_ex": 2.0,
    "tau_inh": 8.0,
    "g_ee": 0.015,
    "g_ei": 0.015,
    "g_ie": 0.015,
    "g_ii": 0.02,
    "g_de": 0.3,
    "g_di": 0.08,
    "dt": 0.05,
    "b_ex": -0.01,
    "b_inh": -0.01,
    "background_rate": 33.3,
    "A": 0.5,
    "seed": 12345,
    "filename": "default",
    "directory": "/",
}


# ### Model instances

# In[5]:


conceptual_model_1 = VierlingSimpleModel(
    controlparams_model_1, schizparams_model_1, name="Conceptual_model_1"
)
conceptual_model_2 = VierlingSimpleModel(
    controlparams_model_2, schizparams_model_2, name="Conceptual_model_2"
)


# ### Tests (note that observations are not yet from the experimental database!!)

# In[6]:


test_4040 = Test4040(observation={"ratio": 0.5})
test_3030 = Test3030(observation={"ratio": 1.0})
test_2020 = Test2020(observation={"ratio": 1.0})
test_2040 = Test2040(observation={"ratio": 1.0})
test_4020 = Test4020(observation={"ratio": 1.0})


# ### A test suite

# In[ ]:


kwon_vierling_main_suite = sciunit.TestSuite(
    "kwon_vierling_main", [test_4040, test_3030, test_2020, test_4020, test_2040]
)
score_matrix = kwon_vierling_main_suite.judge([conceptual_model_1, conceptual_model_2])
score_matrix.view()


# In[ ]:
