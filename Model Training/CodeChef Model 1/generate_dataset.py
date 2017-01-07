from get_probs import get_probs, get_probs_without_category_NA
from word_count import train_test_split, get_wordcount_by_category, get_word_perc
import operator

import sys
sys.path.append('../Utilities/')
from constants import test_size

def make_csv_files(category, sorted_perc, word_count, percentages):
    with open('data/' + category + '/' + '20feature_word_all_data.csv', 'w') as f:
        for w in sorted_perc[:10]:
            print w[0] + " " + str(word_count[w[0]]['yes']) + " " + str(word_count[w[0]]['no']) + " " + str(
                word_count[w[0]]['total'])
            f.write(w[0] + "," + str(word_count[w[0]]['yes']) + "," + str(word_count[w[0]]['no']) + "," + str(
                word_count[w[0]]['total']))
            f.write('\n')

        print "---------------------------------------------------------"
        for w in sorted_perc[-10:]:
            print w[0] + " " + str(word_count[w[0]]['yes']) + " " + str(word_count[w[0]]['no']) + " " + str(
                word_count[w[0]]['total'])
            f.write(w[0] + "," + str(word_count[w[0]]['yes']) + "," + str(word_count[w[0]]['no']) + "," + str(
                word_count[w[0]]['total']))
            f.write('\n')

    with open('data/' + category + '/' + '20feature_word_percentage.csv', 'w') as f:
        for w in sorted_perc[:10]:
            #word name
            f.write(w[0] + ",")
        f.write('\n')

        for w in sorted_perc[:10]:
            #word perc
            f.write(str(w[1]) + ",")
        f.write('\n')

        for w in sorted_perc[-10:]:
            #word name
            f.write(w[0] + ",")
        f.write('\n')

        for w in sorted_perc[-10:]:
            #word perc
            f.write(str(w[1]) + ",")
        f.write('\n')

    
    with open('data/' + category + '/' + 'word_table.csv', 'w') as f :
        for w in word_count:
            f.write(w + "," + str(word_count[w]['yes']) + "," + str(word_count[w]['no']) + "," + str(word_count[w]['total']) + "," + str(percentages[w]))
            f.write('\n')


def write_dataset(category, sorted_perc, data):
    with open('data/' + category + '/' + 'dataset.csv', 'w') as f:
        f.write(','.join([x[0] for x in sorted_perc[:10]]))
        # print ','.join([x[0] for x in sorted_perc[:10]])

        f.write(',')

        f.write(','.join([x[0] for x in sorted_perc[-10:]]))
        # print ','.join([x[0] for x in sorted_perc[-10:]])

        f.write(',sub_size,time_limit')
        f.write(',class')
        f.write('\n')

        for t in data:
            f.write(','.join([str(x) for x in t]))
            f.write('\n')


#data can be train set or test set
def prepare_dataset(sorted_perc, data, category):
    count = 0
    prepared_data = []

    for p in data:
        prepared_data.append([])
        features = []

        for presentWord in sorted_perc[:10]:
            presentWord = presentWord[0] #it contains tuple of word and percentage, hence [0] element for word

            if presentWord in p.description.split():
                features.append(1)
            else:
                features.append(0)

        for notPresentWord in sorted_perc[-10:]:
            notPresentWord = notPresentWord[0]

            if notPresentWord in p.description.split():
                features.append(1)
            else:
                features.append(0)

        features.append(p.submission_size)
        features.append(p.time_limit[:1])

        if p.category == category:
            features.append(1)
        else : features.append(0)

        prepared_data[count] = features
        count += 1

    return prepared_data


def generate(category):

    probs = get_probs_without_category_NA()

    train_set, test_set = train_test_split(probs, test_size)
    word_cnt_by_cateogry = get_wordcount_by_category(train_set, category)

    percentages, word_cnt_stats = get_word_perc(word_cnt_by_cateogry)

    sorted_perc = sorted(percentages.items(), key=operator.itemgetter(1))
    sorted_perc.reverse() #desc order

    total_data = []
    prepared_train_data = prepare_dataset(sorted_perc, train_set, category)
    prepared_test_data = prepare_dataset(sorted_perc, test_set, category)

    [total_data.append(t) for t in prepared_train_data]
    [total_data.append(t) for t in prepared_test_data]

    make_csv_files(category, sorted_perc, word_cnt_stats, percentages)
    write_dataset(category, sorted_perc, total_data)

if __name__ == '__main__':
    generate('dp')