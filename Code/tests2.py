import sciunit

# The type of score the test should return (probably have to change that to zscore or ratioscore)
from sciunit.scores import BooleanScore # One of several SciUnit score types.  
from capabilities2 import ProduceXY

### The test classes ###

# 40Hz/40Hz 
class Test4040(sciunit.Test):
    """Tests if the model predicts the reduction of 40Hz power in the 
	'schizophrenia-like' network compared to the control network."""   
    
    def __init__(self,observation = {'ratio':0.4},name='Reduction of 40Hz power to 40Hz drive'):
	sciunit.Test.__init__(self,observation,name) # Call the base constructor.  
	self.required_capabilities = (ProduceXY,) 

    score_type = BooleanScore # This test's 'judge' method will return a BooleanScore.  
    
    def generate_prediction(self, model):
        [control4040,schiz4040] = model.produce_XY(40.0,40.0) # The model has this method if it inherits from the 'Produce4040' capability.
	return [control4040,schiz4040]    

    def compute_score(self, observation, prediction):
	if prediction[0]>0.0:
		result = {'ratio': prediction[1]/prediction[0]}
        score = self.score_type(result['ratio'] < observation['ratio']) # Returns a BooleanScore. 
        score.description = 'Passing score if the prediction is smaller than the observation'
        return score

# 30Hz/30Hz 
class Test3030(sciunit.Test):
    """Tests if the model predicts the unchanged 30Hz power in the 
	'schizophrenia-like' network compared to the control network."""   
    
    def __init__(self,observation = {'ratio':1.0},name='No change of 30Hz power to 30Hz drive'):
	sciunit.Test.__init__(self,observation,name) # Call the base constructor.  
	self.required_capabilities = (ProduceXY,) 

    score_type = BooleanScore # This test's 'judge' method will return a BooleanScore.  
    
    def generate_prediction(self, model):
        [control3030,schiz3030] = model.produce_XY(30.0,30.0) # The model has this method if it inherits from the 'Produce4040' capability.
	return [control3030,schiz3030]    

    def compute_score(self, observation, prediction):
	epsilon = 0.1
	if prediction[0]>0.0:
		result = {'ratio': prediction[1]/prediction[0]}
        score = self.score_type((abs(result['ratio'] - observation['ratio'])<epsilon)) # Returns a BooleanScore. 
        score.description = 'Passing score if the prediction equals the observation (witin a given range)'
        return score
