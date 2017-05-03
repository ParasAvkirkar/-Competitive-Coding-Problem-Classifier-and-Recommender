import sys
import os
import pickle
import operator
from get_probs import get_all_probs_without_category_NA
from user_class import Codechef_User_Prob_Map
from get_session import get_session_by_configuration
from get_probs import get_category, get_difficulty

sys.path.append("Utilities/")
from constants import PlatformType, codechefDifficultyLevels, categories

popular_problems_by_level_cat = None

def generate_popular_problems():

    global popular_problems_by_level_cat
    if popular_problems_by_level_cat is not None:
        return popular_problems_by_level_cat

    if not os.path.isfile('users/popular_probs.pickle'):
        s = get_session_by_configuration(useIntegrated=False)
        probs = get_all_probs_without_category_NA(useIntegrated=False, platform=PlatformType.Codechef, probs_all_or_categorywise=1)

        probCodeToObjects = {}
        for p in probs:
            probCodeToObjects[p.prob_code] = p

        userProbMapQuery = s.query(Codechef_User_Prob_Map).filter()
        userProbMaps = [p for p in userProbMapQuery if p.difficulty != '' and p.prob_code in probCodeToObjects]

        popular_problems_by_level_cat = {}
        for level in codechefDifficultyLevels:
            popular_problems_by_level_cat[level] = {}
            for cat in categories:
                popular_problems_by_level_cat[level][cat] = {}

        for map in userProbMaps:
            for cat in get_category(map.prob_code):
                if map.prob_code not in popular_problems_by_level_cat[map.difficulty][cat]:
                    popular_problems_by_level_cat[map.difficulty][cat][map.prob_code] = 0
                popular_problems_by_level_cat[map.difficulty][cat][map.prob_code] += 1

        for level in codechefDifficultyLevels:
            for cat in categories:
                sorted_popular_probs = sorted(popular_problems_by_level_cat[level][cat].items(), key=lambda k: k[1], reverse=True)
                popular_problems_by_level_cat[level][cat] = sorted_popular_probs

        with open('users/popular_probs.pickle', 'wb') as f:
            pickle.dump(popular_problems_by_level_cat, f)

    else:
        with open('users/popular_probs.pickle', 'rb') as f:
            popular_problems_by_level_cat = pickle.load(f)

    return popular_problems_by_level_cat

def get_popular(level, category, all_recommendation, solved_probs):
    popular_problems_by_level_cat = generate_popular_problems()
    problem = None

    for prob_code in popular_problems_by_level_cat[level][category]:
        if prob_code not in all_recommendation and prob_code not in solved_probs:
            problem = prob_code
            break

    return problem[0]
