from get_probs import get_all_probs_without_category_NA
from word_count import train_test_split, get_wordcount_by_category, get_word_perc
import operator
import pickle
import numpy as np
import sys, csv, os, random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
import time

sys.path.append('Utilities/')
from constants import categories, performance_metric_keys, ClassifierType, problemOrCategoryKeys, \
    PlatformType, defaultTestSize


def get_num_of_top_words_as_feature(dataFileConvention):
    print('Getting number of top words')
    try:
        with open('data/' + dataFileConvention + '_num_of_top_words_as_feature.pickle') as f:
            num_of_top_words_as_feature = pickle.load(f)
            # print "\n\n\n\n num_of_top_words_as_feature = " + str(num_of_top_words_as_feature) + "\n\n\n\n"
    except:
        with open('data/' + dataFileConvention + '_num_of_top_words_as_feature.pickle', 'w') as f:
            num_of_top_words_as_feature = 10
            pickle.dump(num_of_top_words_as_feature, f)
            # print "\n\n\n\n exception in num of top words as feature, using default size of 10\n\n\n\n"

    return num_of_top_words_as_feature


def make_csv_files(category, sorted_perc, word_count, percentages, dataFileConvention):
    num_of_top_words_as_feature = get_num_of_top_words_as_feature(dataFileConvention)

    with open('data/' + category + '/' + dataFileConvention + '_20feature_word_all_data' + '.csv', 'w') as f:
        for w in sorted_perc[:num_of_top_words_as_feature]:
            # print w[0] + " " + str(word_count[w[0]]['yes']) + " " + str(word_count[w[0]]['no']) + " " + str(
            #     word_count[w[0]]['total'])
            f.write(w[0] + "," + str(word_count[w[0]]['yes']) + "," + str(word_count[w[0]]['no']) + "," + str(
                word_count[w[0]]['total']))
            f.write('\n')

        # print "---------------------------------------------------------"
        for w in sorted_perc[-num_of_top_words_as_feature:]:
            # print w[0] + " " + str(word_count[w[0]]['yes']) + " " + str(word_count[w[0]]['no']) + " " + str(
            #     word_count[w[0]]['total'])
            f.write(w[0] + "," + str(word_count[w[0]]['yes']) + "," + str(word_count[w[0]]['no']) + "," + str(
                word_count[w[0]]['total']))
            f.write('\n')

        print(
        'Writing csv file: ' + 'data/' + category + '/' + dataFileConvention + '_20feature_word_all_data' + '.csv')

    with open('data/' + category + '/' + dataFileConvention + '_20feature_word_all_data' + '.csv', 'w') as f:
        for w in sorted_perc[:num_of_top_words_as_feature]:
            # word name
            f.write(w[0] + ",")
        f.write('\n')

        for w in sorted_perc[:num_of_top_words_as_feature]:
            # word perc
            f.write(str(w[1]) + ",")
        f.write('\n')

        for w in sorted_perc[-num_of_top_words_as_feature:]:
            # word name
            f.write(w[0] + ",")
        f.write('\n')

        for w in sorted_perc[-num_of_top_words_as_feature:]:
            # word perc
            f.write(str(w[1]) + ",")
        f.write('\n')

        print(
        'Writing csv file: ' + 'data/' + category + '/' + dataFileConvention + '_20feature_word_all_data' + '.csv')

    with open('data/' + category + '/' + dataFileConvention + '_word_table' + '.csv', 'w') as f:
        for w in word_count:
            f.write(w + "," + str(word_count[w]['yes']) + "," + str(word_count[w]['no']) + "," + str(
                word_count[w]['total']) + "," + str(percentages[w]))
            f.write('\n')

        print('Writing csv file: ' + 'data/' + category + '/' + dataFileConvention + '_word_table' + '.csv')


def write_dataset(category, sorted_perc, data, dataFileConvention):
    num_of_top_words_as_feature = get_num_of_top_words_as_feature(dataFileConvention)

    with open('data/' + category + '/' + dataFileConvention + '_dataset.csv', 'w') as f:
        f.write(','.join([x[0] for x in sorted_perc[:num_of_top_words_as_feature]]))
        # print ','.join([x[0] for x in sorted_perc[:num_of_top_words_as_feature]])

        f.write(',')

        f.write(','.join([x[0] for x in sorted_perc[-num_of_top_words_as_feature:]]))
        # print ','.join([x[0] for x in sorted_perc[-num_of_top_words_as_feature:]])

        f.write(',sub_size,time_limit')
        f.write(',class')
        f.write('\n')

        for t in data:
            f.write(','.join([str(x) for x in t]))
            f.write('\n')

        print('Writing dataset file: ' + 'data/' + category + '/' + dataFileConvention + '_dataset.csv')


# data can be train set or test set
def prepare_dataset(sorted_perc, data, category, platform, dataFileConvention):
    count = 0
    prepared_data = []
    num_of_top_words_as_feature = get_num_of_top_words_as_feature(dataFileConvention)

    for p in data:
        prepared_data.append([])
        features = []

        for presentWord in sorted_perc[:num_of_top_words_as_feature]:
            presentWord = presentWord[0]  # it contains tuple of word and percentage, hence [0] element for word

            if presentWord in p.modified_description.split():
                features.append(1)
            else:
                features.append(0)

        for notPresentWord in sorted_perc[-num_of_top_words_as_feature:]:
            notPresentWord = notPresentWord[0]

            if notPresentWord in p.modified_description.split():
                features.append(1)
            else:
                features.append(0)

        features.append(p.sub_size.split()[0])
        features.append(p.time_limit[:1])

        if category in p.category:
            features.append(1)
        else:
            features.append(0)

        prepared_data[count] = features
        count += 1

    print('Required dataset prepared')
    return prepared_data


def generate(useIntegrated, category, platform, test_size=defaultTestSize):
    probs = get_all_probs_without_category_NA(useIntegrated, platform)

    # with open('test_size.pickle') as f:
    #     test_size = pickle.load(f)

    train_set, test_set = train_test_split(probs, test_size)
    word_cnt_by_cateogry = get_wordcount_by_category(train_set, category)

    percentages, word_cnt_stats = get_word_perc(word_cnt_by_cateogry)

    sorted_perc = sorted(percentages.items(), key=operator.itemgetter(1))
    sorted_perc.reverse()  # desc order

    total_data = []
    prepared_train_data = prepare_dataset(sorted_perc, train_set, category, platform)
    prepared_test_data = prepare_dataset(sorted_perc, test_set, category, platform)

    [total_data.append(t) for t in prepared_train_data]
    [total_data.append(t) for t in prepared_test_data]

    make_csv_files(category, sorted_perc, word_cnt_stats, percentages, platform)
    write_dataset(category, sorted_perc, total_data, platform)


def generateLazyLoad(useIntegrated, category, platform, uniqueFileConvention, dataFileConvention,
                     shouldShuffle=True, test_size=defaultTestSize):
    dataFileConvention = dataFileConvention + '_' + category + '_' + str(test_size)
    if os.path.isfile('data/' + category + '/' + dataFileConvention + '_dataset.csv'):
        print(dataFileConvention + '_dataset.csv' + ' already generated')
        return
    print(dataFileConvention + '_dataset.csv' + ' not found')
    print(dataFileConvention + '_dataset.csv' + ' generating')
    probs = []
    if len(generateLazyLoad.probs) == 0:
        generateLazyLoad.probs = get_all_probs_without_category_NA(useIntegrated, platform)
    probs = generateLazyLoad.probs
    # with open('test_size.pickle') as f:
    #     test_size = pickle.load(f)

    train_set, test_set = train_test_split(probs, test_size, shouldShuffle)
    word_cnt_by_cateogry = get_wordcount_by_category(train_set, category)

    percentages, word_cnt_stats = get_word_perc(word_cnt_by_cateogry)

    sorted_perc = sorted(percentages.items(), key=operator.itemgetter(1))
    sorted_perc.reverse()  # desc order

    total_data = []
    prepared_train_data = prepare_dataset(sorted_perc, train_set, category, platform, dataFileConvention)
    prepared_test_data = prepare_dataset(sorted_perc, test_set, category, platform, dataFileConvention)

    [total_data.append(t) for t in prepared_train_data]
    [total_data.append(t) for t in prepared_test_data]

    make_csv_files(category, sorted_perc, word_cnt_stats, percentages, dataFileConvention)
    write_dataset(category, sorted_perc, total_data, dataFileConvention)


def generateLazyLoadForModel2(useIntegrated, category, platform, uniqueFileConvention, dataFileConvention,
                              test_size=defaultTestSize):
    dataFileConvention = dataFileConvention + '_' + category + '_' + str(test_size)
    if os.path.isfile('data/' + category + '/' + dataFileConvention + '_dataset.csv'):
        print(dataFileConvention + '_dataset.csv' + ' already generated')
        return
    print(dataFileConvention + '_dataset.csv' + ' not found')
    print(dataFileConvention + '_dataset.csv' + ' generating')
    probs = []
    if len(generateLazyLoad.probs) == 0:
        generateLazyLoadForModel2.probs = get_all_probs_without_category_NA(useIntegrated, platform)
    probs = generateLazyLoadForModel2.probs

    # with open('test_size.pickle') as f:
    #     test_size = pickle.load(f)
    random.shuffle(probs)
    train_set = tuple([prob.modified_description for prob in probs])

    prob_class = []

    for prob in probs:
        prob_class.append(1.0 if category in prob.category else 0.0)

    print 'Test Size: ' + str((test_size))
    print 'Total: ' + str((len(probs)))
    print 'Train Set Length: ' + str(len(train_set))

    timeStart = time.time()
    count_vectorizer = CountVectorizer(stop_words = 'english')
    count_vectorizer.fit_transform(train_set)
    with open('data/' + dataFileConvention + '_countVectorizer.pickle', 'w+b') as f:
        print("Dumping count vectorizer: " + 'data/' + dataFileConvention + '_countVectorizer.pickle')
        pickle.dump(count_vectorizer, f)

    freq_term_matrix = count_vectorizer.transform(train_set)
    # print('Features:')
    # print(str(count_vectorizer.vocabulary_))
    # print('===================================================')

    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(freq_term_matrix)



    with open('data/' + dataFileConvention + '_TfidfTransformer.pickle', 'w+b') as f:
        print('Dumping tfidf transformer: ' + 'data/' + dataFileConvention + '_TfidfTransformer.pickle')
        pickle.dump(tfidf, f)

    np.set_printoptions(threshold = 'nan')
    tf_idf_matrix = tfidf.transform(freq_term_matrix)
    # print(str(tf_idf_matrix))
    numpyAr = tf_idf_matrix.toarray()
    
    # print(str(numpyAr))
    # print(str(tf_idf_matrix.todense()))
    print 'Tfidf Feature Size: ' + str(len(numpyAr[0]) + 1)

    #Applying SVD to reduce features
    svd = TruncatedSVD(int(0.1*len(numpyAr[0] + 1)))
    lsa = make_pipeline(svd, Normalizer(copy = False))
    reduced_lsa_features = lsa.fit_transform(tf_idf_matrix)
    numpyAr = reduced_lsa_features
    print 'Reduced Feature Size: ' + str(len(numpyAr[0]) + 1)
    #print(str(reduced_lsa_features))
    # print(str(numpyAr))
    print('Time taken for generating data: '+ str(time.time() - timeStart))
    if not os.path.exists('data/' + category):
        os.makedirs('data/' + category)
    with open('data/' + category + '/' + dataFileConvention + '_dataset.csv', 'w') as f:
        print('Writing' + 'data/' + category + '/' + dataFileConvention + '_dataset.csv')
        writer = csv.writer(f)
        i = 0
        for row in numpyAr:
            writer.writerow(list(row) + [prob_class[i]])
            i += 1


generateLazyLoad.probs = []
generateLazyLoadForModel2.probs = []

if __name__ == '__main__':
    pass
