# ASSRUnit - A Module for Automated Validation and Comparison of Models of Auditory Steady-State Response (ASSR) Deficits in Psychiatric Disorders

## Purpose
ASSRUnit is a module that integrates databases of experimental studies on ASSR deficits in psychiatric with a repository of computational models of these deficits using the [SciUnit](https://github.com/scidash/sciunit) framework. ASSRUnit allows the user: 

+ to browse the databases and to visualize results and meta-data of studies
+ to test computational models from the repository against observations from (a) study/ies from a database
+ to generate predictions from a computational model and to create prediction databases
+ add new database entries, databases, tests, models, predictions and prediction databases

For more information see this [article](https://www.mitpressjournals.org/doi/full/10.1162/cpsy_a_00015). For examples that illustrate how to use ASSRUnit see [here](https://github.com/ChristophMetzner/ASSRUnit/tree/CompPsychArticle/assrunit/Notebooks).

## Dependencies
In order to use ASSRUnit you need the following packages:
+ [Python 2.7]()
+ [SciUnit](https://github.com/scidash/sciunit)
+ [NumPy](http://www.numpy.org/)
+ [Matplotlib](https://matplotlib.org/)

In order to run some of the example notebooks and models you will additionally need to install the following simulators and tools:
+ [GENESIS](http://genesis-sim.org/) for the GENESIS version of the ACnet2 model
+ [pyNeuroML](https://github.com/NeuroML/pyNeuroML) and [Neuron](https://www.neuron.yale.edu/neuron/) for the NeuroML2 version of the ACnet2 model

In order to run the example notebooks you will need [Jupyter notebook](http://jupyter.org/).

If you want to use ASSRUnit, clone or download the repository and get started. 
