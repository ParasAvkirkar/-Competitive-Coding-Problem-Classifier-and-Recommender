import os
import sys
import pickle
import matplotlib.pyplot as plt
from scipy.stats import mode
from generate_problems_dataset import generate, generateLazyLoad
from generate_users_dataset import generateLazyLoad, generateLazyLoadAll
from datetime import datetime
from get_probs import get_all_probs_without_category_NA, get_probCodeToObjectMap, get_probCodeToDiff_Map

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn')

from constants import categories, performance_metric_keys, ClusterMethod, \
    PlatformType, Metrics, defaultTestSize, codechefDifficultyLevels

# categorywise_difficulty_limits = None
difficulty_limits_without_category = None


# Right now handles codechef, later platform wise changes would be made
def get_difficulty_limits_without_category(uniqueFileConvention, platform, days_to_consider_pro_user):
    global difficulty_limits_without_category

    if difficulty_limits_without_category == None:
        print('Building tipping points without category')
        userNameToObjects = generateLazyLoad(uniqueFileConvention, platform)
        pro_users = get_pro_users(userNameToObjects, days_to_consider_pro_user)
        print('Got ' + str(len(pro_users)) + ' pro users')

        probCodeToObjects = get_probCodeToObjectMap(useIntegrated = False, platform = PlatformType.Codechef)
        probCodeToDifficulty = get_probCodeToDiff_Map(platform)
        tipping_points = {0: [], 1: []}

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
            difficultySequence = ''  # categorySolvingSequence = {} # A dictionary category --->
            for tupl in list_of_mapping_date:
                map = tupl[0]
                try:
                    prob = probCodeToObjects[map.prob_code]
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
                    # print(str(e))
                    pass

            easyCount = 0
            mediumCount = 0
            for character in difficultySequence:
                if 'e' in character:
                    easyCount += 1
                    mediumCount = 0
                elif 'm' in character:
                    mediumCount += 1
                    if easyCount > 0:
                        tipping_points[0].append(easyCount)
                        easyCount = 0
                elif 'h' in character:
                    easyCount = 0
                    if mediumCount > 0:
                        tipping_points[1].append(mediumCount)
                        mediumCount = 0
        tipping_points[0].sort()
        tipping_points[1].sort()
        # print(str(tipping_points[0]))
        # print(str(tipping_points[1]))
        #
        # if len(plt.get_fignums()) > 0:
        #     print('Existing pyplot windows opened are now being closed')
        #     plt.close()
        #
        # plt.plot([i for i in range(len(tipping_points[0]))], tipping_points[0], 'b-')
        # plt.plot([i for i in range(len(tipping_points[1]))], tipping_points[1], 'r-')
        # plt.xlabel(' tipping points')
        # plt.show()

        difficulty_limits_without_category = {'easy': get_equivalence_by_tendency(tipping_points[0]),
                                              'medium': get_equivalence_by_tendency(tipping_points[1])}

        # print('Normal Difficulty Limits ' + str(difficulty_limits_without_category))

    return difficulty_limits_without_category


# Right now handles codechef, later platform wise changes would be made
def get_categorywise_difficulty_limits(uniqueFileConvention, platform, days_to_consider_pro_user):

    categorywise_difficulty_limits = {}
    if not os.path.isfile('users/' + uniqueFileConvention + '_catwise_diff.pickle'):
        probCodeToDifficulty = get_probCodeToDiff_Map(platform)
        probCodeToObjects = get_probCodeToObjectMap(useIntegrated = False, platform = platform)

        categorywise_tipping_points = get_categorywise_tipping_points(uniqueFileConvention, platform, probCodeToObjects,
                                                                      probCodeToDifficulty, days_to_consider_pro_user)
        print('Got categorywise tipping points')

        if len(plt.get_fignums()) > 0:
            print('Existing pyplot windows opened are now being closed')
            plt.close()

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
                categorywise_difficulty_limits[cat]['easy'] = get_equivalence_by_tendency(
                    categorywise_tipping_points[cat][0])
                categorywise_difficulty_limits[cat]['medium'] = get_equivalence_by_tendency(
                    categorywise_tipping_points[cat][1])
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

        # print categorywise_difficulty_limits
        with open('users/' + uniqueFileConvention + '_catwise_diff.pickle', 'wb') as f:
            pickle.dump(categorywise_difficulty_limits, f)
    else:
        with open('users/' + uniqueFileConvention + '_catwise_diff.pickle', 'rb') as f:
            categorywise_difficulty_limits = pickle.load(f)
    return categorywise_difficulty_limits


# Current tendency defining function is max, later on it can be median or mode
def get_equivalence_by_tendency(list_of_tipping_point):
    value = 0 if len(list_of_tipping_point) == 0 else max(list_of_tipping_point)
    return value


def get_categorywise_tipping_points(uniqueFileConvention, platform, probCodeToObjects, probCodeToDifficulty,
                                    days_to_consider_pro_user):
    print('Building category wise tipping points')
    userNameToObjects = generateLazyLoad(uniqueFileConvention, platform)
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
                    # print(str(e))
                    pass

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
