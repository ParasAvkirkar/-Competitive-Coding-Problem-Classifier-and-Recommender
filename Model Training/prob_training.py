import sys, pickle
from generate_problems_dataset import generate, generateLazyLoad, generateLazyLoadForModel2

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn/')
from constants import categories, performance_metric_keys, ClassifierType, problemOrCategoryKeys, \
    PlatformType, Metrics, defaultTestSize

from prob_train_operations import train_for_categoryModel1, get_accuracy, train_for_categoryModel2, baggingBasedTraining


def trainData(useIntegrate=False, platform=PlatformType.Default, problemOrCategoryWise=problemOrCategoryKeys['category'],
              modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=defaultTestSize, shouldBag=False,
              number_of_top_words=10):
    if useIntegrate:
        platform = PlatformType.Default
    uniqueFileConvention = PlatformType.platformString[platform] + '_' + ("model1" if modelNumber is 1 else "model2")\
                            + '_' + ("catWise" if problemOrCategoryWise is 1 else "probWise") +\
                           "_" + ("bag" if shouldBag else "notBag") + '_' + str(number_of_top_words)
    dataFileConvention = PlatformType.platformString[platform] + '_' + ("model1" if modelNumber is 1 else "model2")\
                         + '_' + str(number_of_top_words)

    metricsFileName = uniqueFileConvention + '_' + str(test_size)+ '_' + str(number_of_top_words) + '_metrics.csv'
    if shouldBag:
        accuracy = baggingBasedTraining(categories, mlAlgos,
                             uniqueFileConvention, dataFileConvention, useIntegrated = useIntegrate,
                             platform = platform, test_size = test_size)
    elif problemOrCategoryWise == problemOrCategoryKeys['category']:
        classifierMetricsMap = {}
        for classifier in mlAlgos:
            print('CLASSIFICATION USING '+ ClassifierType.classifierTypeString[classifier])
            metricsList = []
            for category in categories:
                print("Processing for category: "+category)
                tempDataFileConv = dataFileConvention + '_' + category + '_' + str(test_size)
                if modelNumber == 1:
                    generateLazyLoad(useIntegrate, category, platform, uniqueFileConvention, tempDataFileConv, test_size=test_size,
                                     number_of_top_words = number_of_top_words)
                    m = train_for_categoryModel1(category, classifier, uniqueFileConvention,
                                                 tempDataFileConv, test_size=test_size)
                elif modelNumber == 2:
                    generateLazyLoadForModel2(useIntegrate, category, platform, uniqueFileConvention,
                                              tempDataFileConv, test_size=test_size)
                    m = train_for_categoryModel2(category, classifier, uniqueFileConvention,
                                                 tempDataFileConv, test_size=test_size)
                metricsList.append(m)
                print("================ CATEGORY OVER ================")
                if m.isValid:
                    print('Metrics: ' + str(m.precision[1]) + ' ' + str(m.recall[1]) + ' ' + str(m.fScore[1]))
                else:
                    print('Metrics invalid')

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
                classifierMetricsMap[classifier] = get_accuracy(categories, classifier, uniqueFileConvention, dataFileConvention,
                                                   useIntegrated=useIntegrate,
                             platform=platform, modelNumber=1, test_size=test_size, number_of_top_words=number_of_top_words)
                print('=================== CLASSIFICATION OVER ===================')
        Metrics.writeMultipleProblemwiseMetics(metricsFileName=metricsFileName,
                                               classifierMetricsMap=classifierMetricsMap)


if __name__ == '__main__':

    # test_sizeList = [0.1, 0.2, 0.3, 0.4, 0.5]
    # trainData(useIntegrate = True, platform = PlatformType.Default, problemOrCategoryWise=1,
    #           modelNumber=1, mlAlgos=ClassifierType.onlyNonHyperClassifiers, test_size=0.2, shouldBag=False)

    # trainData(shouldBag = True, useIntegrate = True, problemOrCategoryWise = 1, modelNumber = 1,
    #           mlAlgos = ClassifierType.onlyNonHyperClassifiers, test_size = 0.2)
    for n in [i for i in range(1,16)]:
        trainData(useIntegrate = True, platform = PlatformType.Default, problemOrCategoryWise = 2,
              modelNumber = 1, mlAlgos = ClassifierType.onlyNonHyperClassifiers, test_size = 0.2, shouldBag = False,
                  number_of_top_words = n)