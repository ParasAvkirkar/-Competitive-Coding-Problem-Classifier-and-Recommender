from get_probs import get_all_probs_without_category_NA

import pickle

import sys, csv, os, random

sys.path.append('Utilities/')
from constants import categories, codechefDifficultyLevels, PlatformType, defaultTestSize, categoryWiseWeights
from get_users import get_codechef_users
from user_class import Codechef_User


def get_userNameToObjects(uniqueFileConvention, platform):
    if platform == PlatformType.Codechef:
        users = None
        if not os.path.isfile(uniqueFileConvention + '_orm.pickle'):
            print(uniqueFileConvention + '_orm.pickle ' + 'not found')
            userNameToObjects = get_codechef_users()
            with open(uniqueFileConvention + '_orm.pickle', 'wb') as f:
                print('Dumping ' + uniqueFileConvention + '_orm.pickle')
                pickle.dump(userNameToObjects, f)
        else:
            with open(uniqueFileConvention + '_orm.pickle', 'rb') as f:
                print('Loading from ' + uniqueFileConvention + '_orm.pickle')
                userNameToObjects = pickle.load(f)

    return userNameToObjects

def generateLazyLoad(uniqueFileConvention, platform, categorywise_difficulty_limits):
        userNameToObjects = get_userNameToObjects(uniqueFileConvention, platform)
        categorywise_difficulty_weights = {}
        for cat in categorywise_difficulty_limits:
            categorywise_difficulty_weights[cat] = [1.0, float(categorywise_difficulty_limits[cat][0]),
                                    float(categorywise_difficulty_limits[cat][0] * categorywise_difficulty_limits[cat][1])]

        write_dataset(uniqueFileConvention, userNameToObjects, platform, categorywise_difficulty_weights)
        return userNameToObjects

def write_dataset(uniqueFileConvention, userNameToObjects, platform, categorywise_difficulty_weights):


    print('Writing dataset')
    with open(uniqueFileConvention + '_dataset.csv', 'w') as f:
        f.write('uname')
        for category in categories:
            for level in codechefDifficultyLevels:
                f.write(',' + category + '_' + level)
        f.write('\n')
        for username in userNameToObjects:
            user = userNameToObjects[username]
            f.write(user.uname)
            for category in user.categoryDifficultyMap:
                i = 0
                for level in user.categoryDifficultyMap[category]:
                    value = len(user.categoryDifficultyMap[category][level]) * categoryWiseWeights[category]\
                                                                * categorywise_difficulty_weights[category][i]
                    f.write(',' + str(value))
                    i += 1
            f.write('\n')
        print('User Dataset written: ' + uniqueFileConvention)
