import sys
sys.path.append('../Utilities/')

import pickle, operator
from constants import categories

test_example = [1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0]

def createFeaturesForProbByCategory(prob, category):
	description = prob.description
	filePath = 'data/'+category+'/'
	features = []
	with open(filePath+'dataset.csv') as f:
		featureWords = f.readline().split(',')[0:20]
		for word in featureWords:
			features = description.count(word)
		# append other features
		features.append(prob.sub_size)
		features.append(prob.time_limit)
	return features

def predict_top3_categories(prob):
	category_models = {}
	features = {}
	for c in categories:
		with open('model/' + c, 'r') as f:
			category_models[c] = pickle.load(f)
			features[c] = createFeaturesForProbByCategory(prob, c)

	category_perc = {}

	for category in category_models:
		current_prediction = category_models[category].predict_proba(features[category])
		category_perc[category] = current_prediction[0][1]
		# print cm + " " + str(category_perc)

	top_categories = sorted(category_perc.items(), key=operator.itemgetter(1))
	top_categories.reverse()

	# for key, value in top_categories[:3]:
	# 	print key + " " + str(value)

	return top_categories[:3]



if __name__ == "__main__":
	pass
	# print predict_top3_categories(test_example)