from user_class import Codechef_User, Codechef_User_Prob_Map
from prob_class import Codechef_Problem

import sys, pickle
import datetime
import logging
import os
import inspect

sys.path.append('Utilities/')

from user_class import Codechef_User, Codechef_User_Prob_Map
from get_probs import get_all_probs_without_category_NA
from prob_class import Codechef_Problem
from get_session import get_session, get_session_by_configuration
from constants import PlatformType

logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)

def get_codechef_users():
    s = get_session_by_configuration(useIntegrated=False)

    probs = get_all_probs_without_category_NA(useIntegrated=False, platform=PlatformType.Codechef)
    probCodeToObjects = {}
    for p in probs:
        probCodeToObjects[p.prob_code] = p

    print('Prob code to object Map built')
    users = s.query(Codechef_User).filter()
    userNameToObjects = {}
    for user in users:
        userNameToObjects[user.uname] = user

    print('User name to object Map built')
    userProbMaps = s.query(Codechef_User_Prob_Map).filter()
    counter = 0.0
    for map in userProbMaps:
        try:
            user = userNameToObjects[map.uname]
            prob = probCodeToObjects[map.prob_code]
            user.categoryDifficultyMap[prob.category][prob.difficulty].append(map.no_of_submissions)
            user.solved_probs[map.prob_code] = map.no_of_submissions
            userNameToObjects[map.uname] = user
        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            #print 'Exception at line ' + str(exc_tb.tb_lineno)
            if str(e) in map.prob_code:
                errorMsg = 'A problem in problem map exists whose row is not present in problem table '\
                           + str(map.prob_code) + ' ' + str(e)
                user.failed_probs[map.prob_code] = map.no_of_submissions
                userNameToObjects[map.uname] = user
            elif str(e) in map.uname:
                errorMsg = 'A user in problem map exists whose row is not present in user table '\
                           + str(map.uname) + ' ' + str(e)
            else:
                errorMsg = 'Difficulty was empty in problem table ' + str(map.prob_code) + ' ' + str(e)
                user.failed_probs[map.prob_code] = map.no_of_submissions
                userNameToObjects[map.uname] = user
            #print(errorMsg)
            logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(
                    datetime.datetime.now(), os.path.basename(__file__), exc_tb.tb_lineno, errorMsg))

        counter += 1.0
        # For testing uncomment the block below, because whole function takes more than an hour to process
        # if round(counter*100/userProbMaps.count(), 2) > 5:
        #     break
        print('Processing Map: '+str(round(counter*100/userProbMaps.count(), 2) ) + '%')

    usersToBeReturned = []
    count_of_skewed_users = 0
    for userName in userNameToObjects:
        total_solved = float(len(userNameToObjects[userName].solved_probs)
                             + len(userNameToObjects[userName].failed_probs))
        failed_to_fetch = float(len(userNameToObjects[userName].failed_probs))
        if total_solved > 0.0:
            print(str(userName) + ' had loss of ' + str((failed_to_fetch/total_solved)*100)+ '%')
        print(str(userName) + ' ' + str(failed_to_fetch) + ' ' + str(total_solved))
        # print(str(userNameToObjects[userName].solved_probs))
        # print(str(userNameToObjects[userName].failed_probs))
        if failed_to_fetch > 0.0:
            count_of_skewed_users += 1
        usersToBeReturned.append(userNameToObjects[userName])

    print('Skewed users: '+str(count_of_skewed_users))
    print('Fetched codechef users')
    return usersToBeReturned
