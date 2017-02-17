from sklearn import neighbors, svm
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
import pandas
import sys, pickle
from generate_dataset import generate
import operator
sys.path.append('../Utilities')
from constants import categories, performance_metric_keys

test_size = 0.5 #default value
with open('test_size.pickle') as f:
    test_size = pickle.load(f)


def get_accuracy():

    preds_for_prob = {}
    ans_for_prob = {}
    
    for c in categories:

        df = pandas.read_csv('data/' + c + '/' + 'dataset.csv')
        X = np.array(df.drop(['class', 'sub_size', 'time_limit'], 1)).astype(float)
        y = np.array(df['class']).astype(int)

        X_test = X[-int(len(X)*test_size):]
        y_test = y[-int(len(y)*test_size):]

        with open('model/' + c) as f:
            clf = pickle.load(f)

        # y_predictions = []
        for i in range(len(X_test)):

            if i not in preds_for_prob.keys():
                preds_for_prob[i] = {}

            if i not in ans_for_prob.keys():
                ans_for_prob[i] = []

            current_prediction =  clf.predict_proba(X_test[i].reshape(1, -1))
            # print str(current_prediction[0][0]) + " " + str(current_prediction[0][1]) + '\t' + str(y_test[i]
            # y_predictions.append(current_prediction[0][1])
            preds_for_prob[i][c] = float(current_prediction[0][1]) #class 1 confidence i.e confidence for category c
            
            if y_test[i] == 1:
                ans_for_prob[i].append(c)

    correct = 0
    for i in range(len(X_test)):
        sorted_category_perc = sorted(preds_for_prob[i].items(), key=operator.itemgetter(1))
        sorted_category_perc.reverse() #desc

        for i in range(3):
            if sorted_category_perc[i][0] in ans_for_prob[i]:
                correct += 1
                print (sorted_category_perc[i][0] + " => " + str(ans_for_prob[i]))
                break

    print('accuracy = ' + str(correct * 1.0 / len(X_test)))


if __name__ == '__main__':
    get_accuracy()
