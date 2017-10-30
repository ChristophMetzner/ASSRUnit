import sciunit


### The Capabilities ###

# Each capability is implemented separately, although many rely on 40Hz drive
# This increases the computating time, but makes the implementation simpler and more clear

# 40Hz power at 40Hz drive
class Produce4040(sciunit.Capability):
    """40Hz power at 40Hz drive"""

    def produce_4040(self):
        """The implementation of this method should return the power at 40Hz for 40Hz drive of  
	the 'schizophrenia-like' and the control network."""
        raise NotImplementedError("Must implement produce_4040.")


# 30Hz power at 30Hz drive
class Produce3030(sciunit.Capability):
    """30Hz power at 30Hz drive"""

    def produce_3030(self):
        """The implementation of this method should return the power at 30Hz for 30Hz drive of  
	the 'schizophrenia-like' and the control network."""
        raise NotImplementedError("Must implement produce_3030.")


# 20Hz power at 20Hz drive
class Produce2020(sciunit.Capability):
    """20Hz power at 20Hz drive"""

    def produce_2020(self):
        """The implementation of this method should return the power at 20Hz for 20Hz drive of  
	the 'schizophrenia-like' and the control network."""
        raise NotImplementedError("Must implement produce_2020.")


# 20Hz power at 40Hz drive
class Produce2040(sciunit.Capability):
    """20Hz power at 40Hz drive"""

    def produce_2040(self):
        """The implementation of this method should return the power at 20Hz for 40Hz drive of  
	the 'schizophrenia-like' and the control network."""
        raise NotImplementedError("Must implement produce_2040.")


# 40Hz power at 20Hz drive
class Produce4020(sciunit.Capability):
    """40Hz power at 20Hz drive"""

    def produce_4020(self):
        """The implementation of this method should return the power at 40Hz for 20Hz drive of  
	the 'schizophrenia-like' and the control network."""
        raise NotImplementedError("Must implement produce_4020.")


