#!/usr/bin/env python
# coding: utf-8

# ### Using the NeuroML2 version of the model from Beeman (2013)
# A short example demonstrating how to use the NML2 version of the model from Beeman (2013)
#
#
# Note: change the path in the cell below to match your file system!

# In[1]:


import sciunit
import sys

sys.path.append("/home/cm15acr/ASSRUnit/Code")

from capabilities import ProduceXY

from models import BeemanNML2Model

from testsAndPredictionTests import Test4040, Test3030, Test2020, Test2040, Test4020


# ### Parameters

# In[2]:


controlparams = {
    "Filename": "control_model",
    "Random Seed": 12345,
    "E-E Weight": 30.0e-9,
    "I-E Weight": 0.1e-9,
    "E-I Weight": 0.6e-9,
    "I-I Weight": 0.15e-9,
    "Background Noise Weight": 80.0e-9,
    "E-Drive Weight": 50.0e-9,
    "I-Drive Weight": 1.5e-9,
    "Background Noise Frequency": 8.0,
    "Simulation Time": 1000,
    "Time Step": 0.025,
}

schizparams = {
    "Filename": "schiz_model",
    "Random Seed": 12345,
    "E-E Weight": 30.0e-9,
    "I-E Weight": 0.05e-9,
    "E-I Weight": 0.6e-9,
    "I-I Weight": 0.15e-9,
    "Background Noise Weight": 80.0e-9,
    "E-Drive Weight": 50.0e-9,
    "I-Drive Weight": 1.5e-9,
    "Background Noise Frequency": 8.0,
    "Simulation Time": 1000,
    "Time Step": 0.025,
}


# ### Model

# In[3]:


test_model = BeemanNML2Model(controlparams, schizparams)


# ### Tests

# In[4]:


test_4040 = Test4040(observation={"ratio": 0.5})
score_4040 = test_4040.judge(test_model)
"""
test_3030 = Test3030(observation={'ratio':1.0})
score_3030 = test_3030.judge(test_model)

test_2020 = Test2020(observation={'ratio':1.0})
score_2020 = test_2020.judge(test_model)

test_2040 = Test2040(observation={'ratio':1.0})
score_2040 = test_2040.judge(test_model)

test_4020 = Test4020(observation={'ratio':1.0})
score_4020 = test_4020.judge(test_model)
"""
print "\n\n Results 4040:\n"
print score_4040
"""
print '\n Results 3030:\n'
print score_3030
print '\n Results 2020:\n'
print score_2020
print '\n Results 2040:\n'
print score_2040
print '\n Results 4020:\n'
print score_4020
"""


# In[ ]:
