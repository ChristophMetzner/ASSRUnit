from assrunit.db import Models, ModelsPredictions


def add_prediction(model_name, power, drive, score, description):

    ratio = str(score).split('=')[1]
    model_id = Models.select().where(Models.name.contains(model_name))

    query = ModelsPredictions.insert(model_id=model_id, power=power, drive=drive, score_ratio=ratio, description=description)
    query.execute()
