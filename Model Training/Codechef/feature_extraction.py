__author__ = 'Pranay'
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import csv
import operator
import random
import numpy
from get_probs import get_probs, getProbByCode
from training_params import categories, test_size
#import StringIO


probs = get_probs()

print(len(probs))
newProbs = []
# for prob in probs:
# 	#print str(prob.description)
# 	#prob.description = StringIO.StringIO(prob.description)
# 	#]prob.description = unicode(prob.description, 'utf-8')
# 	prob.description = unicode(prob.description, errors='ignore')
# 	print(str(prob.description))
# 	newProbs.append(prob)
# probs = newProbs


#prob_class = 'dp'
random.shuffle(probs)

train_set = tuple([str(prob.description) for prob in probs])
train_set = tuple([str(prob.description) for prob in probs[:-int(test_size*len(probs))] ])
test_set = tuple([prob.description for prob in probs[-int(test_size*len(probs)):] ])

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

# print features
# print('hello')
# print otherFeatures

numpy.set_printoptions(threshold='nan')

count_vectorizer = CountVectorizer(decode_error='ignore')
count_vectorizer.fit_transform(train_set)
freq_term_matrix = count_vectorizer.transform(train_set)

#print(freq_term_matrix.toarray())

tfidf = TfidfTransformer(norm="l2")
tfidf.fit(freq_term_matrix)
tf_idf_matrix = tfidf.transform(freq_term_matrix)
numpyAr = tf_idf_matrix.toarray()

#print(tf_idf_matrix.toarray())

with open('words.csv', 'w') as f:
	writer = csv.writer(f)
	i = 0
	for row in numpyAr:
		writer.writerow(list(row) + (otherFeatures[i]))
		i += 1
#getFeaturesByProbCode('AVGSHORT')

def getFeaturesByProbCode(prob):
	print('Requested problem '+ prob.name)
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
	print(numpyAr[0])
	return list(numpyAr[0]) + features