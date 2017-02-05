import os, sys
import pickle
from train import train_for_category, generate
import matplotlib.pyplot as plt
from matplotlib import style
import csv

style.use('fivethirtyeight')

try:
    with open('num_of_top_words_as_feature.pickle') as f:
        num_of_top_words_as_feature = pickle.load(f) 
except:
    with open('num_of_top_words_as_feature.pickle', 'w+b') as f:
        num_of_top_words_as_feature = 10
        pickle.dump(num_of_top_words_as_feature, f)

num_to_score = {}
num_to_count_matrix = {}
category = 'dp'
window = {'lower':10, 'upper':51}

f1_file = open('all_f1_scores.csv', 'wb')
f1_writer = csv.writer(f1_file, delimiter=',')

header = ['test size'] + [i for i in range(window['lower'], window['upper']) ]
f1_writer.writerow(header)

for tsize in range(10, 60, 10):
	with open('test_size.pickle', 'w+b') as f:
		test_size = tsize * 0.01
		pickle.dump(test_size, f)

	f1_values = []

	for i in range(window['lower'], window['upper']):
		with open('num_of_top_words_as_feature.pickle', 'w+b') as f:
			num_of_top_words_as_feature = i
			pickle.dump(num_of_top_words_as_feature, f)
		
		generate(category)
		fscore, cm = train_for_category(category, 'KNN')
		num_to_score[i] = fscore
		num_to_count_matrix[i] = cm

		f1_values.append( num_to_score[i] )

	f1_writer.writerow([tsize]+f1_values)

print num_to_score
print num_to_count_matrix

f1_file.close()

# axes = ['train_word_size', 'f1-score']
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xlabel(axes[0])
# ax.set_ylabel(axes[1])

# plt.plot([i for i in num_to_score], [num_to_score[i] for i in num_to_score])
# # plt.show()

# f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex = 'col', sharey = 'row')
# # plt.subplot(221)
# ax1.plot([i for i in num_to_count_matrix], [num_to_count_matrix[i]['tp'] for i in num_to_count_matrix])

# # plt.subplot(222)
# ax2.plot([i for i in num_to_count_matrix], [num_to_count_matrix[i]['fp'] for i in num_to_count_matrix])

# # plt.subplot(223)
# ax3.plot([i for i in num_to_count_matrix], [num_to_count_matrix[i]['fn'] for i in num_to_count_matrix])

# # plt.subplot(224)
# ax4.plot([i for i in num_to_count_matrix], [num_to_count_matrix[i]['tn'] for i in num_to_count_matrix])

# plt.show()