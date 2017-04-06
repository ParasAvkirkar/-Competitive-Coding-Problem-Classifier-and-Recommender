from sklearn.cluster import KMeans
from sklearn.metrics import precision_recall_fscore_support
# from sklearn.exceptions import ConvergenceWarning
import numpy as np
import pandas
import sys
import csv
import pickle
import operator
import time
import warnings
import matplotlib.pyplot as plt
from recommend import build_recommendation_list_for_users
from scipy.stats import mode
from generate_problems_dataset import generate, generateLazyLoad
from generate_users_dataset import generateLazyLoad, generateLazyLoadAll
from datetime import datetime
from get_probs import get_all_probs_without_category_NA, get_probCodeToObjectMap, get_probCodeToDiff_Map
from gensim.models import Word2Vec
from get_users import get_codechef_users
from sorting import sort_by_date_difficulty

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn')

from constants import categories, performance_metric_keys, ClusterMethod, \
    PlatformType, Metrics, defaultTestSize, codechefDifficultyLevels

categorywise_difficulty_limits = None
from user_level_limits import get_categorywise_difficulty_limits, get_difficulty_limits_without_category

def build_user_clusters(users_X, clusteringMethod=ClusterMethod.KMeans):
    mlAlgo = None
    if clusteringMethod == ClusterMethod.KMeans:
        mlAlgo = KMeans(n_clusters = 7, random_state = 0)

    trained_model = mlAlgo.fit(users_X)
    return trained_model


def process_users(uniqueFileConvention, userNameToObjects, probCodeToObjects, platform=PlatformType.Codechef,
                  clusteringMethod=ClusterMethod.KMeans, test_size=0.2):
    dataFileConvention = uniqueFileConvention + '_' + ClusterMethod.clusterMethodString[clusteringMethod]
    df = pandas.read_csv(uniqueFileConvention + '_dataset.csv')
    X = np.array(df.drop(['uname'], 1)).astype(float)
    X_usernames = list(df['uname'])
    print('printing usernames')
    print(X_usernames)
    print(X.shape)

    X_train = X[:-int(len(X) * test_size)]
    trainedModel = build_user_clusters(X_train, clusteringMethod)
    X_train_labels = trainedModel.labels_
    print(X_train_labels)

    usersClusterMap = {}
    index = 0
    for label in X_train_labels:
        if label not in usersClusterMap:
            usersClusterMap[label] = [userNameToObjects[X_usernames[index]]]
        else:
            userList = usersClusterMap[label]
            userList.append(userNameToObjects[X_usernames[index]])
            usersClusterMap[label] = userList
        index += 1

        usersClusterMap = build_recommendation_list_for_users(usersClusterMap, probCodeToObjects)
        usersToBeWrittenOnPickle = []
        for label in usersClusterMap:
            usersList = usersClusterMap[label]
            usersToBeWrittenOnPickle = usersToBeWrittenOnPickle + usersList

        with open(dataFileConvention + '_orm.pickle', 'wb') as f:
            print('Dumping ' + uniqueFileConvention + '_orm.pickle')
            pickle.dump(usersToBeWrittenOnPickle, f)


def train_word2vec(uniqueFileConvention, platform, probs_all_or_categorywise):
    if probs_all_or_categorywise == 1:
        userNameToObjects = generateLazyLoad(uniqueFileConvention, platform)
    else:
        userNameToObjects = generateLazyLoadAll(uniqueFileConvention, platform)
    sentences = []

    for user in userNameToObjects:
        submissionsDict = userNameToObjects[user].problemMappings

        sorted_submissions = sort_by_date_difficulty(submissionsDict)

        submission_sentence = []

        [submission_sentence.append(row[0]) for row in sorted_submissions]
        sentences.append(submission_sentence)

    print ("Sentences done")
    print ("Started training Word2Vec model")
    start = time.time()
    model = Word2Vec(sentences, size=50, window=5, workers=2, min_count=1, iter=25, negative=15, sg=1)
    end = time.time()
    print ("Finished training Word2Vec model")

    model.save(uniqueFileConvention)
