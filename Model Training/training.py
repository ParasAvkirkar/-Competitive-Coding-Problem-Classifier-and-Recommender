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


def trainData(useIntegrate=False, platform=PlatformType.Default, problemOrCategoryWise=1,
              modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=defaultTestSize):
    if useIntegrate:
        platform = PlatformType.Default
    dataFilesNameHash = PlatformType.platformString[platform] + '_' + ("model1" if modelNumber is 1 else "model0")\
                            + '_' + ("catWise" if problemOrCategoryWise is 1 else "probWise")
    metricsFileName = dataFilesNameHash + '_' + str(test_size) + '_metrics.csv'
    if problemOrCategoryWise == problemOrCategoryKeys['problem']:
        if modelNumber == 1:

            classifierMetricsMap = {}
            for classifier in mlAlgos:
                print('CLASSIFICATION USING '+ ClassifierType.classifierTypeString[classifier])
                metricsList = []
                for category in categories:
                    print("Processing for category: "+category)
                    generateLazyLoad(useIntegrate, category, platform, dataFilesNameHash + '_' + category, test_size=test_size)
                    m = train_for_categoryModel1(category, classifier, platform, dataFilesNameHash + '_' + category, test_size=test_size)
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
            classifierMetricsMap = {}
            for classifier in mlAlgos:
                if classifier in ClassifierType.onlyHyperClassifiers:
                    print('Cannot apply hyper based classifiers to problem-wise modelling technique')
                    continue
                print('Processing for classifier: '+ClassifierType.classifierTypeString[classifier])
                classifierMetricsMap[classifier] = get_accuracy(categories, classifier, dataFilesNameHash, useIntegrated=useIntegrate,
                             platform=platform, modelNumber=1, test_size=test_size)
                print('=================== CLASSIFICATION OVER ===================')
            Metrics.writeMultipleProblemwiseMetics(metricsFileName=metricsFileName,
                                                   classifierMetricsMap=classifierMetricsMap)
        else:
            pass


if __name__ == '__main__':

    test_sizeList = [0.1, 0.2, 0.3, 0.4, 0.5]
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

        # trainData(useIntegrate=True, problemOrCategoryWise=1, model1or2=1, mlAlgos=allClassifierTypes)
        # trainData(useIntegrate=False, platform=PlatformType.Codeforces, problemOrCategoryWise=1, model1or2=1, mlAlgos=allClassifierTypes)
        # trainData(False, platform=PlatformType.Codechef, problemOrCategoryWise=1, modelNumber=1, mlAlgos=onlyNonHyperClassifiers[:-2])
        trainData(False, platform=PlatformType.Codeforces, problemOrCategoryWise=1, modelNumber=2, mlAlgos=[onlyNonHyperClassifiers[0]])

