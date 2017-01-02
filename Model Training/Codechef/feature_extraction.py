__author__ = 'Pranay'
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import csv
import operator
import random
import numpy
from get_probs import get_probs, getProbByCode
from training_params import categories, test_size

probs = get_probs()
prob_class = 'dp'

random.shuffle(probs)

train_set = tuple([prob.description for prob in probs[:-int(test_size*len(probs))] ])
#test_set = tuple([prob.description for prob in probs[-int(test_size*len(probs)):] ])


otherFeatures = []
difficulty = {'easy': 1, 'medium': 2, 'hard':3, 'school':4, 'challenge':5}
for prob in probs:
	features = []
	if '-' in prob.time_limit:
		j = prob.time_limit.index('-')
		prob.time_limit = prob.time_limit[j + 1:]
	features += [float(prob.submission_size), 1.0 if 'True' in prob.example_given else 0.0 , difficulty[prob.difficulty] ,
	 float(prob.time_limit), float(categories.index(prob.category))]
	otherFeatures.append(features)	

print otherFeatures

count_vectorizer = CountVectorizer()
count_vectorizer.fit_transform(train_set)
freq_term_matrix = count_vectorizer.transform(train_set)

tfidf = TfidfTransformer(norm="l2")
tfidf.fit(freq_term_matrix)
tf_idf_matrix = tfidf.transform(freq_term_matrix)
numpyAr = tf_idf_matrix.toarray()


with open('words.csv', 'w') as f:
	writer = csv.writer(f)
	i = 0
	for row in numpyAr:
		writer.writerow(list(row) + (otherFeatures[i]))
		i += 1
#getFeaturesByProbCode('AVGSHORT')

def getFeaturesByProbCode(prob):
	print 'Requested problem '+ prob.name
	# prob = getProbByCode(probCode)
	# print 'Got problem '+prob.prob_code
	features = []
	if '-' in prob.time_limit:
		j = prob.time_limit.index('-')
		prob.time_limit = prob.time_limit[j + 1:]
	features += [float(prob.submission_size), 1.0 if 'True' in prob.example_given else 0.0 , difficulty[prob.difficulty] ,float(prob.time_limit)]
	freq_term_matrix = count_vectorizer.transform([prob.description])
	# print(freq_term_matrix)
	tf_idf_matrix = tfidf.transform(freq_term_matrix)
	numpyAr = tf_idf_matrix.toarray()
	print numpyAr[0]
	return list(numpyAr[0]) + features