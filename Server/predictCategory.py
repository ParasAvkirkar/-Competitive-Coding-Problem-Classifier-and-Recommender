import sys, os
# sys.path.append("../Model Training/Codechef")
sys.path.append("../Model Training/CodeChef Model1")
import pickle
from sklearn import neighbors, svm
import numpy as np
import pandas
import predict
import training_params

def predict(problem):
	with open('../Model Training/Codechef/classifier.pickle', 'rb') as f:
		try:
			clf = pickle.load(f)
			print 'Classifier Loaded'
			features = predict.predict(problem)
			# print features
			# return training_params.categories[int(clf.predict(np.array(features).reshape((1, len(features))))[0])]
			print clf.predict_proba(np.array(features).reshape((1, len(features))))[0]
			probs = clf.predict_proba(np.array(features).reshape((1, len(features))))[0]
			prediction = ''
			for i in range(len(probs)):
				prediction += training_params.categories[i]+': '+str(int(probs[i]*100))+'%\n'
			return prediction
		except Exception as e:
			print(e)
			return 'failed'


