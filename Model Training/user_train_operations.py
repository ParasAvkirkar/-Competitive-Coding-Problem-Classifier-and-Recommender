from sklearn.cluster import KMeans
from sklearn.metrics import precision_recall_fscore_support
# from sklearn.exceptions import ConvergenceWarning
import numpy as np
import pandas
import sys
import os
import pickle
import operator
import warnings
from generate_problems_dataset import generate, generateLazyLoad

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn')

from constants import categories, performance_metric_keys, ClusterMethod, \
    PlatformType, Metrics, defaultTestSize

def build_user_clusters(users_X, clusteringMethod=ClusterMethod.KMeans):

    mlAlgo = None
    if clusteringMethod == ClusterMethod.KMeans:
        mlAlgo = KMeans(n_clusters=7, random_state=0)

    mlAlgo = mlAlgo.fit(users_X)
    return mlAlgo

def build_recommendation_list_for_users(usersClusterMap):
   for label in usersClusterMap:
       userList = usersClusterMap[label]
       for user in userList:
           user.calculate_user_level()
           print(user.uname + ' ' + str(len(user.failed_probs)) + ' ' + str(len(user.solved_probs)))
           if len(user.failed_probs) == 0 and len(user.solved_probs) > 0:
               # for category in user.categoryDifficultyMap:
               #     for level in user.categoryDifficultyMap[category]:
               #          pass
               print(user.uname + ' Level: ' + str(user.user_level))
       userList.sort(key=lambda x: x.user_level, reverse=True)

       #print(str(userList))
       usersClusterMap[label] = userList

def process_users(uniqueFileConvention, users, platform=PlatformType.Codechef, clusteringMethod=ClusterMethod.KMeans, test_size=0.2):
    df = pandas.read_csv(uniqueFileConvention + '_dataset.csv')
    X = np.array(df.drop(['uname'], 1)).astype(float)
    print(X.shape)

    usersDict = {}
    for user in users:
        usersDict[user.uname] = user

    X_train = X[:-int(len(X) * test_size)]
    trainedModel = build_user_clusters(X_train, clusteringMethod)
    X_train_labels = trainedModel.labels_
    print(X_train_labels)

    usersClusterMap = {}
    index = 0
    for label in X_train_labels:
        if label not in usersClusterMap:
            usersClusterMap[label] = [users[index]]
        else:
            userList = usersClusterMap[label]
            userList.append(users[index])
            usersClusterMap[label] = userList
        index += 1

    build_recommendation_list_for_users(usersClusterMap)




