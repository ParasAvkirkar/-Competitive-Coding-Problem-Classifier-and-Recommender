from user_class import Codechef_User, Codechef_User_Prob_Map
from prob_class import Codechef_Problem

import sys, pickle
import datetime
import logging
import os
import inspect
import csv

sys.path.append('Utilities/')

from user_class import Codechef_User, Codechef_User_Prob_Map
from get_probs import get_all_probs_without_category_NA
from prob_class import Codechef_Problem
from get_session import get_session, get_session_by_configuration
from constants import PlatformType, codechefDifficultyLevels, categories

logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)


def get_codechef_users(probs_all_or_categorywise):
    s = get_session_by_configuration(useIntegrated=False)

    probCodeToDifficulty = {}
    with open('codechef_prob_diff.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            probCodeToDifficulty[line[0]] = line[1]

    probs = get_all_probs_without_category_NA(useIntegrated=False, platform=PlatformType.Codechef,
                                              probs_all_or_categorywise=probs_all_or_categorywise)
    probCodeToObjects = {}
    for p in probs:
        probCodeToObjects[p.prob_code] = p
    users = s.query(Codechef_User).filter()
    userNameToObjects = {}

    for user in users:
        userNameToObjects[user.uname] = user
    userProbMapQuery = s.query(Codechef_User_Prob_Map).filter()

    userProbMaps = [p for p in userProbMapQuery if p.date != 'None' and p.difficulty != '' and p.prob_code in probCodeToObjects]

    counter = 0.0
    userNotInProbTable = 0
    probNotInProbTablem = 0
    difficultyErrCount = 0

    for map in userProbMaps:
        try:
            user = userNameToObjects[map.uname]
            prob = probCodeToObjects[map.prob_code]
            difficulty = ''

            if map.prob_code in probCodeToDifficulty:
                difficulty = probCodeToDifficulty[map.prob_code]
            elif prob.difficulty in codechefDifficultyLevels:
                difficulty = prob.difficulty
            else:
                difficultyErrCount += 1
                user.failed_probs[map.prob_code] = map.no_of_submissions
                user.problemMappings[map.prob_code] = map
                continue

            for cat in categories:
                if cat in prob.category:
                    user.categoryDifficultyMap[cat][prob.difficulty] += 1

            user.level_wise_submissions[prob.difficulty] += 1

            if map.prob_code in user.problemMappings:
                if map.date > user.problemMappings[map.prob_code].date:
                    user.problemMappings[map.prob_code] = map
            else:
                user.problemMappings[map.prob_code] = map

            user.solved_probs[map.prob_code] = map.no_of_submissions
            user.solved_probs_obj[map.prob_code] = prob
            userNameToObjects[map.uname] = user
        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print "Exception"
            print map.prob_code
            print user.categoryDifficultyMap
            print user.uname
            failedKey = str(e).replace("'", "")

            if failedKey in str(map.prob_code):
                errorMsg = 'A problem in problem map exists whose row is not present in problem table ' \
                           + str(map.prob_code) + ' ' + failedKey
                user.failed_probs[map.prob_code] = map.no_of_submissions
                userNameToObjects[map.uname] = user
                probNotInProbTablem += 1
            elif failedKey in map.uname:
                errorMsg = 'A user in problem map exists whose row is not present in user table ' \
                           + str(map.uname) + ' ' + failedKey
                userNotInProbTable += 1

            logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(
                datetime.datetime.now(), os.path.basename(__file__), exc_tb.tb_lineno, errorMsg))

        counter += 1.0
        # For testing uncomment the block below, because whole function takes more than an hour to process
        # if round(counter*100/len(userProbMaps), 2) == 100 :
        #    break
        # print('Processing Map: '+str(round(counter*100/len(userProbMaps), 2) ) + '%')
    print('User failed cases: ' + str(userNotInProbTable) + ' Problem failed cases: ' +
          str(probNotInProbTablem) + ' Difficulty failed cases: ' + str(difficultyErrCount))
    # usersToBeReturned = []
    # for userName in userNameToObjects:
    #    usersToBeReturned.append(userNameToObjects[userName])
    print(str(len(userNameToObjects)))
    print('Fetched codechef users')
    return userNameToObjects, probCodeToObjects


def print_skewed_codechef_user_stats(userNameToObjects):
    count_of_skewed_users = 0
    for userName in userNameToObjects:
        total_solved = float(len(userNameToObjects[userName].solved_probs)
                             + len(userNameToObjects[userName].failed_probs))
        failed_to_fetch = float(len(userNameToObjects[userName].failed_probs))
        if total_solved > 0.0:
            print(str(userName) + ' had loss of ' + str((failed_to_fetch / total_solved) * 100) + '%')
        print(str(userName) + ' ' + str(failed_to_fetch) + ' ' + str(total_solved))
        if failed_to_fetch > 0.0:
            count_of_skewed_users += 1

    print('Skewed users: ' + str(count_of_skewed_users))
