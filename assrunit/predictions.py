from models import VierlingSimpleModel
from tests.tests import PredictionTest1010
from prediction import addPrediction


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

# create model instance
model = VierlingSimpleModel(controlparams_model, schizparams_model)

# create test instance
prediction_test_1010 = PredictionTest1010()

# run and judge model
score = prediction_test_1010.judge(model)

# add prediction to database
measure = prediction_test_1010.name
model = model.name
name = "VierlingSimpleModel-1010"
dbname = "ASSR_schizophrenia_prediction_database"
addPrediction(score, measure, model, name, dbname)
