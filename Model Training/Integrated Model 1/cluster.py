import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

df = pd.read_csv('dp_dataset.csv')

X = np.array(df.drop(['class', 'sub_size', 'time_limit'], 1))
y = np.array(df['class'])

clf = KMeans(n_clusters=2)
clf.fit(X)

print clf.labels_

correct = 0
for i in range(len(X)):
    predict_me = np.array(X[i].astype(float))
    predict_me = predict_me.reshape(-1, len(predict_me))
    xclass = clf.predict(predict_me)
    xclass = xclass[0]

    if y[i] == xclass:
        correct += 1


print 1.0 * correct / len(X)