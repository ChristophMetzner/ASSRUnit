import os
from peewee import SqliteDatabase, Model, AutoField, FloatField, TextField, IntegerField, ForeignKeyField
from assrunit.constants import DATA_PATH

db = SqliteDatabase(os.path.join(DATA_PATH, 'ASSRUnit.db'))


class Disorders(Model):
    ID = AutoField()
    name = TextField()
    abbreviation = TextField()

    class Meta:
        database = db
        table_name = "disorders"


class Studies(Model):
    ID = AutoField()
    title = TextField()
    authors = TextField()
    journal = TextField()
    year = IntegerField()
    comments = TextField()
    paradigm = TextField()

    class Meta:
        database = db
        table_name = "studies"


class StudiesMeasurements(Model):
    ID = AutoField()
    study_id = ForeignKeyField(Studies)
    value = TextField()
    location = TextField()
    modality = TextField()
    processing = TextField()

    class Meta:
        database = db
        table_name = "studies_measurements"


class StudiesExperiments(Model):
    ID = AutoField()
    study_id = ForeignKeyField(Studies)
    power = IntegerField()
    drive = IntegerField()
    disorder_id = ForeignKeyField(Disorders)
    value = FloatField()
    hedges_g = FloatField()
    SE = FloatField()
    p_value = TextField()

    class Meta:
        database = db
        table_name = "studies_experiments"


class SubjectsGroups(Model):
    ID = AutoField()
    study_id = ForeignKeyField(Studies)
    count = IntegerField()
    sex = TextField()
    mean_age = FloatField()
    disorder_id = ForeignKeyField(Disorders)
    mean_illness_duration = FloatField()
    medication_status = TextField()
    illness_type = TextField()

    class Meta:
        database = db
        table_name = "subjects_groups"


class Subjects(Model):
    ID = AutoField()
    subject_group = ForeignKeyField(SubjectsGroups)
    sex = TextField()
    age = FloatField()

    class Meta:
        database = db
        table_name = "subjects"


class Models(Model):
    ID = AutoField()
    name = TextField()

    class Meta:
        database = db
        table_name = "models"


class ModelsPredictions(Model):
    ID = AutoField()
    model_id = ForeignKeyField(Models)
    power = IntegerField()
    drive = IntegerField()
    score_ratio = FloatField()
    description = TextField()

    class Meta:
        database = db
        table_name = "models_predictions"
