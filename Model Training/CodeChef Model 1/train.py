from sklearn import neighbors, svm
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
import pandas
import sys, pickle
from generate_dataset import generate
sys.path.append('../Utilities')
from constants import categories, performance_metric_keys

test_size = 0.5 #default value
with open('test_size.pickle') as f:
    test_size = pickle.load(f)

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

def train_for_category(category, classifier):

    df = pandas.read_csv('data/' + category + '/' + 'dataset.csv')
    X = np.array(df.drop(['class', 'sub_size', 'time_limit'], 1)).astype(float)
    y = np.array(df['class']).astype(int)

    X_train = X[:-int(len(X)*test_size)]
    y_train = y[:-int(len(y)*test_size)]

    X_test = X[-int(len(X)*test_size):]
    y_test = y[-int(len(y)*test_size):]

    if classifier == 'KNN':
        clf = neighbors.KNeighborsClassifier()
    elif classifier == 'SVM':
        clf = svm.SVC(probability=True)
    else: print "Enter valid classifier"
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)
    print "accuracy : " + str(accuracy)

    fCapX = np.empty([len(X_test), 1])
    fX = np.empty([len(X_test), 1])
    y_predictions = []
    for i in range(len(X_test)):
        current_prediction =  clf.predict_proba(X_test[i].reshape(1, -1))
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
            else :
                count_metrics['fp'] += 1
        else :
            if y_test[i] == 1:
                count_metrics['fn'] += 1
            else :
                count_metrics['tn'] += 1

    print count_metrics

    performance_metrics =  precision_recall_fscore_support(np.array(y_test), np.array(y_predictions))

    print "precision : " + str(performance_metrics[performance_metric_keys['precision']])
    print "recall : " + str(performance_metrics[performance_metric_keys['recall']])
    print "fscore : " + str(performance_metrics[performance_metric_keys['fscore']])

    with open('model/' + category, 'w') as f:
        pickle.dump(clf, f)

    write_performance_matrix(category, count_metrics, performance_metrics, bias, variance)
    return performance_metrics[performance_metric_keys['fscore']][0], count_metrics

    

def write_performance_matrix(category, count_metrics, performance_metrics, bias, variance):
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


def train_all_models():
    
    with open('accuracy.csv', 'w') as f:
        f.write('category,tp,fp,tn,fn,precision,recall,fscore,bias,variance')
        f.write('\n')
    
    for c in categories:
        generate(c)
        train_for_category(c, 'KNN')


if __name__ == '__main__':
    train_all_models()
    # generate('greedy')
    # train_for_category('greedy', 'KNN')
