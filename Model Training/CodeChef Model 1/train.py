from sklearn import neighbors, svm, tree
from sklearn.naive_bayes import  GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.exceptions import ConvergenceWarning
import numpy as np
import pandas
import sys, pickle
import warnings
from generate_dataset import generate, generateLazyLoad
sys.path.append('../Utilities')
sys.path.append('../../hyperopt-sklearn')
from constants import categories, performance_metric_keys
from hpsklearn import HyperoptEstimator, any_classifier, knn, svc, random_forest
from hyperopt import tpe


test_size = 0.5 #default value
with open('test_size.pickle') as f:
    test_size = pickle.load(f)

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

def train_for_category(category, classifier):
    np.set_printoptions(threshold='nan')
    df = pandas.read_csv('data/' + category + '/' + 'dataset.csv')
    X = np.array(df.drop(['class', 'sub_size', 'time_limit'], 1)).astype(float)
    # X = np.array(df.drop(['class'], 1)).astype(float)
    # print(X)
    y = np.array(df['class']).astype(int)

    X_train = X[:-int(len(X)*test_size)]
    y_train = y[:-int(len(y)*test_size)]

    X_test = X[-int(len(X)*test_size):]
    y_test = y[-int(len(y)*test_size):]
    print(str(X_test.shape))

    if classifier == 'KNN':
        clf = neighbors.KNeighborsClassifier()
    elif classifier == 'SVM':
        clf = svm.SVC(probability=True)
    elif classifier == 'DECISIONTREE':
        clf = tree.DecisionTreeClassifier()
    elif classifier == 'RANDOMFOREST':
        clf = RandomForestClassifier()
    elif classifier == 'NAIVEBAYES':
        clf = GaussianNB()
    elif classifier == 'HPKNN':
        clf = HyperoptEstimator(classifier=knn('clf'))
    elif classifier == 'HPSVM':
        clf = HyperoptEstimator(classifier=svc('clf', max_iter=20000000))
    elif classifier == 'HPRANDOMFOREST':
        clf = HyperoptEstimator(classifier=random_forest('clf'))
    elif classifier == 'HYPERSKLEARN':
        clf = HyperoptEstimator(classifier=any_classifier('clf'), algo=tpe.suggest, trial_timeout=60)
    else:
        print "Enter valid classifier"

    warnings.filterwarnings("error")
    try:
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)
    except:
        print('got training error')
        with open('accuracy.csv', 'a') as f:
            f.write(category
                    + ',' + 'training or accuracy testing failed')

            f.write('\n')
            return

    print("Classifier trained")


    if classifier == 'HYPERSKLEARN':
        print('Best model is '+str(clf.best_model()))
    print "accuracy : " + str(accuracy)

    fCapX = np.array([])
    fX = np.array([])
    y_predictions = []
    print("Predictions started")

    if classifier == 'HYPERSKLEARN' or 'HP' in classifier:
        y_predictions = clf.predict(X_test)
        print(type(y_predictions))
        # print(y_predictions)
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
    print('Total Error: '+str(totalError))
    print('Bias: ' + str(bias))
    print('Variance: ' + str(variance))
    print('Irreducible Error: ' + str(irreducibleError))

    count_metrics = {'tp':0, 'fp':0, 'tn':0, 'fn':0}
    for i in range(len(y_test)):
        if y_predictions[i] == 1:
            if y_test[i] == 1:
                count_metrics['tp'] += 1
            else :
                count_metrics['fp'] += 1
        else :
            if y_test[i] == 1:
                count_metrics['fn'] += 1
            else :
                count_metrics['tn'] += 1

    try:
        performance_metrics = precision_recall_fscore_support(np.array(y_test), np.array(y_predictions))
    except:
        print('performance metrics not valid')
        with open('accuracy.csv', 'a') as f:
            f.write(category
                    + ',' + str(count_metrics['tp'])
                    + ',' + str(count_metrics['fp'])
                    + ',' + str(count_metrics['tn'])
                    + ',' + str(count_metrics['fn'])
                    + ',' + 'invalid'
                    + ',' + 'invalid'
                    + ',' + 'invalid'
                    + ',' + str(bias)
                    + ',' + str(variance))
            f.write('\n')
        return

    print "precision : " + str(performance_metrics[performance_metric_keys['precision']])
    print "recall : " + str(performance_metrics[performance_metric_keys['recall']])
    print "fscore : " + str(performance_metrics[performance_metric_keys['fscore']])

    with open('model/' + category, 'w') as f:
        pickle.dump(clf, f)

    write_performance_matrix(category, count_metrics, performance_metrics,
                             bias, variance, totalError, irreducibleError,True)
    print("Performance metrics written to file")
    return performance_metrics[performance_metric_keys['fscore']][0], count_metrics


def write_performance_matrix(category, count_metrics, performance_metrics,
                             bias, variance, totalError, irreducibleError, isPositiveBased=True):
    index = 1 if isPositiveBased else 0
    with open('accuracy.csv', 'a') as f:
        f.write(category
            + ',' + str(count_metrics['tp'])
            + ',' + str(count_metrics['fp'])
            + ',' + str(count_metrics['tn'])
            + ',' + str(count_metrics['fn'])
            + ',' + str(performance_metrics[performance_metric_keys['precision']][index])
            + ',' + str(performance_metrics[performance_metric_keys['recall']][index])
            + ',' + str(performance_metrics[performance_metric_keys['fscore']][index])
            + ',' + str(bias)
            + ',' + str(variance)
            + ',' + str(totalError)
            + ',' + str(irreducibleError))
        f.write('\n')


def train_all_models():
    
    with open('accuracy.csv', 'w') as f:
        f.write('category,tp,fp,tn,fn,precision,recall,fscore,bias,variance,total error,irreducible error')
        f.write('\n')
    
    for c in categories:
        generate(c)
        train_for_category(c, 'KNN')


def train_all_types_of_models():
    classifierTypes = ['KNN', 'SVM', 'DECISIONTREE', 'RANDOMFOREST', 'NAIVEBAYES',
                       'HPKNN', 'HPSVM', 'HPRANDOMFOREST', 'HYPERSKLEARN']

    # classifierTypes = ['HYPERSKLEARN']

    open('accuracy.csv', 'w').close()

    for type in classifierTypes:
        with open('accuracy.csv', 'a') as f:
            f.write(type)
            f.write('\n')
            f.write('category,tp,fp,tn,fn,precision,recall,fscore,bias,variance,total error,irreducible error')
            f.write('\n')
        print ('for classfier '+str(type))
        for c in categories:
            # generateLazyLoad(c)
            generate(c)
            print('for category ' +str(c))
            train_for_category(c, type)


if __name__ == '__main__':
    #train_all_models()
    train_all_types_of_models()
    # generate('greedy')
    # train_for_category('greedy', 'KNN')
