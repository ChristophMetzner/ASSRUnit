import pickle
import os.path


def saveObj(obj, name):
    with open(name + ".pkl", "wb") as f:
        pickle.dump(obj, f, protocol=2)


def loadObj(name):
    with open(name + ".pkl", "rb") as f:
        return pickle.load(f)


def addPrediction(score, measure, model, name, dbname):
    # create dictionary
    entry = {name: {"Model": model, "Measure": measure, "Result score": score}}
    database = entry
    # if database exists, load it and add prediction
    if os.path.exists(dbname + ".pkl"):
        print "updating database"
        database = loadObj(dbname)
        database.update(entry)
    # if it doesn't exist, just save the newly created dictionary
    saveObj(database, dbname)
