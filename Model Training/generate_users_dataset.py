from get_probs import get_all_probs_without_category_NA

import pickle

import sys, csv, os, random

sys.path.append('Utilities/')
from constants import categories, performance_metric_keys, ClassifierType, problemOrCategoryKeys, \
    PlatformType, defaultTestSize
from get_users import get_codechef_users
from user_class import Codechef_User


def generate(uniqueFileConvention, platform=PlatformType.Codechef):
    if platform == PlatformType.Codechef:
        users = None
        if not os.path.isfile(uniqueFileConvention + '_orm.pickle'):
            print(uniqueFileConvention + '_orm.pickle ' + 'not found')
            users = get_codechef_users()
            with open(uniqueFileConvention + '_orm.pickle', 'wb') as f:
                print('Dumping ' + uniqueFileConvention + '_orm.pickle')
                pickle.dump(users, f)
        else:
            with open(uniqueFileConvention + '_orm.pickle', 'rb') as f:
                print('Loading from ' + uniqueFileConvention + '_orm.pickle')
                users = pickle.load(f)

        write_dataset(uniqueFileConvention, users)


def write_dataset(uniqueFileConvention, users):
    print('Writing dataset')
    with open(uniqueFileConvention + '_dataset.csv', 'w') as f:
        for user in users:
            f.write(user.uname)
            for category in user.categoryDifficultyMap:
                for level in user.categoryDifficultyMap[category]:
                    f.write(',' + str(len(user.categoryDifficultyMap[category][level])))
            f.write('\n')
        print('User Dataset written: ' + uniqueFileConvention)
