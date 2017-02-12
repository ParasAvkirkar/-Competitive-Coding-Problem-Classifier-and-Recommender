import sys
sys.path.append('../Utilities/')
sys.path.append('../../Data Transformation/codechef_problem/')
sys.path.append('../Data Transformation/codechef_problem/')
import pickle, operator
from constants import categories
import transform_description

test_example = [1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0]

def createFeaturesForProbByCategory(prob, category):
	description = transform_description.transform(prob.description)
	filePath = '../Model Training/Codechef Model 1/data/'+category+'/'
	features = []
	with open(filePath+'dataset.csv') as f:
		featureWords = f.readline().split(',')[0:20]
		for word in featureWords:
			if description.count(word)>0:
				features.append(1)
			else:
				features.append(0)
		# append other features
		# features.append(prob.submission_size)
		# features.append(float(prob.time_limit))
	return features

def predict_top3_categories(prob):
	category_models = {}
	features = {}
	for c in categories:
		with open('../Model Training/Codechef Model 1/model/' + c, 'r') as f:
			category_models[c] = pickle.load(f)
			print 'Model Loaded'
			features[c] = createFeaturesForProbByCategory(prob, c)
			print 'Features created from problem data'

	category_perc = {}

	for category in category_models:
		print 'Features for '+category
		print str(len(features[category]))
		print 'Training length: '+str(len(test_example))
		current_prediction = category_models[category].predict_proba(features[category])
		category_perc[category] = current_prediction[0][1]
		# print cm + " " + str(category_perc)

	top_categories = sorted(category_perc.items(), key=operator.itemgetter(1))
	top_categories.reverse()

	# for key, value in top_categories[:3]:
	# 	print key + " " + str(value)
	print 'Predicted '
	return top_categories[:3]



if __name__ == "__main__":
	pass
	# print predict_top3_categories(test_example)