import sys
sys.path.append('../Utilities/')

import pickle, operator
from constants import categories

test_example = [1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0]

def predict_top3_categories(test_example):
	category_models = {}
	for c in categories:
		with open('model/' + c, 'r') as f:
			category_models[c] = pickle.load(f)


	category_perc = {}

	for category in category_models:
		current_prediction = category_models[category].predict_proba(test_example)
		category_perc[category] = current_prediction[0][1]
		# print cm + " " + str(category_perc)

	top_categories = sorted(category_perc.items(), key=operator.itemgetter(1))
	top_categories.reverse()

	# for key, value in top_categories[:3]:
	# 	print key + " " + str(value)

	return top_categories[:3]



if __name__ == "__main__":
	print predict_top3_categories(test_example)