import pickle

__author__ = 'Pranay'
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import csv
import operator
import random
import numpy,sys
from get_probs import get_probs
sys.path.append('../Utilities')
from constants import test_size, categories, performance_metric_keys
import string
from nltk.corpus import stopwords
print 'import once feature ex'


difficulty = {'A': 1, 'C': 3, 'B': 2, 'E': 5, 'D': 4, 'G': 7, 'F': 6, 'I': 9,
 'H': 8, 'K': 11, 'J': 10, 'M': 13, 'L': 12, 'O': 15, 'N': 14, 'Q': 17,
 'P': 16, 'S': 19, 'R': 18, 'U': 21, 'T': 20, 'V': 22}
if __name__ == "__main__":
    probs = get_probs()

    random.shuffle(probs)

    train_set = tuple([prob.description for prob in probs[:-int(test_size*len(probs))] ])
    for category in categories:

        #test_set = tuple([prob.description for prob in probs[-int(test_size*len(probs)):] ])
        otherFeatures = []

        for prob in probs:
            features = []
            if 'sec' in prob.time_limit:
                prob.time_limit = prob.time_limit[0:(prob.time_limit.index('sec'))-1]
            features += [1.0 if 'True' in prob.example_given else 0.0 , difficulty[prob.difficulty] ,
             float(prob.time_limit), 1.0 if category in prob.category else 0.0]
            otherFeatures.append(features)

        # print otherFeatures
        print category+':'
        print 'Test Size: '+str((test_size))
        print 'Total: '+str((len(probs)))
        print 'Train Set Length: '+str(len(train_set))

        count_vectorizer = CountVectorizer()
        count_vectorizer.fit_transform(train_set)
        with open('data/countVectorizer_'+category+'.pickle', 'w+b') as f:
            pickle.dump(count_vectorizer, f)
        freq_term_matrix = count_vectorizer.transform(train_set)

        tfidf = TfidfTransformer(norm="l2")
        tfidf.fit(freq_term_matrix)
        with open('data/TfidfTransformer_'+category+'.pickle', 'w+b') as f:
            pickle.dump(tfidf, f)

        tf_idf_matrix = tfidf.transform(freq_term_matrix)
        numpyAr = tf_idf_matrix.toarray()
        print 'Feature Size: '+ str(len(numpyAr[0])+len(otherFeatures[0]))

        with open('data/'+category+'_training.csv', 'w') as f:
            writer = csv.writer(f)
            i = 0
            for row in numpyAr:
                writer.writerow(list(row) + (otherFeatures[i]))
                # print len(list(row) + (otherFeatures[i]))
                i += 1
        #getFeaturesByProbCode('AVGSHORT')

def getFeaturesByProb(prob):
    print 'Requested problem '+ prob.name
    printable = set(string.printable)
    prob.description = filter(lambda x: x in printable, prob.description)
    desc = prob.description
    desc = desc.replace('.', ' ')
    desc = desc.replace(',', ' ')
    desc = create_word_features(desc)
    prob.description = desc.lower()
    prob.difficulty = 'medium'
    # prob = getProbByCode(probCode)
    # print 'Got problem '+prob.prob_code
    features = []
    if '-' in prob.time_limit:
        j = prob.time_limit.index('-')
        prob.time_limit = prob.time_limit[j + 1:]
    features += [float(prob.submission_size), 1.0 if 'True' in str(prob.example_given) else 0.0 , difficulty[prob.difficulty] ,float(prob.time_limit)]
    with open('countVectorizer.pickle','r+b') as f:
        count_vectorizer = pickle.load(f)
    with open('TfidfTransformer.pickle','r+b') as f:
        tfidf = pickle.load(f)
    freq_term_matrix = count_vectorizer.transform([prob.description])
    # print(features)
    tf_idf_matrix = tfidf.transform(freq_term_matrix)
    numpyAr = tf_idf_matrix.toarray()
    print 'LEN :'+ str(len(list(numpyAr[0]) + features))
    return list(numpyAr[0]) + features

def create_word_features(words):
    # print words
    w = []
    for wrd in words.split():
        w.append(wrd)
    useful_words = [word for word in w if word not in
                       stopwords.words('english')]
    my_dict = ' '.join([word for word in useful_words])
    # print my_dict
    return my_dict