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
        mlAlgo = KMeans(n_clusters = 7, random_state = 0)

    mlAlgo = mlAlgo.fit(users_X)
    return mlAlgo


def build_recommendation_list_for_users(usersClusterMap, probs):
    probDict = {}
    for prob in probs:
        probDict[prob.prob_code] = prob

    for label in usersClusterMap:
        userList = usersClusterMap[label]
        for user in userList:
            user.calculate_user_level()
            print(user.uname + ' ' + str(len(user.failed_probs)) + ' ' + str(len(user.solved_probs)))
            if len(user.failed_probs) == 0 and len(user.solved_probs) > 0:
                print(user.uname + ' Level: ' + str(user.user_level))

        userList.sort(key = lambda x: x.user_level, reverse = True)
        # print(userList)

    for label in usersClusterMap:
        userList = usersClusterMap[label]

        probsSolvedUntilCurrentLevelUser = []
        generalUsersStartIndex = int(len(userList) * 0.1) + 1
        for i in range(len(userList)):
            tempDict = {}
            if i >= generalUsersStartIndex:
                for probCode in probsSolvedUntilCurrentLevelUser:
                    if probCode not in userList[i].solved_probs:
                        tempDict[probCode] = probDict[probCode].get_problem_level()

                        tempDict = dict(sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True))
                # print(str(tempDict))
            for probCode in tempDict:
                userList[i].recommendation_list.append(probCode)
            # print(str(userList[i].recommendation_list))

            for probCode in userList[i].solved_probs:
                probsSolvedUntilCurrentLevelUser.append(probCode)

        usersClusterMap[label] = userList
        return usersClusterMap

def process_users(uniqueFileConvention, users, probs, platform=PlatformType.Codechef,
                  clusteringMethod=ClusterMethod.KMeans, test_size=0.2):
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

    usersClusterMap = build_recommendation_list_for_users(usersClusterMap, probs)
    usersToBeWrittenOnPickle = []
    for label in usersClusterMap:
        usersList = usersClusterMap[label]
        usersToBeWrittenOnPickle = usersToBeWrittenOnPickle + usersList

    with open(uniqueFileConvention + '_orm.pickle', 'wb') as f:
        print('Dumping ' + uniqueFileConvention + '_orm.pickle')
        pickle.dump(usersToBeWrittenOnPickle, f)
