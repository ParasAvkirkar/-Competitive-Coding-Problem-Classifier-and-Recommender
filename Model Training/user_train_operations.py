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
from scipy.stats import mode
from generate_problems_dataset import generate, generateLazyLoad
from recommend import build_recommendation_list_for_clusters

from generate_users_dataset import generateLazyLoad, generateLazyLoadAll
from datetime import datetime
from get_probs import get_all_probs_without_category_NA
from gensim.models import Word2Vec
from get_users import get_codechef_users
from sorting import sort_by_date_difficulty


sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn')

from constants import categories, performance_metric_keys, ClusterMethod, \
    PlatformType, Metrics, defaultTestSize, codechefDifficultyLevels

categorywise_difficulty_limits = None

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

    usersClusterMap = build_recommendation_list_for_clusters(usersClusterMap, probCodeToObjects)
    usersToBeWrittenOnPickle = []
    for label in usersClusterMap:
        usersList = usersClusterMap[label]
        usersToBeWrittenOnPickle = usersToBeWrittenOnPickle + usersList

    with open(dataFileConvention + '_orm.pickle', 'wb') as f:
        print('Dumping ' + uniqueFileConvention + '_orm.pickle')
        pickle.dump(usersToBeWrittenOnPickle, f)


# Right now handles codechef, later platform wise changes would be made
def get_categorywise_difficulty_limits(uniqueFileConvention, platform, days_to_consider_pro_user):

    global categorywise_difficulty_limits
    if categorywise_difficulty_limits ==  None:
        categorywise_difficulty_limits = {}

        probs = get_all_probs_without_category_NA(useIntegrated=False, platform=PlatformType.Codechef)
        probCodeToObjects = {}
        for prb in probs:
            probCodeToObjects[prb.prob_code] = prb

        probCodeToDifficulty = {}
        with open('codechef_prob_diff.csv', 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                probCodeToDifficulty[line[0]] = line[1]

        categorywise_tipping_points = get_categorywise_tipping_points(uniqueFileConvention, platform, probCodeToObjects, probCodeToDifficulty, days_to_consider_pro_user)
        print('Got categorywise tipping points')
        for cat in categories:
            categorywise_tipping_points[cat][0].sort()
            categorywise_tipping_points[cat][1].sort()
            len0 = len(categorywise_tipping_points[cat][0])
            len1 = len(categorywise_tipping_points[cat][1])
            # print cat
            # print(str(len0) + ' ' + str(len1))
            try:
                # print('Category: ' + cat + ' Maximum Stats ---> Easy_To_Medium: ' + str(
                #     max(categorywise_tipping_points[cat][0])) + ' Medium_To_Hard: '
                #       + str(max(categorywise_tipping_points[cat][1])))
                # Currently considering maximum value as tendency of difficulty limits
                categorywise_difficulty_limits[cat] = {}
                categorywise_difficulty_limits[cat]['easy'] = max(categorywise_tipping_points[cat][0])
                categorywise_difficulty_limits[cat]['medium'] = max(categorywise_tipping_points[cat][1])
                # print('Category: ' + cat + ' Median Stats ---> Easy_To_Medium: ' + str(
                #     categorywise_tipping_points[cat][0][len0 / 2]) + ' Medium_To_Hard: '
                #       + str(categorywise_tipping_points[cat][1][len1 / 2]))
                # print('Category: ' + cat + ' Easy_To_Medium: ' + str(mode(categorywise_tipping_points[cat][0])) + ' Medium_To_Hard: '
                # + str(mode(categorywise_tipping_points[cat][1])))
                # print('===============')
            except Exception as e:
                print e
            plt.plot([i for i in range(len(categorywise_tipping_points[cat][0]))], categorywise_tipping_points[cat][0],
                     'b-')
            plt.plot([i for i in range(len(categorywise_tipping_points[cat][1]))], categorywise_tipping_points[cat][1],
                     'r-')
            plt.xlabel(cat + ' tipping points')
            # plt.show()

        print categorywise_difficulty_limits

    return categorywise_difficulty_limits

# Current tendency defining function is max, later on it can be median or mode
def get_equivalence_by_tendency(easy_to_med_list, med_to_high_list):
    easy_to_med = 0 if len(easy_to_med_list) == 0 else max(easy_to_med_list)
    med_to_high = 0 if len(med_to_high_list) == 0 else max(med_to_high_list)
    return easy_to_med, med_to_high


def get_categorywise_tipping_points(uniqueFileConvention, platform, probCodeToObjects, probCodeToDifficulty,
                                    days_to_consider_pro_user):
    print('Building category wise tipping points')
    userNameToObjects = get_userNameToObjects(uniqueFileConvention, platform)
    pro_users = get_pro_users(userNameToObjects, days_to_consider_pro_user)
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


def get_pro_users(userNameToObjects, days_to_consider_pro):
    print('Getting pro users with days consideration: ' + str(days_to_consider_pro))
    pro_users = []
    for username in userNameToObjects:
        user = userNameToObjects[username]
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


def train_word2vec(uniqueFileConvention, platform,probs_all_or_categorywise):
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
    print ("Finished training Word2Vec model " + str(round((end - start) / 60, 2)) + " minutes")

    model.save(uniqueFileConvention)

