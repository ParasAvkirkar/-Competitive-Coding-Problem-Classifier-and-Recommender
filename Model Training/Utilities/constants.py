from enum import Enum

test_size = 0.0
defaultTestSize = 0.5

categoryWiseWeights = {'math':1, 'combinatorics':1000, 'tree':1000000,
                       'greedy':1000000000, 'dp':1000000000000, 'graph':1000000000000000}
categories = ['graph', 'tree', 'combinatorics', 'math', 'dp', 'greedy']

'''
codechef
    greedy
    graph
    tree -> trees, tree
    combinatorics
    math -> maths
    dp

codeforces
    greedy
    graph -> graph, graphs
    tree -> trees
    combinatorics
    math
    dp
'''

# For each level in codechef, we had defined weights for that level
codechefDifficultyLevels = {'easy':1, 'medium':1000, 'hard':1000000}

classifierTypes = ['KNN', 'SVM', 'DECISIONTREE', 'RANDOMFOREST', 'NAIVEBAYES',
                   'HPKNN', 'HPSVM', 'HPRANDOMFOREST', 'HYPERSKLEARN']

problemOrCategoryKeys = {'category': 1, 'problem': 2}

minimum_number_of_probs_inwhich_word_to_exist = 50
performance_metric_keys = {'precision': 0, 'recall': 1, 'fscore': 2}


class PlatformType:
    Default = 0
    Codechef = 1
    Codeforces = 2
    Spoj = 3
    platformString = {Default: 'integrated', Codechef: 'codechef', Codeforces: 'codeforces', Spoj: 'spoj'}


class ClusterMethod:
    KMeans = 1

    allClusteringMethods = [KMeans]
    clusterMethodString = {KMeans: 'KMeans'}

class ClassifierType:
    KNN = 1
    SVM = 2
    DECISIONTREE = 3
    RANDOMFOREST = 4
    NAIVEBAYES = 5
    HPKNN = 6
    HPSVM = 7
    HPRANDOMFOREST = 8
    HYPERSKLEARN = 9
    classifierTypeString = {KNN: 'KNN', SVM: 'SVM', DECISIONTREE: 'DECISIONTREE',
                            RANDOMFOREST: 'RANDOMFOREST', NAIVEBAYES: 'NAVIBAYES',
                            HPKNN: 'HPKNN', HPSVM: 'HPSVM', HPRANDOMFOREST: 'HPRANDOMFOREST',
                            HYPERSKLEARN: 'HYPERSKLEARN'}


    allClassifierTypes = [KNN, SVM, DECISIONTREE,
                          RANDOMFOREST, NAIVEBAYES, HPKNN,
                          HPSVM, HPRANDOMFOREST, HYPERSKLEARN]
    
    onlyNonHyperClassifiers = [KNN, SVM, DECISIONTREE,
                               RANDOMFOREST, NAIVEBAYES]
    
    onlyHyperClassifiers = [HPKNN, HPSVM, HPRANDOMFOREST,
                            HYPERSKLEARN]


class Metrics:
    def __init__(self, category='', truePositive=0, trueNegative=0, falsePositive=0, falseNegative=0,
                 precision=0.0, recall=0.0, fScore=0.0, bias=0.0, variance=0.0, irreducibleError=0.0,
                 totalError=0.0, isValid=True, invalidityMessage=''):
        self.category = category
        self.truePositive = truePositive
        self.trueNegative = trueNegative
        self.falsePositive = falsePositive
        self.falseNegative = falseNegative
        self.precision = precision
        self.recall = recall
        self.fScore = fScore
        self.bias = bias
        self.variance = variance
        self.irreducibleError = irreducibleError
        self.totalError = totalError
        self.isValid = isValid
        self.invalidityMessage = invalidityMessage

    def __str__(self):
        return 'Precision: '+str(self.precision[1]) + ' Recall: ' + str(self.recall[1]) + ' F1:' + str(self.fScore[1])

    @staticmethod
    def writeMultipleMetics(metricsFileName, classifierMetricsMap, isPositiveBased=True):
        performanceMetricIndex = 1 if isPositiveBased else 0
        with open(metricsFileName, 'w') as f:
            for classifier in classifierMetricsMap:
                f.write(ClassifierType.classifierTypeString[classifier] + '\n')
                f.write('category,'
                        + 'tp,fp,tn,fn,'
                        + 'precision,recall,fscore,'
                        + 'bias,variance,total error,irreducible error' + '\n')
                metricsList = classifierMetricsMap[classifier]
                for metric in metricsList:
                    if metric.isValid:
                        f.write(metric.category
                                + ',' + str(metric.truePositive)
                                + ',' + str(metric.falsePositive)
                                + ',' + str(metric.trueNegative)
                                + ',' + str(metric.falseNegative)
                                + ',' + str(metric.precision[performanceMetricIndex])
                                + ',' + str(metric.recall[performanceMetricIndex])
                                + ',' + str(metric.fScore[performanceMetricIndex])
                                + ',' + str(metric.bias)
                                + ',' + str(metric.variance)
                                + ',' + str(metric.totalError)
                                + ',' + str(metric.irreducibleError)
                                + '\n')
                    else:
                        f.write(metric.category + ',' + metric.invalidityMessage + '\n')
            print('Metrics written to file: '+metricsFileName)

    @staticmethod
    def writeMultipleProblemwiseMetics(metricsFileName, classifierMetricsMap):
        with open(metricsFileName, 'w') as f:
            f.write('classifier,accuracy\n')
            for classifier in classifierMetricsMap:
                f.write(ClassifierType.classifierTypeString[classifier] + ','
                        + str(classifierMetricsMap[classifier])
                        + '\n')
            print('Metrics written to file: ' + metricsFileName)
            print(ClassifierType.classifierTypeString[classifier] + ' ' + str(classifierMetricsMap[classifier]))

    @staticmethod
    def writeBaggedMetrics(metricsFileName, accuracy):
        with open(metricsFileName, 'w') as f:
            f.write('accuracy,'+str(accuracy)+'\n')
            print('Metrics written to file: ' + metricsFileName)


    def __str__(self):
        return ''


