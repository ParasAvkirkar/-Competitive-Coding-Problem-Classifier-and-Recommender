__author__ = 'Pranay'
from sklearn.feature_extraction.text import CountVectorizer
import operator
import random
from get_probs import get_probs

probs = get_probs()
prob_class = 'dp'

random.shuffle(probs)

test_size = 0.2
train_set = tuple([prob.description for prob in probs[:-int(test_size*len(probs))] ])
test_set = tuple([prob.description for prob in probs[-int(test_size*len(probs)):] ])

count_vectorizer = CountVectorizer()
count_vectorizer.fit_transform(train_set)
print "Vocabulary:", count_vectorizer.vocabulary

