import sys, pickle
import csv

# from libxslt import transformCtxt

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn/')
from constants import categories, performance_metric_keys, ClusterMethod, \
    PlatformType, Metrics, defaultTestSize
from generate_users_dataset import generateLazyLoad
from get_probs import get_all_probs_without_category_NA, get_probCodeToDiff_Map, get_probCodeToObjectMap
from user_train_operations import process_users, train_word2vec
from user_level_limits import get_categorywise_difficulty_limits, get_difficulty_limits_without_category

if __name__ == '__main__':

    uniqueFileConvention = 'users_codechef'

    # users = generateLazyLoad(uniqueFileConvention, PlatformType.Codechef)

    probs = get_all_probs_without_category_NA(useIntegrated=False, platform=PlatformType.Codechef)
    probCodeToObjects = get_probCodeToObjectMap(useIntegrated = False, platform = PlatformType.Codechef)

    probCodeToDifficulty = get_probCodeToDiff_Map(PlatformType.Codechef)

    # categorywise_difficulty_limits = get_categorywise_difficulty_limits(uniqueFileConvention, PlatformType.Codechef, probCodeToObjects,
    #                                    probCodeToDifficulty, days_to_consider_pro_user = 730)
    # userNameToObjects = generateLazyLoad(uniqueFileConvention, PlatformType.Codechef, categorywise_difficulty_limits)

    # # train_word2vec(uniqueFileConvention, PlatformType.Codechef)
    # process_users(uniqueFileConvention, userNameToObjects, probCodeToObjects, PlatformType.Codechef, ClusterMethod.KMeans)


    uniqueFileConvention = 'users_codechef'
    # train_word2vec(uniqueFileConvention, PlatformType.Codechef, probs_all_or_categorywise=1)
    # uniqueFileConvention = 'users_codechef_all_probs'
    # train_word2vec(uniqueFileConvention, PlatformType.Codechef, probs_all_or_categorywise=2)

    catwiselimits = get_categorywise_difficulty_limits(uniqueFileConvention, platform = PlatformType.Codechef,
                                                       days_to_consider_pro_user = 730)
    print('CategorywiseLimits: '+str(catwiselimits))
    normalDiffLimits = get_difficulty_limits_without_category(uniqueFileConvention, platform = PlatformType.Codechef,
                                                              days_to_consider_pro_user = 730)

    print('Normal Limits: ' + str(normalDiffLimits))


