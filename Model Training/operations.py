from sklearn import neighbors, svm, tree
from sklearn.naive_bayes import  GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.exceptions import ConvergenceWarning
import numpy as np
import pandas
import sys
import os
import pickle
import operator
import warnings
from generate_dataset import generate, generateLazyLoad
sys.path.append('Utilities/')
sys.path.append('../hyperopt-sklearn')
from constants import performance_metric_keys, ClassifierType, allClassifierTypes,\
                problemOrCategoryKeys, PlatformType,\
                onlyNonHyperClassifiers, onlyHyperClassifiers, PlatformType, Metrics
from hpsklearn import HyperoptEstimator, any_classifier, knn, svc, random_forest
from hyperopt import tpe


test_size = 0.5 #default value
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
    squaredFCaps = fCapX**2
    return calculateExpectedValue(squaredFCaps) - (calculateExpectedValue(fCapX)**2)

def calculateTotalError(fX, fCapX):
    errors = np.array([])
    for i in range(len(fX)):
        errors = np.append(errors, (fCapX[i] - fX[i])**2)
    return np.mean(errors)

def calculateIrreducibleError(fX, fCapX):
    return calculateTotalError(fX, fCapX) - (calculateBias(fX, fCapX)**2) - calculateVariance(fX, fCapX)


def train_for_categoryModel1(category, classifier, platform, dataFileNamesHash):
    df = pandas.read_csv('data/' + category + '/' + dataFileNamesHash + '_dataset.csv')
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

    if classifier == ClassifierType.HYPERSKLEARN or classifier in onlyHyperClassifiers:
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

    with open('model/' + dataFileNamesHash + '_' + ClassifierType.classifierTypeString[classifier]
                      + category + '.pickle', 'w') as f:
        pickle.dump(clf, f)

    return Metrics(category=category, truePositive=count_metrics['tp'], trueNegative=count_metrics['tn'],
                   falsePositive=count_metrics['fp'], falseNegative=count_metrics['fn'],
                   precision=performance_metrics[performance_metric_keys['precision']],
                   recall=performance_metrics[performance_metric_keys['recall']],
                   fScore=performance_metrics[performance_metric_keys['fscore']],
                   bias=bias, variance=variance, irreducibleError=irreducibleError, totalError=totalError)


def get_accuracy(categories, classifier, dataFileNamesHash, useIntegrated=True, platform=PlatformType.Default, modelNumber=1):
    preds_for_prob = {}
    ans_for_prob = {}

    for category in categories:
        if not os.path.isfile('data/' + category + '/' + dataFileNamesHash + '_dataset.csv'):
            generateLazyLoad(useIntegrated=useIntegrated, category=category, platform=platform,
                             dataFilesNameHash=(dataFileNamesHash + '_' + category), shouldShuffle=False)
        df = pandas.read_csv('data/' + category + '/' + dataFileNamesHash + '_dataset.csv')
        X = np.array(df.drop(['class', 'sub_size', 'time_limit'], 1)).astype(float)
        y = np.array(df['class']).astype(int)

        X_test = X[-int(len(X) * test_size):]
        y_test = y[-int(len(y) * test_size):]

        if not os.path.isfile('model/' + dataFileNamesHash + '_' + ClassifierType.classifierTypeString[classifier]
                      + category + '.pickle'):
            train_for_categoryModel1(category=category, classifier=classifier, platform=platform,
                                     dataFileNamesHash=dataFileNamesHash)

        with open('model/' + dataFileNamesHash + '_' + ClassifierType.classifierTypeString[classifier]
                      + category + '.pickle') as f:
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
            preds_for_prob[i][category] = float(current_prediction[0][1])  # class 1 confidence i.e confidence for category c

            if y_test[i] == 1:
                ans_for_prob[i].append(category)

    correct = 0
    for i in range(len(X_test)):
        sorted_category_perc = sorted(preds_for_prob[i].items(), key=operator.itemgetter(1))
        sorted_category_perc.reverse()  # desc

        for j in range(3):
            if sorted_category_perc[j][0] in ans_for_prob[i]:
                correct += 1
                print (sorted_category_perc[j][0] + " => " + str(ans_for_prob[i]))
                break

    print('accuracy = ' + str(correct * 1.0 / len(X_test)))
