import sys, pickle

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn/')
from constants import categories, performance_metric_keys, ClusterMethod, \
    PlatformType, Metrics, defaultTestSize
from generate_users_dataset import generateLazyLoad
from get_probs import get_all_probs_without_category_NA
from user_train_operations import process_users

if __name__ == '__main__':
    uniqueFileConvention = 'users_codechef'
    users = generateLazyLoad(uniqueFileConvention, PlatformType.Codechef)
    probs = get_all_probs_without_category_NA(useIntegrated=False, platform=PlatformType.Codechef)
    process_users(uniqueFileConvention, users, probs, PlatformType.Codechef, ClusterMethod.KMeans)