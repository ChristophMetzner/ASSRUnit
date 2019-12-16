#!/usr/bin/env python
# coding: utf-8

# # A simple example notebook that demonstrates how to query the database to get an overview of studies and observations

# In[1]:


get_ipython().run_line_magic("matplotlib", "inline")
import sys

sys.path.append("/home/cm15acr/ASSRUnit/Code")

import numpy as np
import matplotlib.pyplot as plt

from visualizations import experimental_overview, get_studies, get_observations


# ### List all studies in database

# In[2]:


s = get_studies(dbname="../Databases/ASSR_schizophrenia_experimental_database")
print s


# Note that, at the moment, providing the name of the database (by specifying *dbname*) is not necessary, because all database visualization methods use the '*ASSR schizophrenia*' database. However, in the future there might/will be several databases in *ASSRUnit* (e.g. for several psychiatric disorders) and by specifying *dbname*, one can choose the database to work with.

# ### List all observations in database

# In[3]:


o = get_observations(dbname="../Databases/ASSR_schizophrenia_experimental_database")
print o


# ## Qualitative representation of studies

# ### Full overview

# In[4]:


a = experimental_overview(
    dbname="../Databases/ASSR_schizophrenia_experimental_database"
)


# ### Specific studies

# In[5]:


studies = ["Kwon_1999", "Krishnan_2009"]
a = experimental_overview(
    studies=studies, dbname="../Databases/ASSR_schizophrenia_experimental_database"
)


# ### Specific observations

# In[6]:


observations = ["2020", "3030", "4040"]
a = experimental_overview(
    observations=observations,
    dbname="../Databases/ASSR_schizophrenia_experimental_database",
)


# ### Specific observations for specific studies

# In[7]:


observations = ["2020", "3030", "4040"]
studies = ["Kwon_1999", "Krishnan_2009"]
a = experimental_overview(
    studies=studies,
    observations=observations,
    dbname="../Databases/ASSR_schizophrenia_experimental_database",
)


# ## Quantitative representation of studies

# In[8]:


a = experimental_overview(
    entrytype="Full", dbname="../Databases/ASSR_schizophrenia_experimental_database"
)


# ### Specific studies

# In[9]:


studies = ["Kwon_1999", "Krishnan_2009"]
a = experimental_overview(
    studies=studies,
    entrytype="Full",
    dbname="../Databases/ASSR_schizophrenia_experimental_database",
)


# ### Specific observations

# In[10]:


observations = ["2020", "3030", "4040"]
a = experimental_overview(
    observations=observations,
    entrytype="Full",
    dbname="../Databases/ASSR_schizophrenia_experimental_database",
)


# ### Specific observations for specific studies

# In[11]:


observations = ["2020", "3030", "4040"]
studies = ["Kwon_1999", "Krishnan_2009"]
a = experimental_overview(
    studies=studies,
    observations=observations,
    entrytype="Full",
    dbname="../Databases/ASSR_schizophrenia_experimental_database",
)


# ### Display meta data

# In[12]:


a = experimental_overview(
    meta=True, dbname="../Databases/ASSR_schizophrenia_experimental_database"
)


# In[ ]:
