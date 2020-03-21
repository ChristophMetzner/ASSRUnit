from assrunit.models import VierlingSimpleModel
from assrunit.tests.test_and_prediction_tests import PredictionTest1010
from assrunit.prediction_database_functions import add_prediction


# model parameters
controlparams_model = {
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
schizparams_model = {
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

# Create model instance
model = VierlingSimpleModel(controlparams_model, schizparams_model)

# Create test instance
prediction_test_1010 = PredictionTest1010()

# Run and judge model
score = prediction_test_1010.judge(model)

# Save to DB
add_prediction(model_name=model.name, power=10, drive=10, score=score, description=prediction_test_1010.name)
