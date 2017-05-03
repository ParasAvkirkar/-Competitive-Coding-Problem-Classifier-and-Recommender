from get_probs import get_all_probs_without_category_NA

import pickle

import sys, csv, os, random

sys.path.append('Utilities/')
from constants import categories, codechefDifficultyLevels, PlatformType, defaultTestSize, categoryWiseWeights
from get_users import get_codechef_users
from user_class import Codechef_User

userNameToObjects = None
userNameToObjectsAll = None


def get_userNameToObjects(uniqueFileConvention, platform):
    if platform == PlatformType.Codechef:
        users = None
        if not os.path.isfile(uniqueFileConvention + '_orm.pickle'):
            print(uniqueFileConvention + '_orm.pickle ' + 'not found')
            userNameToObjects, probCodeToObjects = get_codechef_users()
            with open(uniqueFileConvention + '_orm.pickle', 'wb') as f:
                print('Dumping ' + uniqueFileConvention + '_orm.pickle')
                pickle.dump(userNameToObjects, f)
        else:
            with open(uniqueFileConvention + '_orm.pickle', 'rb') as f:
                print('Loading from ' + uniqueFileConvention + '_orm.pickle')
                userNameToObjects = pickle.load(f)

    return userNameToObjects

def get_probCodeToObjects():
    with open('users/' + 'codechef_probs.pickle', 'rb') as f:
        probCodeToObjects = pickle.load(f)

    with open('users/' + 'codechef_probs_all.pickle', 'rb') as f:
        probCodeToObjectsAll = pickle.load(f)

    return probCodeToObjects, probCodeToObjectsAll


def generateLazyLoad(uniqueFileConvention, platform=PlatformType.Codechef, username='none'):
    global userNameToObjects

    # if userNameToObjects is None:
    #     if platform == PlatformType.Codechef:
    #         users = None
    userObject = None
    if userNameToObjects is not None:
        return userNameToObjects

    if not os.path.isfile('users/'+ uniqueFileConvention + '_orm.pickle'):
        print(uniqueFileConvention + '_orm.pickle ' + 'not found')
        userNameToObjects, probCodeToObjects = get_codechef_users(probs_all_or_categorywise=1)
        print('Dumping ' + uniqueFileConvention + '_orm.pickle')
        with open('users/' + uniqueFileConvention + '_orm.pickle', 'wb') as f:
            pickle.dump(userNameToObjects, f)

        with open('users/' + 'codechef_probs.pickle', 'wb') as f:
            pickle.dump(probCodeToObjects, f)

        for user in userNameToObjects:
            with open('users/' + uniqueFileConvention + '_' + user + '.pickle', 'wb') as f:
                pickle.dump(userNameToObjects[user], f)

        userObject = userNameToObjects[username]

    else:
        # with open(uniqueFileConvention + '_orm.pickle', 'rb') as f:
        #     print('Loading from ' + uniqueFileConvention + '_orm.pickle')
        #     userNameToObjects = pickle.load(f)
        with open('users/' + uniqueFileConvention + '_' + username + '.pickle', 'rb') as f:
            userObject = pickle.load(f)
            # write_dataset(uniqueFileConvention, userNameToObjects, platform)

    return userObject


def generateLazyLoadAll(uniqueFileConvention, platform=PlatformType.Codechef, username='none'):
    global userNameToObjectsAll

    # if userNameToObjectsAll is None:
    #     if platform == PlatformType.Codechef:
    #         users = None

    userObjectsAll = None

    if userNameToObjectsAll is not None:
        return userNameToObjectsAll

    if not os.path.isfile('users/' + uniqueFileConvention + '_orm.pickle'):
        print(uniqueFileConvention + '_orm.pickle ' + 'not found')
        userObjectsAll, probCodeToObjects = get_codechef_users(probs_all_or_categorywise=2)
        print('Dumping ' + uniqueFileConvention + '_orm.pickle')

        with open('users/' + uniqueFileConvention + '_orm.pickle', 'wb') as f:
            pickle.dump(userObjectsAll, f)

        with open('users/' + 'codechef_probs_all.pickle', 'wb') as f:
            pickle.dump(probCodeToObjects, f)

        for user in userNameToObjects:
            with open('users/' + uniqueFileConvention + '_' + user + '.pickle', 'wb') as f:
                pickle.dump(userNameToObjects[user], f)

    else:
        # with open(uniqueFileConvention + '_orm.pickle', 'rb') as f:
        #     print('Loading from ' + uniqueFileConvention + '_orm.pickle')
        #     userNameToObjectsAll = pickle.load(f)
        with open('users/' + uniqueFileConvention + '_' + username + '.pickle', 'rb') as f:
            userObjectsAll = pickle.load(f)
            # write_dataset(uniqueFileConvention, userNameToObjects, platform)

    return userObjectsAll


def write_dataset(uniqueFileConvention, userNameToObjects, platform=PlatformType.Codechef):
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
