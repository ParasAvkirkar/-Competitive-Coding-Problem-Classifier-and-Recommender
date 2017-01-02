import sys, os
sys.path.append("../Model Training/Codechef")
import pickle
from sklearn import neighbors, svm
import numpy as np
import pandas
from get_probs import get_probs, getProbByCode

with open('classifier.pickle', 'rb') as f:
	try:
		clf = pickle.load(f)

	except Exception as e:
		print(e)


