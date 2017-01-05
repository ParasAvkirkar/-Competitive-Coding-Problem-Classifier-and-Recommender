from sklearn import neighbors, svm
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
import pandas

performance_metric_keys = {'precision':0, 'recall':1, 'fscore':2}

df = pandas.read_csv('dp_dataset.csv')
test_size = 0.2

X = np.array(df.drop(['class', 'sub_size', 'time_limit'], 1)).astype(float)
y = np.array(df['class']).astype(int)

X_train = X[:-int(len(X)*test_size)]
y_train = y[:-int(len(y)*test_size)]

X_test = X[-int(len(X)*test_size):]
y_test = y[-int(len(y)*test_size):]

clf = neighbors.KNeighborsClassifier()
# clf = svm.SVC()
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print "accuracy : " + str(accuracy)

y_predictions = []
for i in range(len(X_test)):
    current_prediction =  clf.predict_proba(X_test[i])
    # print str(current_prediction[0][0]) + " " + str(current_prediction[0][1]) + '\t' + str(y_test[i]
    y_predictions.append(0 if current_prediction[0][0] > 0.5 else 1)



count_metrics = {'tp':0, 'fp':0, 'tn':0, 'fn':0}
for i in range(len(y_test)):
    if y_predictions[i] == 1:
        if y_test[i] == 1:
            count_metrics['tp'] += 1
            print 'tp ' + str(y_predictions[i]) + " " + str(y_test[i])
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
