from sklearn import neighbors, svm, tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
# from sklearn.exceptions import ConvergenceWarning
import numpy as np
import pandas
import sys, pickle
import warnings
from generate_dataset import generate, generateLazyLoad, generateLazyLoadForModel2

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn/')
from constants import categories, performance_metric_keys, ClassifierType, allClassifierTypes, problemOrCategoryKeys, \
    PlatformType, Metrics, onlyNonHyperClassifiers, onlyHyperClassifiers

from operations import train_for_categoryModel1, get_accuracy, train_for_categoryModel2


def trainData(useIntegrate=False, platform=PlatformType.Default, problemOrCategoryWise=1,
              modelNumber=1, mlAlgos=allClassifierTypes):
    if useIntegrate:
        platform = PlatformType.Default
    dataFilesNameHash = PlatformType.platformString[platform] + '_' + str(modelNumber)\
                            + '_' + str(problemOrCategoryWise)

    if problemOrCategoryWise == problemOrCategoryKeys['problem']:
        if modelNumber == 1:
            metricsFileName = dataFilesNameHash + '_metrics.csv'
            classifierMetricsMap = {}
            for classifier in mlAlgos:
                print('CLASSIFICATION USING '+ ClassifierType.classifierTypeString[classifier])
                metricsList = []
                for category in categories:
                    print("Processing for category: "+category)
                    generateLazyLoad(useIntegrate, category, platform, dataFilesNameHash + '_' + category)
                    m = train_for_categoryModel1(category, classifier, platform, dataFilesNameHash + '_' + category)
                    metricsList.append(m)

                    print("================ CATEGORY OVER ================")

                classifierMetricsMap[classifier] = metricsList
                print("================ CLASSIFIER OVER ================")

            Metrics.writeMultipleMetics(metricsFileName, classifierMetricsMap, isPositiveBased=True)
            print('Metrics are written to the file')
        else:
            metricsFileName = dataFilesNameHash + '_metrics.csv'
            classifierMetricsMap = {}
            for classifier in mlAlgos:
                print('CLASSIFICATION USING '+ ClassifierType.classifierTypeString[classifier])
                metricsList = []
                for category in categories:
                    print("Processing for category: "+category)

                    generateLazyLoadForModel2(useIntegrate, category, platform, dataFilesNameHash)
                    m = train_for_categoryModel2(category, classifier, platform, dataFilesNameHash)
                    metricsList.append(m)

                    print("================ CATEGORY OVER ================")

                classifierMetricsMap[classifier] = metricsList
                print("================ CLASSIFIER OVER ================")

            Metrics.writeMultipleMetics(metricsFileName, classifierMetricsMap, isPositiveBased=True)
            print('Metrics are written to the file')
    else:
        if modelNumber == 1:
            for classifier in mlAlgos:
                get_accuracy(categories, classifier, dataFilesNameHash, useIntegrated=useIntegrate, platform=platform, modelNumber=1)
        else:
            pass


if __name__ == '__main__':
    # trainData(useIntegrate=True, problemOrCategoryWise=1, model1or2=1, mlAlgos=allClassifierTypes)
    # trainData(useIntegrate=False, platform=PlatformType.Codeforces, problemOrCategoryWise=1, model1or2=1, mlAlgos=allClassifierTypes)
    # trainData(False, platform=PlatformType.Codechef, problemOrCategoryWise=1, modelNumber=1, mlAlgos=onlyNonHyperClassifiers[:-2])
    trainData(False, platform=PlatformType.Codeforces, problemOrCategoryWise=1, modelNumber=2, mlAlgos=[onlyNonHyperClassifiers[0]])