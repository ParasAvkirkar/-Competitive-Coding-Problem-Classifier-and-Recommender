from sklearn.cluster import KMeans
from sklearn.metrics import precision_recall_fscore_support
# from sklearn.exceptions import ConvergenceWarning
import numpy as np
import pandas
import sys
import os
import pickle
import operator
import time
import warnings
import matplotlib.pyplot as plt
from scipy.stats import mode
from generate_problems_dataset import generate, generateLazyLoad
from generate_users_dataset import generateLazyLoad
from datetime import datetime

from gensim.models import Word2Vec
from get_users import get_codechef_users
from sorting import sort_by_date_difficulty


sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn')

from constants import categories, performance_metric_keys, ClusterMethod, \
    PlatformType, Metrics, defaultTestSize, codechefDifficultyLevels


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

                        tempDict = dict(sorted(tempDict.items(), key = operator.itemgetter(1), reverse = True))
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
    dataFileConvention = uniqueFileConvention + '_' + PlatformType.platformString[platform] \
                         + '_' + ClusterMethod.clusterMethodString[clusteringMethod]

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

    with open(dataFileConvention + '_orm.pickle', 'wb') as f:
        print('Dumping ' + uniqueFileConvention + '_orm.pickle')
        pickle.dump(usersToBeWrittenOnPickle, f)


# Right now handles codechef, later platform wise changes would be made
def get_categorywise_difficulty_limits(uniqueFileConvention, platform, probCodeToObjects, probCodeToDifficulty,
                                          days_to_consider_pro_user):
    categorywise_difficulty_limits = {}
    categorywise_tipping_points = get_categorywise_tipping_points(uniqueFileConvention, platform, probCodeToObjects, probCodeToDifficulty, days_to_consider_pro_user)
    print('Got categorywise tipping points')
    for cat in categories:
        categorywise_tipping_points[cat][0].sort()
        categorywise_tipping_points[cat][1].sort()
        len0 = len(categorywise_tipping_points[cat][0])
        len1 = len(categorywise_tipping_points[cat][1])
        print(str(len0) + ' ' + str(len1))
        # print('Category: ' + cat + ' Maximum Stats ---> Easy_To_Medium: ' + str(
        #     max(categorywise_tipping_points[cat][0])) + ' Medium_To_Hard: '
        #       + str(max(categorywise_tipping_points[cat][1])))
        # # Currently considering maximum value as tendency of difficulty limits
        # categorywise_difficulty_limits[cat] = (max(categorywise_tipping_points[cat][0]), max(categorywise_tipping_points[cat][1]))
        # print('Category: ' + cat + ' Median Stats ---> Easy_To_Medium: ' + str(
        #     categorywise_tipping_points[cat][0][len0 / 2]) + ' Medium_To_Hard: '
        #       + str(categorywise_tipping_points[cat][1][len1 / 2]))
        # print('Category: ' + cat + ' Easy_To_Medium: ' + str(mode(categorywise_tipping_points[cat][0])) + ' Medium_To_Hard: '
        # + str(mode(categorywise_tipping_points[cat][1])))
        # print('===============')
        plt.plot([i for i in range(len(categorywise_tipping_points[cat][0]))], categorywise_tipping_points[cat][0],
                 'b-')
        plt.plot([i for i in range(len(categorywise_tipping_points[cat][1]))], categorywise_tipping_points[cat][1],
                 'r-')
        plt.xlabel(cat + ' tipping points')
        plt.show()

    return categorywise_difficulty_limits


def get_categorywise_tipping_points(uniqueFileConvention, platform, probCodeToObjects, probCodeToDifficulty,
                                    days_to_consider_pro_user):
    print('Building category wise tipping points')
    users = generateLazyLoad(uniqueFileConvention, platform)
    pro_users = get_pro_users(users, days_to_consider_pro_user)
    print('Got ' + str(len(pro_users)) + ' pro users')

    categorywise_tipping_points = {}
    for cat in categories:
        # easy_to_med = [] med_to_hard = []
        categorywise_tipping_points[cat] = ([], [])

    for user in pro_users:
        list_of_mapping_date = []
        for probCode in user.problemMappings:
            map = user.problemMappings[probCode]
            try:
                list_of_mapping_date.append((map, datetime.strptime(map.date, '%Y-%m-%d %H:%M:%S')))
            except ValueError as v:
                # Ignoring probable absence of datetime value like None
                # print('datetime found was none')
                pass
        # Sorting list of tuples based on date parameter
        list_of_mapping_date = sorted(list_of_mapping_date, key = lambda x: x[1])
        for cat in categories:
            difficultySequence = ''  # categorySolvingSequence = {} # A dictionary category --->
            for tupl in list_of_mapping_date:
                map = tupl[0]
                try:
                    prob = probCodeToObjects[map.prob_code]
                    if cat in prob.category:
                        difficulty = ''
                        if map.prob_code in probCodeToDifficulty:
                            difficulty = probCodeToDifficulty[map.prob_code]
                        elif prob.difficulty in codechefDifficultyLevels:
                            difficulty = prob.difficulty
                        else:
                            # Didn't found difficulty from either prob_diff csv or DB
                            continue
                        difficultySequence = difficultySequence + difficulty[0]
                except KeyError as e:
                    print(str(e))

            easyCount = 0
            mediumCount = 0
            for character in difficultySequence:
                if 'e' in character:
                    easyCount += 1
                    mediumCount = 0
                elif 'm' in character:
                    mediumCount += 1
                    if easyCount > 0:
                        categorywise_tipping_points[cat][0].append(easyCount)
                        easyCount = 0
                        break
                elif 'h' in character:
                    easyCount = 0
                    if mediumCount > 0:
                        categorywise_tipping_points[cat][1].append(mediumCount)
                        mediumCount = 0

    return categorywise_tipping_points


def get_pro_users(users, days_to_consider_pro):
    print('Getting pro users with days consideration: ' + str(days_to_consider_pro))
    pro_users = []
    for user in users:
        # Initializing sentinel values for first pass comparisons
        minDate = datetime.strptime('2100-01-01 01:01:01', '%Y-%m-%d %H:%M:%S')
        maxDate = datetime.strptime('1990-01-01 01:01:01', '%Y-%m-%d %H:%M:%S')
        for probCode in user.problemMappings:
            map = user.problemMappings[probCode]
            try:
                if minDate > datetime.strptime(map.date, '%Y-%m-%d %H:%M:%S'):
                    minDate = datetime.strptime(map.date, '%Y-%m-%d %H:%M:%S')
                if maxDate < datetime.strptime(map.date, '%Y-%m-%d %H:%M:%S'):
                    maxDate = datetime.strptime(map.date, '%Y-%m-%d %H:%M:%S')
            except ValueError as v:
                # Ignoring probable absence of datetime value like None
                # print('datetime found was none')
                pass
            except Exception as e:
                print(str(e) + ' found exception')
        timeDeltaObj = maxDate - minDate
        if timeDeltaObj.days > days_to_consider_pro:
            pro_users.append(user)

    return pro_users


def train_word2vec():
    try:
        with open('userNameToObjectsDict.pickle', 'r+b') as f:
            print ("Pickle used")
            userNameToObjectsDict = pickle.load(f)

    except:
        print ("DB accessed")
        userObjectsList, userNameToObjectsDict = get_codechef_users()

        with open('userNameToObjectsDict.pickle', 'w+b') as f:
            pickle.dump(userNameToObjectsDict, f)

    sentences = []

    for user in userNameToObjectsDict:
        submissionsDict = userNameToObjectsDict[user].problemMappings

        sorted_submissions = sort_by_date_difficulty(submissionsDict)

        submission_sentence = []

        [submission_sentence.append(row[0]) for row in sorted_submissions]
        sentences.append(submission_sentence)

    print ("Sentences done")
    print ("Started training Word2Vec model")
    start = time.time()
    model = Word2Vec(sentences, size=50, window=5, workers=2, min_count=1, iter=25, negative=15, sg=1)
    end = time.time()
    print ("Finished training Word2Vec model " + str(round((end - start) / 60, 2)) + " minutes")

    model.save("Codechef_word2vec")

