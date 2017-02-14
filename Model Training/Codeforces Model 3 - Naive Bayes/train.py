from sklearn import neighbors, svm
from sklearn.naive_bayes import  GaussianNB
import numpy as np
import pandas
import pickle, sys
from sklearn.metrics import precision_recall_fscore_support
sys.path.append('../Utilities')
from constants import test_size, categories, performance_metric_keys


def write_performance_matrix(category, count_metrics, performance_metrics):
    with open('accuracy.csv', 'a') as f:
        f.write(category
            + ',' + str(count_metrics['tp'])
            + ',' + str(count_metrics['fp'])
            + ',' + str(count_metrics['tn'])
            + ',' + str(count_metrics['fn'])
            + ',' + str(performance_metrics[performance_metric_keys['precision']][0])
            + ',' + str(performance_metrics[performance_metric_keys['recall']][0])
            + ',' + str(performance_metrics[performance_metric_keys['fscore']][0])
                + ',' + str(bias)
                + ',' + str(variance))

        f.write('\n')

def calculateExpectedValue(valuesAsNumpyArray):
    #return np.std(valuesAsNumpyArray)/(len(valuesAsNumpyArray)**0.5)
    #return np.sum(valuesAsNumpyArray)/len(valuesAsNumpyArray)
    print('mean was '+str(np.mean(valuesAsNumpyArray)) )
    return np.mean(valuesAsNumpyArray)

def calculateBias(fX, fCapX):
    errors = np.empty([len(fX), 1])
    for i in range(len(fX)):
        np.append(errors, fCapX[i] - fX[i])
    return calculateExpectedValue(errors)

def calculateVariance(fX, fCapX):
    squaredFCaps = fCapX**2
    return calculateExpectedValue(squaredFCaps) - (calculateExpectedValue(fCapX)**2)


for category in categories:
    df = pandas.read_csv('data/'+category+'_training.csv')

    df1 = df.ix[:, :-1]
    df2 = df.ix[:, -1:]

    print 'DataFrame Shape: '+str(df1.shape)
    print 'DataFrame2 Shape: '+str(df2.shape)
    # X = np.array(df.drop(['class'], 1))
    # y = np.array(df['class'])

    X = np.array(df1)
    y = np.array(df2)

    X_train = X[:-int(len(X)*test_size)]
    y_train = y[:-int(len(y)*test_size)]

    X_test = X[-int(len(X)*test_size):]
    y_test = y[-int(len(y)*test_size):]

    # clf = neighbors.KNeighborsClassifier()
    #clf = svm.SVC(probability=True)
    clf = GaussianNB()
    clf.fit(X_train, y_train)

    with open('classifier/'+category+'_classifier.pickle', 'wb') as f:
        pickle.dump(clf, f)


    accuracy = clf.score(X_test, y_test)
    print category+" : accuracy - "+str(accuracy)

    fCapX = np.empty([len(X_test), 1])
    fX = np.empty([len(X_test), 1])
    y_predictions = []
    for i in range(len(X_test)):
        current_prediction =  clf.predict_proba(X_test[i])
        # print str(current_prediction[0][0]) + " " + str(current_prediction[0][1]) + '\t' + str(y_test[i]
        y_predictions.append(0 if current_prediction[0][0] > 0.5 else 1)
        np.append(fCapX, y_predictions[-1])
        np.append(fX, y_test[i])

    bias = calculateBias(fX, fCapX)
    variance = calculateVariance(fX, fCapX)

    count_metrics = {'tp':0, 'fp':0, 'tn':0, 'fn':0}
    for i in range(len(y_test)):
        if y_predictions[i] == 1:
            if y_test[i] == 1:
                count_metrics['tp'] += 1
                # print 'tp ' + str(y_predictions[i]) + " " + str(y_test[i])
            else : count_metrics['fp'] += 1
        else :
            if y_test[i] == 1:
                count_metrics['fn'] += 1
            else : count_metrics['tn'] += 1

    print count_metrics

    performance_metrics =  precision_recall_fscore_support(np.array(y_test), np.array(y_predictions))

    print "precision : " + str(performance_metrics[performance_metric_keys['precision']])
    print "recall : " + str(performance_metrics[performance_metric_keys['recall']])
    print "fscore : " + str(performance_metrics[performance_metric_keys['fscore']])

    write_performance_matrix(category, count_metrics, performance_metrics)

