import sys, pickle

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn/')
from constants import categories, performance_metric_keys, ClassifierType, problemOrCategoryKeys, \
    PlatformType, Metrics, defaultTestSize
from generate_users_dataset import generate

if __name__ == '__main__':
    uniqueFileConvention = 'users_codechef'
    generate(uniqueFileConvention, PlatformType.Codechef)