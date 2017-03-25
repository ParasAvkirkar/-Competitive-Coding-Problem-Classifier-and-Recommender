import sys
import numpy as np

sys.path.append('../Utilities/')
sys.path.append('../../Data Transformation/codechef_problem/')
sys.path.append('../Data Transformation/codechef_problem/')
import pickle, operator
from constants import categories
import transform_description

test_example = [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]


def createFeaturesForProbByCategory(prob, category):
    description = transform_description.transform(prob.description)
    filePath = '../Model Training/Integrated Model 1/data/' + category + '/'
    # filePath = 'data/'+category+'/'
    features = []
    with open(filePath + 'dataset.csv') as f:

        with open(filePath + 'feature_size.pickle') as fs:
            feature_size = pickle.load(fs)
            print ('\n\n\n\tfeature size for ' + str(category) + ' : ' + str(feature_size))

        # try:
        # 	with open(filePath + 'feature_size.pickle') as fs:
        # 		feature_size = pickle.load(fs)
        # 		print ('feature size for ' + category + ' : ' + feature_size)
        # except:
        # 	feature_size = 10

        featureWords = f.readline().split(',')[0: -3]
        for word in featureWords:
            if description.count(word) > 0:
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
        with open('../Model Training/Integrated Model 1/model/' + c) as f:
            # with open('model/' + c, 'r') as f:
            category_models[c] = pickle.load(f)
            print 'Model Loaded'
            features[c] = createFeaturesForProbByCategory(prob, c)
            features[c] = np.array(features[c])
            print 'Features created from problem data ' + str(len(features[c]))

    category_perc = {}

    for category in category_models:
        print 'Features for ' + category
        print str(len(features[category]))
        print 'Training length: ' + str(len(test_example))
        current_prediction = category_models[category].predict_proba(features[category].reshape(1, -1))
        category_perc[category] = current_prediction[0][1]
    # print cm + " " + str(category_perc)

    top_categories = sorted(category_perc.items(), key = operator.itemgetter(1))
    top_categories.reverse()

    # for key, value in top_categories[:3]:
    # 	print key + " " + str(value)
    print 'Predicted '
    return top_categories[:3]


if __name__ == "__main__":
    # pass
    # prob = 'There are N servers which you have to place in N slots. Slots and servers are numbered from 1 to N. A distance between slots i and j is |i - j|. There are M pairs of servers that should be connected by wire. You are to place all the servers in the slots so the total wire length is minimized.'
    # prob = 'Given an array of size n, you have to answer queries of the form : L R k . For each query, you have to find an element which occurs consecutively in the subarray [L,R] more than or equal to k times. k will always be greater than floor((R-L+1)/2). If no such element exists, print -1.'
    print predict_top3_categories(prob)
