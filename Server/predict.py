import sys, os
sys.path.append("../Model Training/Codechef")
import pickle
from sklearn import neighbors, svm
import numpy as np
import pandas
from feature_extraction import getFeaturesByProbCode

def predict(problem):
	with open('../Model Training/Codechef/classifier.pickle', 'rb') as f:
		try:
			clf = pickle.load(f)
			print 'Classifier Loaded'
			features = getFeaturesByProbCode(problem)
			print clf.predict(features)
		except Exception as e:
			print(e)


