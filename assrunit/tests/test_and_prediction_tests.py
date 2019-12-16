import sciunit

from sciunit.scores import (
    BooleanScore,
    RatioScore,
)  # Two of several SciUnit score types.
from assrunit.capabilities import ProduceXY


### The test classes ###


# 40Hz/40Hz
class Test4040(sciunit.Test):
    """Tests if the model predicts the reduction of 40Hz power in the 
    'schizophrenia-like' network compared to the control network."""

    def __init__(
        self, observation={"ratio": 0.4}, name="Reduction of 40Hz power to 40Hz drive"
    ):
        # Call the base constructor.
        sciunit.Test.__init__(self, observation, name)
        self.required_capabilities = (ProduceXY,)

    # This test's 'judge' method will return a BooleanScore.
    score_type = BooleanScore

    def generate_prediction(self, model):
        [control4040, schiz4040] = model.produce_XY(
            40.0, 40.0
        )  # The model has this method if it inherits from the 'ProduceXY' capability.
        return [control4040, schiz4040]

    def compute_score(self, observation, prediction):
        if prediction[0] > 0.0:
            result = {"ratio": prediction[1] / prediction[0]}
        score = self.score_type(
            result["ratio"] < observation["ratio"]
        )  # Returns a BooleanScore.
        score.description = (
            "Passing score if the prediction is smaller than the observation"
        )
        return score


# 30Hz/30Hz
class Test3030(sciunit.Test):
    """Tests if the model predicts the unchanged 30Hz power in the 
    'schizophrenia-like' network compared to the control network."""

    def __init__(
        self, observation={"ratio": 1.0}, name="No change of 30Hz power to 30Hz drive"
    ):
        # Call the base constructor.
        sciunit.Test.__init__(self, observation, name)
        self.required_capabilities = (ProduceXY,)

    # This test's 'judge' method will return a BooleanScore.
    score_type = BooleanScore

    def generate_prediction(self, model):
        [control3030, schiz3030] = model.produce_XY(
            30.0, 30.0
        )  # The model has this method if it inherits from the 'ProduceXY' capability.
        return [control3030, schiz3030]

    def compute_score(self, observation, prediction):
        epsilon = 0.1
        if prediction[0] > 0.0:
            result = {"ratio": prediction[1] / prediction[0]}
        score = self.score_type(
            (abs(result["ratio"] - observation["ratio"]) < epsilon)
        )  # Returns a BooleanScore.
        score.description = "Passing score if the prediction equals the observation (witin a given range)"
        return score


# 20Hz/20Hz
class Test2020(sciunit.Test):
    """Tests if the model predicts the increase in 20Hz power in the 
    'schizophrenia-like' network compared to the control network."""

    def __init__(
        self, observation={"ratio": 1.4}, name="Increase of 20Hz power to 20Hz drive"
    ):
        # Call the base constructor.
        sciunit.Test.__init__(self, observation, name)
        self.required_capabilities = (ProduceXY,)

    # This test's 'judge' method will return a BooleanScore.
    score_type = BooleanScore

    def generate_prediction(self, model):
        [control2020, schiz2020] = model.produce_XY(
            20.0, 20.0
        )  # The model has this method if it inherits from the 'ProduceXY' capability.
        return [control2020, schiz2020]

    def compute_score(self, observation, prediction):
        if prediction[0] > 0.0:
            result = {"ratio": prediction[1] / prediction[0]}
        score = self.score_type(
            result["ratio"] > observation["ratio"]
        )  # Returns a BooleanScore.
        score.description = (
            "Passing score if the prediction is larger than the observation"
        )
        return score


# 20Hz/40Hz
class Test2040(sciunit.Test):
    """Tests if the model predicts the increase in 20Hz power at 40Hz drive in the 
    'schizophrenia-like' network compared to the control network."""

    def __init__(
        self, observation={"ratio": 1.4}, name="Increase of 20Hz power to 40Hz drive"
    ):
        # Call the base constructor.
        sciunit.Test.__init__(self, observation, name)
        self.required_capabilities = (ProduceXY,)

    # This test's 'judge' method will return a BooleanScore.
    score_type = BooleanScore

    def generate_prediction(self, model):
        [control2040, schiz2040] = model.produce_XY(
            20.0, 40.0
        )  # The model has this method if it inherits from the 'ProduceXY' capability.
        return [control2040, schiz2040]

    def compute_score(self, observation, prediction):
        if prediction[0] > 0.0:
            result = {"ratio": prediction[1] / prediction[0]}
        score = self.score_type(
            result["ratio"] > observation["ratio"]
        )  # Returns a BooleanScore.
        score.description = (
            "Passing score if the prediction is larger than the observation"
        )
        return score


# 40Hz/20Hz
class Test4020(sciunit.Test):
    """Tests if the model predicts the decrease in 40Hz power at 20Hz drive in the 
    'schizophrenia-like' network compared to the control network."""

    def __init__(
        self, observation={"ratio": 1.4}, name="Decrease of 40Hz power to 20Hz drive"
    ):
        # Call the base constructor.
        sciunit.Test.__init__(self, observation, name)
        self.required_capabilities = (ProduceXY,)

    # This test's 'judge' method will return a BooleanScore.
    score_type = BooleanScore

    def generate_prediction(self, model):
        [control4020, schiz4020] = model.produce_XY(
            40.0, 20.0
        )  # The model has this method if it inherits from the 'ProduceXY' capability.
        return [control4020, schiz4020]

    def compute_score(self, observation, prediction):
        if prediction[0] > 0.0:
            result = {"ratio": prediction[1] / prediction[0]}
        score = self.score_type(
            result["ratio"] > observation["ratio"]
        )  # Returns a BooleanScore.
        score.description = (
            "Passing score if the prediction is larger than the observation"
        )
        return score


# 10Hz/10Hz - Prediction test
class PredictionTest1010(sciunit.Test):
    """Tests the model response at the 10Hz power band at 10Hz drive in the 
    'schizophrenia-like' condition compared to the control condition."""

    def __init__(
        self, observation={"ratio": 1.4}, name="Prediction: 10Hz power to 10Hz drive"
    ):
        # Call the base constructor.
        sciunit.Test.__init__(self, observation, name)
        self.required_capabilities = (ProduceXY,)

    score_type = RatioScore

    def generate_prediction(self, model):
        [control1010, schiz1010] = model.produce_XY(
            10.0, 10.0
        )  # The model has this method if it inherits from the 'ProduceXY' capability.
        return [control1010, schiz1010]

    def compute_score(self, observation, prediction):
        if prediction[0] > 0.0:
            result = {"ratio": prediction[1] / prediction[0]}
        score = self.score_type(result["ratio"] / observation["ratio"])
        score.description = "Prediction: Score reflects the ratio between power in the control and schizo-like network."
        return score
