from sklearn import neighbors, svm, tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
# from sklearn.exceptions import ConvergenceWarning
import numpy as np
import pandas
import sys
import os
import pickle
import operator
import warnings
from generate_problems_dataset import generateLazyLoad

sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn')

from constants import performance_metric_keys, ClassifierType, problemOrCategoryKeys, \
    PlatformType, Metrics, defaultTestSize
from hpsklearn import HyperoptEstimator, any_classifier, knn, svc, random_forest
from hyperopt import tpe
from get_probs import get_all_probs_without_category_NA


# with open('test_size.pickle') as f:
#     test_size = pickle.load(f)

def calculateExpectedValue(valuesAsNumpyArray):
    return np.mean(valuesAsNumpyArray)


def calculateBias(fX, fCapX):
    errors = np.array([])
    for i in range(len(fX)):
        errors = np.append(errors, abs(fCapX[i] - fX[i]))
    return calculateExpectedValue(errors)


def calculateVariance(fX, fCapX):
    squaredFCaps = fCapX ** 2
    return calculateExpectedValue(squaredFCaps) - (calculateExpectedValue(fCapX) ** 2)


def calculateTotalError(fX, fCapX):
    errors = np.array([])
    for i in range(len(fX)):
        errors = np.append(errors, (fCapX[i] - fX[i]) ** 2)
    return np.mean(errors)


def calculateIrreducibleError(fX, fCapX):
    return calculateTotalError(fX, fCapX) - (calculateBias(fX, fCapX) ** 2) - calculateVariance(fX, fCapX)


def train_for_categoryModel1(category, classifier, uniqueFileConvention, dataFileConvention, test_size=defaultTestSize):
    modelFileConvention = uniqueFileConvention + '_' + category + '_' + str(test_size)\
                          + '_' + ClassifierType.classifierTypeString[classifier]
    df = pandas.read_csv('data/' + category + '/' + dataFileConvention + '_dataset.csv')
    X = np.array(df.drop(['class', 'sub_size', 'time_limit'], 1)).astype(float)
    y = np.array(df['class']).astype(int)

    X_train = X[:-int(len(X) * test_size)]
    y_train = y[:-int(len(y) * test_size)]
    X_test = X[-int(len(X) * test_size):]
    y_test = y[-int(len(y) * test_size):]

    if classifier == ClassifierType.KNN:
        clf = neighbors.KNeighborsClassifier()
    elif classifier == ClassifierType.SVM:
        clf = svm.SVC(probability=True)
    elif classifier == ClassifierType.DECISIONTREE:
        clf = tree.DecisionTreeClassifier()
    elif classifier == ClassifierType.RANDOMFOREST:
        clf = RandomForestClassifier()
    elif classifier == ClassifierType.NAIVEBAYES:
        clf = GaussianNB()
    elif classifier == ClassifierType.HPKNN:
        clf = HyperoptEstimator(classifier=knn('clf'))
    elif classifier == ClassifierType.HPSVM:
        clf = HyperoptEstimator(classifier=svc('clf', max_iter=20000000))
    elif classifier == ClassifierType.HPRANDOMFOREST:
        clf = HyperoptEstimator(classifier=random_forest('clf'))
    elif classifier == ClassifierType.HYPERSKLEARN:
        clf = HyperoptEstimator(classifier=any_classifier('clf'), algo=tpe.suggest, trial_timeout=60)
    else:
        print "Enter valid classifier"

    warnings.filterwarnings("error")
    try:
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)
    except:
        print('got training error')
        m = Metrics(category=category)
        m.isValid = False
        m.invalidityMessage = 'Training Failed'
        return m
    warnings.filterwarnings("always")
    print("Classifier trained")

    if classifier == ClassifierType.HYPERSKLEARN:
        print('Best model is ' + str(clf.best_model()))
    print "accuracy : " + str(accuracy)

    fCapX = np.array([])
    fX = np.array([])
    y_predictions = []
    print("Predictions started")

    if classifier == ClassifierType.HYPERSKLEARN or classifier in ClassifierType.onlyHyperClassifiers:
        y_predictions = clf.predict(X_test)
        print(type(y_predictions))
        print(str(y_predictions.shape))
        for i in range(len(X_test)):
            fCapX = np.append(fCapX, y_predictions[i])
            fX = np.append(fX, y_test[i])
    else:
        for i in range(len(X_test)):
            current_prediction = clf.predict_proba(X_test[i].reshape(1, -1))
            y_predictions.append(0 if current_prediction[0][0] > 0.5 else 1)
            fCapX = np.append(fCapX, current_prediction[0][1])
            fX = np.append(fX, y_test[i])

    bias = calculateBias(fX, fCapX)
    variance = calculateVariance(fX, fCapX)
    totalError = calculateTotalError(fX, fCapX)
    irreducibleError = calculateIrreducibleError(fX, fCapX)

    print("Bias Variance Calculated")
    print('Total Error: ' + str(totalError))
    print('Bias: ' + str(bias))
    print('Variance: ' + str(variance))
    print('Irreducible Error: ' + str(irreducibleError))

    count_metrics = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
    for i in range(len(y_test)):
        if y_predictions[i] == 1:
            if y_test[i] == 1:
                count_metrics['tp'] += 1
            else:
                count_metrics['fp'] += 1
        else:
            if y_test[i] == 1:
                count_metrics['fn'] += 1
            else:
                count_metrics['tn'] += 1

    warnings.filterwarnings("error")
    try:
        performance_metrics = precision_recall_fscore_support(np.array(y_test), np.array(y_predictions))
    except:
        print('performance metrics not valid')
        m = Metrics(category=category)
        m.isValid = False
        m.invalidityMessage = 'Performance metrics invalid'
        return m
    warnings.filterwarnings("always")

    print "precision : " + str(performance_metrics[performance_metric_keys['precision']])
    print "recall : " + str(performance_metrics[performance_metric_keys['recall']])
    print "fscore : " + str(performance_metrics[performance_metric_keys['fscore']])

    # Here uniqueFileConvention that we get from function call has actually appended,
    # '_' + category, at its end
    with open('model/' + modelFileConvention + '.pickle', 'w') as f:
        print('Dumping model: ' + 'model/' + modelFileConvention + '.pickle')
        pickle.dump(clf, f)

    return Metrics(category=category, truePositive=count_metrics['tp'], trueNegative=count_metrics['tn'],
                   falsePositive=count_metrics['fp'], falseNegative=count_metrics['fn'],
                   precision=performance_metrics[performance_metric_keys['precision']],
                   recall=performance_metrics[performance_metric_keys['recall']],
                   fScore=performance_metrics[performance_metric_keys['fscore']],
                   bias=bias, variance=variance, irreducibleError=irreducibleError, totalError=totalError)


def train_for_categoryModel2(category, classifier, uniqueFileConvention, dataFileConvention, test_size=defaultTestSize):
    dataFileConvention = dataFileConvention + '_' + category + '_' + str(test_size)
    modelFileConvention = uniqueFileConvention + '_' + category + '_' + str(test_size)\
                          + '_' + ClassifierType.classifierTypeString[classifier]
    df = pandas.read_csv('data/' + category + '/' + dataFileConvention + '_dataset.csv')
    df1 = df.ix[:, :-1]
    df2 = df.ix[:, -1:]

    # print 'DataFrame Shape: '+str(df1.shape)
    # print 'DataFrame2 Shape: '+str(df2.shape)

    X = np.array(df1)
    y = np.array(df2)
    X_train = X[:-int(len(X) * test_size)]
    y_train = y[:-int(len(y) * test_size)]

    X_test = X[-int(len(X) * test_size):]
    y_test = y[-int(len(y) * test_size):]

    if classifier == ClassifierType.KNN:
        clf = neighbors.KNeighborsClassifier()
    elif classifier == ClassifierType.SVM:
        clf = svm.SVC(probability=True)
    elif classifier == ClassifierType.DECISIONTREE:
        clf = tree.DecisionTreeClassifier()
    elif classifier == ClassifierType.RANDOMFOREST:
        clf = RandomForestClassifier()
    elif classifier == ClassifierType.NAIVEBAYES:
        clf = GaussianNB()
    elif classifier == ClassifierType.HPKNN:
        clf = HyperoptEstimator(classifier=knn('clf'))
    elif classifier == ClassifierType.HPSVM:
        clf = HyperoptEstimator(classifier=svc('clf', max_iter=20000000))
    elif classifier == ClassifierType.HPRANDOMFOREST:
        clf = HyperoptEstimator(classifier=random_forest('clf'))
    elif classifier == ClassifierType.HYPERSKLEARN:
        clf = HyperoptEstimator(classifier=any_classifier('clf'), algo=tpe.suggest, trial_timeout=60)
    else:
        clf = None
        print "Enter valid classifier"

    warnings.filterwarnings("error")
    try:
        print('Classifier Training started')
        clf.fit(X_train, y_train.ravel())
        accuracy = clf.score(X_test, y_test.ravel())
    except Exception as e:
        print('got training error')
        print e
        m = Metrics(category=category)
        m.isValid = False
        m.invalidityMessage = 'Training Failed'
        return m
    warnings.filterwarnings("always")

    print("Classifier trained")

    if classifier == ClassifierType.HYPERSKLEARN:
        print('Best model is ' + str(clf.best_model()))
    print "accuracy : " + str(accuracy)

    fCapX = np.array([])
    fX = np.array([])
    y_predictions = []
    print("Predictions started")

    if classifier == ClassifierType.HYPERSKLEARN or classifier in ClassifierType.onlyHyperClassifiers:
        y_predictions = clf.predict(X_test)
        print(type(y_predictions))
        print(str(y_predictions.shape))
        for i in range(len(X_test)):
            fCapX = np.append(fCapX, y_predictions[i])
            fX = np.append(fX, y_test[i])
    else:
        for i in range(len(X_test)):
            current_prediction = clf.predict_proba(X_test[i].reshape(1, -1))
            y_predictions.append(0 if current_prediction[0][0] > 0.5 else 1)
            fCapX = np.append(fCapX, current_prediction[0][1])
            fX = np.append(fX, y_test[i])

    bias = calculateBias(fX, fCapX)
    variance = calculateVariance(fX, fCapX)
    totalError = calculateTotalError(fX, fCapX)
    irreducibleError = calculateIrreducibleError(fX, fCapX)

    print("Bias Variance Calculated")
    print('Total Error: ' + str(totalError))
    print('Bias: ' + str(bias))
    print('Variance: ' + str(variance))
    print('Irreducible Error: ' + str(irreducibleError))

    count_metrics = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
    for i in range(len(y_test)):
        if y_predictions[i] == 1:
            if y_test[i] == 1:
                count_metrics['tp'] += 1
            else:
                count_metrics['fp'] += 1
        else:
            if y_test[i] == 1:
                count_metrics['fn'] += 1
            else:
                count_metrics['tn'] += 1

    warnings.filterwarnings("error")
    try:
        performance_metrics = precision_recall_fscore_support(np.array(y_test), np.array(y_predictions))
    except:
        print('performance metrics not valid')
        m = Metrics(category=category)
        m.isValid = False
        m.invalidityMessage = 'Performance metrics invalid'
        return m
    warnings.filterwarnings("always")

    print "precision : " + str(performance_metrics[performance_metric_keys['precision']])
    print "recall : " + str(performance_metrics[performance_metric_keys['recall']])
    print "fscore : " + str(performance_metrics[performance_metric_keys['fscore']])

    if not os.path.exists('model'):
        os.makedirs('model')
    with open('model/' + modelFileConvention + '.pickle', 'w') as f:
        print('Dumping model: ' + 'model/' + modelFileConvention + '.pickle')
        pickle.dump(clf, f)

    return Metrics(category=category, truePositive=count_metrics['tp'], trueNegative=count_metrics['tn'],
                   falsePositive=count_metrics['fp'], falseNegative=count_metrics['fn'],
                   precision=performance_metrics[performance_metric_keys['precision']],
                   recall=performance_metrics[performance_metric_keys['recall']],
                   fScore=performance_metrics[performance_metric_keys['fscore']],
                   bias=bias, variance=variance, irreducibleError=irreducibleError, totalError=totalError)


def get_accuracy(categories, classifier, uniqueFileConvention, useIntegrated=True, platform=PlatformType.Default,
                 modelNumber=1, test_size=defaultTestSize):
    preds_for_prob = {}
    ans_for_prob = {}

    for category in categories:
        print('Processing for category: ' + category)
        dataFileConvention = uniqueFileConvention + '_' + category + '_' + str(test_size)
        modelFileConvention = uniqueFileConvention + '_' + category + '_' + str(test_size) + '_' + \
                              ClassifierType.classifierTypeString[classifier]
        if not os.path.isfile("data/" + category + "/" + dataFileConvention + "_dataset.csv"):
            print('File does not exist: ' + 'data/' + category + '/' + dataFileConvention + '_dataset.csv')
            print('Generating dataset file')
            generateLazyLoad(useIntegrated=useIntegrated, category=category, platform=platform,
                             uniqueFileConvention=uniqueFileConvention, shouldShuffle=False,
                             test_size=test_size)
        df = pandas.read_csv("data/" + category + "/" + dataFileConvention + "_dataset.csv")
        X = np.array(df.drop(['class', 'sub_size', 'time_limit'], 1)).astype(float)
        y = np.array(df['class']).astype(int)

        X_test = X[-int(len(X) * test_size):]
        y_test = y[-int(len(y) * test_size):]

        if not os.path.isfile('model/' + modelFileConvention + '.pickle'):
            print('Model does not exist: ' 'model/' + modelFileConvention + '.pickle')
            print('Training dataset for building model')
            metrics = train_for_categoryModel1(category=category, classifier=classifier, uniqueFileConvention=uniqueFileConvention,
                                               test_size=test_size)
            if not metrics.isValid:
                return -1.0
        with open('model/' + modelFileConvention + '.pickle') as f:
            clf = pickle.load(f)

        # y_predictions = []
        for i in range(len(X_test)):
            if i not in preds_for_prob.keys():
                preds_for_prob[i] = {}

            if i not in ans_for_prob.keys():
                ans_for_prob[i] = []

            current_prediction = clf.predict_proba(X_test[i].reshape(1, -1))
            # print str(current_prediction[0][0]) + " " + str(current_prediction[0][1]) + '\t' + str(y_test[i]
            # y_predictions.append(current_prediction[0][1])
            preds_for_prob[i][category] = float(
                current_prediction[0][1])  # class 1 confidence i.e confidence for category c

            if y_test[i] == 1:
                ans_for_prob[i].append(category)

        print('=================== CATEGORY OVER ===================')
    correct = 0
    for i in range(len(X_test)):
        sorted_category_perc = sorted(preds_for_prob[i].items(), key=operator.itemgetter(1))
        sorted_category_perc.reverse()  # desc

        for j in range(3):
            if sorted_category_perc[j][0] in ans_for_prob[i]:
                correct += 1
                # print (sorted_category_perc[j][0] + " => " + str(ans_for_prob[i]))
                break

    accuracy = str(correct * 1.0 / len(X_test))
    print('accuracy = ' + str(accuracy))
    return accuracy


def baggingBasedTraining(categories, classifiers, uniqueFileConvention, dataFileConvention, useIntegrated=True,
                         platform=PlatformType.Default, test_size=defaultTestSize):

    #Preprocessing Models
    classifierCategoryMapToModels = {}
    for classifier in classifiers:
        categoryMapToModels = {}
        for category in categories:
            print('Processing for category: ' + category)
            modelFileConvention = uniqueFileConvention + '_' + category + '_' + str(test_size) + '_' + \
                                  ClassifierType.classifierTypeString[classifier]
            tempDataFileConv = dataFileConvention + '_notShuffled' + '_' + category + '_' + str(test_size)
            if not os.path.isfile("data/" + category + "/" + tempDataFileConv + "_dataset.csv"):
                print('File does not exist: ' + 'data/' + category + '/' + tempDataFileConv + '_dataset.csv')
                print('Generating dataset file')
                generateLazyLoad(useIntegrated=useIntegrated, category=category, platform=platform,
                                 uniqueFileConvention=uniqueFileConvention, dataFileConvention=tempDataFileConv,
                                 shouldShuffle=False, test_size=test_size)

            if not os.path.isfile('model/' + modelFileConvention + '.pickle'):
                print('Model does not exist: ' 'model/' + modelFileConvention + '.pickle')
                print('Training dataset for building model')
                metrics = train_for_categoryModel1(category=category, classifier=classifier,uniqueFileConvention=uniqueFileConvention,
                                                   dataFileConvention = dataFileConvention, test_size=test_size)

            with open('model/' + modelFileConvention + '.pickle') as f:
                clf = pickle.load(f)
            categoryMapToModels[category] = clf

        classifierCategoryMapToModels[ClassifierType.classifierTypeString[classifier]] = categoryMapToModels

    probs = get_all_probs_without_category_NA(False, PlatformType.Codechef)
    test_probs = probs[-int(test_size*len(probs)):]
    for prob in test_probs:
        for classifierString in classifierCategoryMapToModels:
            for cat in classifierCategoryMapToModels[classifierString]:





def createFeaturesForProbByCategory(prob, category):
    description = transform_description.transform(prob.description)
    filePath = '../Model Training/Integrated Model 1/data/' + category + '/'
    # filePath = 'data/'+category+'/'
    features = []
    with open(filePath + 'dataset.csv') as f:

        with open(filePath + 'feature_size.pickle') as fs:
            feature_size = pickle.load(fs)
            print ('\n\n\n\tfeature size for ' + str(category) + ' : ' + str(feature_size))

        featureWords = f.readline().split(',')[0: -3]
        for word in featureWords:
            if description.count(word) > 0:
                features.append(1)
            else:
                features.append(0)
    return features

