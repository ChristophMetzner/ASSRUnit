import sciunit


### The Capabilities ###

# These are the additional cpapbilities required for the prediction tests


# Alpha - 10Hz power at 10 Hz drive
class PredictionProduce1010(sciunit.Capability):
    """10Hz power at 10Hz drive"""

    def prediction_produce_1010(self):
        """The implementation of this method should return the power at 10Hz for 10Hz drive of  
	the 'schizophrenia-like' and the control network."""
        raise NotImplementedError("Must implement produce_1010.")
