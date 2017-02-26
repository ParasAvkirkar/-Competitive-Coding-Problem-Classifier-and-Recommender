import random

import sys
sys.path.append('Utilities/')
from constants import minimum_number_of_probs_inwhich_word_to_exist


def train_test_split(probs, test_size, shouldShuffle=True):
    if shouldShuffle:
        random.shuffle(probs)

    train_set = probs[ : -int(test_size*len(probs))]
    test_set = probs[-int(test_size*len(probs)) : ]

    return train_set, test_set


def get_wordcount_by_category(train_set, category):

    #word count by, no of words in prob_class(e.g dp) problems and in no prob_class(e.g other than dp) problems
    words = {}
    count = 0

    for p in train_set:
        desclist = p.modified_description.split()
        uniqWordList = sorted(set(desclist), key=desclist.index)
        p.modified_description = ' '.join(uniqWordList)

        if category in p.category:
            for w in p.modified_description.split(' '):
                if w not in words:
                    words[w] = {0:0, 1:0}
                    words[w][1] = 1
                else :
                    words[w][1] += 1

            count += 1
        else:
            for w in p.modified_description.split(' '):
                if w not in words:
                    words[w] = {0: 0, 1: 0}
                    words[w][0] = 1
                else :
                    words[w][0] += 1

    # print "\n\n\n\n\n\n\n" + str(count) + "\n\n\n\n\n"
    return words


def get_word_perc(words):
    percent = {}
    word_count = {}
    for w in words:
        if (words[w][0] + words[w][1]) > minimum_number_of_probs_inwhich_word_to_exist: #word should have atleast 50 occurances
            word_count[w] = {}
            word_count[w]['yes'] = words[w][1]
            word_count[w]['no'] = words[w][0]
            word_count[w]['total'] = words[w][0] + words[w][1]
            percent[w] = 100.0 * word_count[w]['yes'] / word_count[w]['total']

    return percent, word_count