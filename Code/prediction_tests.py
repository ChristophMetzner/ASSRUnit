import sciunit

from sciunit.scores import RatioScore # One of several SciUnit score types.  
from prediction_capabilities import PredictionProduce1010


# 10Hz/10Hz 
class PredictionTest1010(sciunit.Test):
    """Creates a model prediction for the difference in 10Hz power  at 10Hz drive between the 
	'schizophrenia-like' network compared to the control network."""   
    
    def __init__(self,observation = {'ratio':1.0},name='Prediction of 10Hz power to 10Hz drive'):# Since this is a prediction, we set the observation to 1.0, so that the ratio
	# reflects the ratio between power in the control and schizo-like network.
	sciunit.Test.__init__(self,observation,name) # Call the base constructor.  
	self.required_capabilities = (PredictionProduce1010,) 

    score_type = RatioScore # This test's 'judge' method will return a RatioScore.  
    
    def generate_prediction(self, model):
        [control1010,schiz1010] = model.prediction_produce_1010() # The model has this method if it inherits from the 'Produce1010' capability.
	return [control1010,schiz1010]    

    def compute_score(self, observation, prediction):
	if prediction[0]>0.0:
		result = {'ratio': prediction[1]/prediction[0]}
        score = self.score_type(result['ratio']/observation['ratio']) # Returns a RatioScore. 
        score.description = 'Score reflects the ratio between power in the control and schizo-like network.'
        return score
