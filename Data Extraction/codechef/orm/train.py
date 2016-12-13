from sklearn import neighbors, svm
import numpy as np
import pandas

df = pandas.read_csv('dp_dataset.csv')
test_size = 0.2

X = np.array(df.drop(['class'], 1))
y = np.array(df['class'])

X_train = X[:-int(len(X)*test_size)]
y_train = y[:-int(len(y)*test_size)]

X_test = X[-int(len(X)*test_size):]
y_test = y[-int(len(y)*test_size):]

clf = neighbors.KNeighborsClassifier()
# clf = svm.SVC()
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print accuracy