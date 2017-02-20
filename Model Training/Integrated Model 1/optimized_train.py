from sklearn import neighbors, svm
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
import pandas
import sys, pickle
from generate_dataset import generate
from train import train_for_category
sys.path.append('../Utilities')
from constants import categories, performance_metric_keys


def train_with_optimized_feature_size(category, classifier):

    clfs_with_score = {}
    
    for i in range(10, 14):

        with open('num_of_top_words_as_feature.pickle', 'w+b') as f:
            num_of_top_words_as_feature = i
            pickle.dump(num_of_top_words_as_feature, f)

        generate(category)
        f1_score, cm, clf = train_for_category(category, classifier)
        clfs_with_score[i] = f1_score

    max_score = 0
    best_feature_size = 10
    clf = None
    
    for i in clfs_with_score:
        if max_score < clfs_with_score[i]:
            print i
            best_feature_size = i
            max_score = clfs_with_score[i]

    print category + " " + str(max_score) + " " + str(best_feature_size)

    with open('num_of_top_words_as_feature.pickle', 'w+b') as f:
        pickle.dump(best_feature_size, f)

    #trained again so that all csv files are updated for correct feature size
    generate(category)
    f1_score, cm, clf = train_for_category(category, classifier)
    print f1_score

    with open('model/' + category, 'w+b') as f:
        pickle.dump(clf, f)

    with open('data/' + category + '/feature_size.pickle', 'w') as f:
        pickle.dump(best_feature_size, f)

    return clf, max_score



if __name__ == '__main__':

    for c in categories:
        train_with_optimized_feature_size(c, 'KNN')
    # generate('greedy')
    # train_for_category('greedy', 'KNN')
