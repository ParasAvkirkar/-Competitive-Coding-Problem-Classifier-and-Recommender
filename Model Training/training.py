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
from constants import categories, performance_metric_keys, ClassifierType, problemOrCategoryKeys, \
    PlatformType, Metrics, defaultTestSize

from operations import train_for_categoryModel1, get_accuracy, train_for_categoryModel2


def trainData(useIntegrate=False, platform=PlatformType.Default, problemOrCategoryWise=problemOrCategoryKeys['problem'],
              modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=defaultTestSize):
    if useIntegrate:
        platform = PlatformType.Default
    uniqueFileConvention = PlatformType.platformString[platform] + '_' + ("model1" if modelNumber is 1 else "model0")\
                            + '_' + ("catWise" if problemOrCategoryWise is 1 else "probWise")
    metricsFileName = uniqueFileConvention + '_' + str(test_size) + '_metrics.csv'
    if problemOrCategoryWise == problemOrCategoryKeys['problem']:
        classifierMetricsMap = {}
        for classifier in mlAlgos:
            print('CLASSIFICATION USING '+ ClassifierType.classifierTypeString[classifier])
            metricsList = []
            for category in categories:
                print("Processing for category: "+category)
                if modelNumber == 1:
                    generateLazyLoad(useIntegrate, category, platform, uniqueFileConvention, test_size=test_size)
                    m = train_for_categoryModel1(category, classifier, uniqueFileConvention, test_size=test_size)
                elif modelNumber == 2:
                    generateLazyLoadForModel2(useIntegrate, category, platform, uniqueFileConvention,
                                              test_size=defaultTestSize)
                    m = train_for_categoryModel2(category, classifier, uniqueFileConvention, test_size=defaultTestSize)

                metricsList.append(m)
                print("================ CATEGORY OVER ================")

            classifierMetricsMap[classifier] = metricsList
            print("================ CLASSIFIER OVER ================")

        Metrics.writeMultipleMetics(metricsFileName, classifierMetricsMap, isPositiveBased=True)
        print('Metrics are written to the file')
    else:
        classifierMetricsMap = {}
        for classifier in mlAlgos:
            if modelNumber == 1:
                if classifier in ClassifierType.onlyHyperClassifiers:
                    print('Cannot apply hyper based classifiers to problem-wise modelling technique')
                    continue
                print('Processing for classifier: '+ClassifierType.classifierTypeString[classifier])
                classifierMetricsMap[classifier] = get_accuracy(categories, classifier, uniqueFileConvention, useIntegrated=useIntegrate,
                             platform=platform, modelNumber=1, test_size=test_size)
                print('=================== CLASSIFICATION OVER ===================')
        Metrics.writeMultipleProblemwiseMetics(metricsFileName=metricsFileName,
                                               classifierMetricsMap=classifierMetricsMap)


if __name__ == '__main__':

    # test_sizeList = [0.1, 0.2, 0.3, 0.4, 0.5]
    test_sizeList = []
    for test_size in test_sizeList:
        trainData(useIntegrate=True, problemOrCategoryWise=1, modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=test_size)
        trainData(useIntegrate=False, platform=PlatformType.Codechef, problemOrCategoryWise=1, modelNumber=1,
                  mlAlgos=ClassifierType.allClassifierTypes, test_size=test_size)
        trainData(useIntegrate=False, platform=PlatformType.Codeforces, problemOrCategoryWise=1, modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=test_size)

        trainData(useIntegrate=True, problemOrCategoryWise=2, modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=test_size)
        trainData(useIntegrate=False, platform=PlatformType.Codechef, problemOrCategoryWise=2,
                  modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=test_size)
        trainData(useIntegrate=False, platform=PlatformType.Codeforces, problemOrCategoryWise=2,
                  modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=test_size)

    # trainData(useIntegrate=True, platform=PlatformType.Codechef, problemOrCategoryWise=2, modelNumber=1, mlAlgos=ClassifierType.onlyNonHyperClassifiers, test_size=0.2)
    trainData(useIntegrate=False, platform=PlatformType.Codechef, problemOrCategoryWise=1, modelNumber=2, mlAlgos=ClassifierType.onlyNonHyperClassifiers[:1], test_size=0.5)
    # trainData(False, platform=PlatformType.Codeforces, problemOrCategoryWise=1, modelNumber=2, mlAlgos=[ClassifierType.onlyNonHyperClassifiers[0]])

