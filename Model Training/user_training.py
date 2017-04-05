import sys, pickle
import csv

from libxslt import transformCtxt

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn/')
from constants import categories, performance_metric_keys, ClusterMethod, \
    PlatformType, Metrics, defaultTestSize
from generate_users_dataset import generateLazyLoad
from get_probs import get_all_probs_without_category_NA
from user_train_operations import process_users, get_categorywise_difficulty_limits, train_word2vec

if __name__ == '__main__':
    # users = generateLazyLoad(uniqueFileConvention, PlatformType.Codechef)
    probs = get_all_probs_without_category_NA(useIntegrated=False, platform=PlatformType.Codechef)
    probCodeToObjects = {}
    for prb in probs:
        probCodeToObjects[prb.prob_code] = prb
    probCodeToDifficulty = {}

    with open('codechef_prob_diff.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            probCodeToDifficulty[line[0]] = line[1]


    uniqueFileConvention = 'users_codechef'
    train_word2vec(uniqueFileConvention, PlatformType.Codechef, probs_all_or_categorywise=1)
    uniqueFileConvention = 'users_codechef_all_probs'
    train_word2vec(uniqueFileConvention, PlatformType.Codechef, probs_all_or_categorywise=2)

