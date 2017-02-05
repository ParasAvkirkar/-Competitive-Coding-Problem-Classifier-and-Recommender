mport pickle

with open('num_of_top_words_as_feature.pickle') as f:
	print f.name
	num_of_top_words_as_feature = pickle.load(f)
	print num_of_top_words_as_feature
	
# with open('num_of_top_words_as_feature.pickle', 'w+b') as f:
#     num_of_top_words_as_feature = 10
#     pickle.dump(num_of_top_words_as_feature, f)

