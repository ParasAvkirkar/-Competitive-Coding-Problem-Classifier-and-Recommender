import sys, os

# sys.path.append("../Model Training/CodeChef Model 1")
sys.path.append("../Model Training/Integrated Model 1/")
sys.path.append("../Model Training/Utilities/")
import pickle
from sklearn import neighbors, svm
import numpy as np
import pandas
import predict
import constants


def predict_category(problem):
    try:
        result = predict.predict_top3_categories(problem)
        print result
        return result
    except Exception as e:
        print e
        return 'failed'
