import sys, pickle
from generate_problems_dataset import generateLazyLoad, generateLazyLoadForModel2

sys.path.append('../Utilities/')
sys.path.append('../../hyperopt-sklearn/')
from constants import categories, performance_metric_keys, ClassifierType, problemOrCategoryKeys, \
    PlatformType, Metrics, defaultTestSize
from get_conventions import get_problem_model_file_convention, get_problem_dataset_file_convention, \
    get_problem_metrics_file_convention
from prob_train_operations import train_for_categoryModel1, get_accuracy, train_for_categoryModel2


def trainData(useIntegrate=False, platform=PlatformType.Default,
              problemOrCategoryWise=problemOrCategoryKeys['category'],
              modelNumber=1, mlAlgos=ClassifierType.allClassifierTypes, test_size=defaultTestSize,
              number_of_top_words=10):
    if useIntegrate:
        platform = PlatformType.Default

    print(str(type(number_of_top_words)))
    metricsFileName = get_problem_metrics_file_convention(platform=platform, model_number=modelNumber, category_or_problemWise=("catWise" if problemOrCategoryWise is 1 else "probWise"),
                                                          test_size=test_size, number_of_top_words=number_of_top_words)  + '_metrics.csv'

    if problemOrCategoryWise == problemOrCategoryKeys['category']:
        classifierMetricsMap = {}
        for classifier in mlAlgos:
            print('CLASSIFICATION USING ' + ClassifierType.classifierTypeString[classifier])
            metricsList = []
            for category in categories:
                print("Processing for category: " + category)
                if modelNumber == 1:
                    generateLazyLoad(useIntegrate, category, platform, test_size = test_size,
                                     number_of_top_words = number_of_top_words)
                    m = train_for_categoryModel1(platform = platform, number_of_top_words = number_of_top_words, category = category, classifier = classifier,
                                                 test_size = test_size)
                elif modelNumber == 2:
                    #Deprecated code dont send model number = 2
                    tempDataFileConv = ''
                    uniqueFileConvention = PlatformType.platformString[platform] + '_' + (
                    "model1" if modelNumber is 1 else "model2") \
                                           + '_' + ("catWise" if problemOrCategoryWise is 1 else "probWise") + \
                                           '_' + str(number_of_top_words)
                    dataFileConvention = PlatformType.platformString[platform] + '_' + (
                    "model1" if modelNumber is 1 else "model2") \
                                         + '_' + str(number_of_top_words)



                    generateLazyLoadForModel2(useIntegrate, category, platform, uniqueFileConvention,
                                              tempDataFileConv, test_size = test_size)
                    m = train_for_categoryModel2(category, classifier, uniqueFileConvention,
                                                 tempDataFileConv, test_size = test_size)
                metricsList.append(m)
                print("================ CATEGORY OVER ================")
                if m.isValid:
                    print('Metrics: ' + str(m.precision[1]) + ' ' + str(m.recall[1]) + ' ' + str(m.fScore[1]))
                else:
                    print('Metrics invalid')

            classifierMetricsMap[classifier] = metricsList
            print("================ CLASSIFIER OVER ================")

        Metrics.writeMultipleMetics(metricsFileName, classifierMetricsMap, isPositiveBased = True)
        print('Metrics are written to the file')
    else:
        classifierMetricsMap = {}
        for classifier in mlAlgos:
            if modelNumber == 1:
                if classifier in ClassifierType.onlyHyperClassifiers:
                    print('Cannot apply hyper based classifiers to problem-wise modelling technique')
                    continue
                print('Processing for classifier: ' + ClassifierType.classifierTypeString[classifier])
                classifierMetricsMap[classifier] = get_accuracy(categories, classifier, useIntegrated = useIntegrate,
                                                                platform = platform, modelNumber = 1,
                                                                test_size = test_size, number_of_top_words = number_of_top_words)
                print('=================== CLASSIFICATION OVER ===================')
        Metrics.writeMultipleProblemwiseMetics(metricsFileName = metricsFileName,
                                               classifierMetricsMap = classifierMetricsMap)


def trainDataByEnsemble():
    pass


if __name__ == '__main__':

    # trainData(useIntegrate = True, platform = PlatformType.Default, problemOrCategoryWise = 1,
    #           modelNumber = 1, mlAlgos = ClassifierType.onlyNonHyperClassifiers, test_size = 0.2,
    #           number_of_top_words = 10)

    trainData(useIntegrate = True, platform = PlatformType.Default, problemOrCategoryWise = 2,
              modelNumber = 1, mlAlgos = ClassifierType.onlyNonHyperClassifiers, test_size = 0.2,
              number_of_top_words = 10)


    # test_sizeList = [0.1, 0.2, 0.3, 0.4, 0.5]
    # for test_size in testsizeList:
    #     pass