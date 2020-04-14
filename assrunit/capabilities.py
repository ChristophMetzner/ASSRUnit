import sciunit


### The Capabilities ###

# Each capability is implemented separately, although many rely on 40Hz drive
# This increases the computating time, but makes the implementation simpler and more clear

# X Hz power at Y Hz drive
class ProduceXY(sciunit.Capability):
    """X Hz power at Y Hz drive"""

    def produce_XY(self):
        """The implementation of this method should return the power at X Hz for Y Hz drive of  
        the 'schizophrenia-like' and the control network."""
        raise NotImplementedError("Must implement produce_XY.")
