import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import numpy as np

style.use('fivethirtyeight')
colors = ['y', 'g']
axes = ['sub_size', 'time_limit']
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel(axes[0])
ax.set_ylabel(axes[1])

df = pd.read_csv('dp_dataset.csv')
# print df.head()

x1 = np.array(df[axes[0]]).astype(float)
x2 = np.array(df[axes[1]]).astype(float)
y = np.array(df['class']).astype(float)

for i in range(len(y)):
    if x1[i] < 400:
        plt.scatter(x1[i], x2[i], color=colors[int(y[i])])

plt.show()