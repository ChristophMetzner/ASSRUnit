#!/usr/bin/env python
# coding: utf-8

# ### Using the simple model from Vierling-Claassen et al (2008)
# A short example demonstrating how to use the simle model from Vierling-Claasen et al. (2008)
#
#
# Note: change the path in the cell below to match your file system!

# In[1]:


import sciunit

from assrunit.models import VierlingSimpleModel

from assrunit.tests.test_and_prediction_tests import Test4040, Test3030, Test2020, Test2040, Test4020


# ### Parameters

# In[2]:


controlparams = {
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

schizparams = {
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


# ### Model

# In[3]:


test_model = VierlingSimpleModel(controlparams, schizparams)


# ### Tests

# In[4]:


test_4040 = Test4040(observation={"ratio": 0.5})
score_4040 = test_4040.judge(test_model)
print(score_4040)

test_3030 = Test3030(observation={"ratio": 1.0})
score_3030 = test_3030.judge(test_model)
print(score_3030)

test_2020 = Test2020(observation={"ratio": 1.0})
score_2020 = test_2020.judge(test_model)
print(score_2020)

test_2040 = Test2040(observation={"ratio": 1.0})
score_2040 = test_2040.judge(test_model)
print(score_2040)

test_4020 = Test4020(observation={"ratio": 1.0})
score_4020 = test_4020.judge(test_model)
print(score_4020)


# ### A test suite

# In[6]:


kwon_vierling_main_suite = sciunit.TestSuite(
    "kwon_vierling_main", [test_4040, test_3030, test_2020, test_4020, test_2040]
)
score_matrix = kwon_vierling_main_suite.judge(test_model)
score_matrix.view()


# In[ ]:
