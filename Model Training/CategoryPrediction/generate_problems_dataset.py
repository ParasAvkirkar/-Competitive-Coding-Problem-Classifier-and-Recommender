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

sys.path.append('../Utilities/')
from constants import categories, performance_metric_keys, ClassifierType, problemOrCategoryKeys, \
    PlatformType, defaultTestSize
from get_conventions import get_problem_model_file_convention, get_problem_dataset_file_convention, get_problem_metrics_file_convention

def get_num_of_top_words_as_feature(dataFileConvention, number_of_top_words_as_feature):
    print('Getting number of top words')
    try:
        with open('data/' + dataFileConvention + '_num_of_top_words_as_feature.pickle') as f:
            num_of_top_words_as_feature = pickle.load(f)
            # print "\n\n\n\n num_of_top_words_as_feature = " + str(num_of_top_words_as_feature) + "\n\n\n\n"
    except:
        with open('data/' + dataFileConvention + '_num_of_top_words_as_feature.pickle', 'w') as f:
            # num_of_top_words_as_feature = 10
            pickle.dump(num_of_top_words_as_feature, f)
            # print "\n\n\n\n exception in num of top words as feature, using default size of 10\n\n\n\n"

    return num_of_top_words_as_feature


def make_csv_files(category, sorted_perc, word_count, percentages, dataFileConvention, number_of_top_words):
    # num_of_top_words_as_feature = get_num_of_top_words_as_feature(dataFileConvention, number_of_top_words)
    num_of_top_words_as_feature = number_of_top_words
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


def write_dataset(category, sorted_perc, data, dataFileConvention, number_of_top_words):
    # num_of_top_words_as_feature = get_num_of_top_words_as_feature(dataFileConvention, number_of_top_words)
    num_of_top_words_as_feature = number_of_top_words
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
def prepare_dataset(sorted_perc, data, category, platform, dataFileConvention, number_of_top_words):
    count = 0
    prepared_data = []
    # num_of_top_words_as_feature = get_num_of_top_words_as_feature(dataFileConvention, number_of_top_words)
    num_of_top_words_as_feature = number_of_top_words
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
                     shouldShuffle=True, test_size=defaultTestSize, number_of_top_words = 10):

    # dataFileConvention = get_problem_dataset_file_convention(platform = platform, model_number = 1,
    #                                                          number_of_top_words = number_of_top_words,
    #                                                          category = category, test_size = test_size)

    if os.path.isfile('data/' + category + '/' + dataFileConvention + '_dataset.csv'):
        print(dataFileConvention + '_dataset.csv' + ' already generated only shuffling right now')
        with open('data/' + category + '/' + dataFileConvention + '_dataset.csv', 'r') as f:
            l = list(csv.reader(f))
            firstHeadersRow = l[0]
            l = l[1:]
        if shouldShuffle:
            random.shuffle(l)
        with open('data/' + category + '/' + dataFileConvention + '_dataset.csv', 'w') as f:
            csv.writer(f).writerows([firstHeadersRow] + l)
        return
    print(dataFileConvention + '_dataset.csv' + ' not found')
    print(dataFileConvention + '_dataset.csv' + ' generating')
    probs = []
    if len(generateLazyLoad.probs) == 0:
        generateLazyLoad.probs = get_all_probs_without_category_NA(useIntegrated, platform)
        random.shuffle(generateLazyLoad.probs)
    probs = generateLazyLoad.probs
    # with open('test_size.pickle') as f:
    #     test_size = pickle.load(f)

    train_set, test_set = train_test_split(probs, test_size, shouldShuffle)
    word_cnt_by_cateogry = get_wordcount_by_category(train_set, category)

    percentages, word_cnt_stats = get_word_perc(word_cnt_by_cateogry)

    sorted_perc = sorted(percentages.items(), key=operator.itemgetter(1))
    sorted_perc.reverse()  # desc order

    total_data = []
    prepared_train_data = prepare_dataset(sorted_perc, train_set, category, platform, dataFileConvention,
                                          number_of_top_words = number_of_top_words)
    prepared_test_data = prepare_dataset(sorted_perc, test_set, category, platform, dataFileConvention,
                                         number_of_top_words = number_of_top_words)

    [total_data.append(t) for t in prepared_train_data]
    [total_data.append(t) for t in prepared_test_data]

    make_csv_files(category, sorted_perc, word_cnt_stats, percentages, dataFileConvention,
                   number_of_top_words = number_of_top_words)
    write_dataset(category, sorted_perc, total_data, dataFileConvention,
                  number_of_top_words = number_of_top_words)


def generateLazyLoadForModel2(useIntegrated, category, platform, uniqueFileConvention, dataFileConvention,
                              test_size=defaultTestSize):
    if os.path.isfile('data/' + category + '/' + dataFileConvention + '_dataset.csv'):
        print(dataFileConvention + '_dataset.csv' + ' already generated only shuffling right now')
        with open('data/' + category + '/' + dataFileConvention + '_dataset.csv', 'r') as f:
            l = list(csv.reader(f))
            firstHeadersRow = l[0]
            l = l[1:]
        random.shuffle(l)
        with open('data/' + category + '/' + dataFileConvention + '_dataset.csv', 'w') as f:
            csv.writer(f).writerows([firstHeadersRow] + l)
        return
    print(dataFileConvention + '_dataset.csv' + ' not found')
    print(dataFileConvention + '_dataset.csv' + ' generating')
    probs = []
    if len(generateLazyLoad.probs) == 0:
        generateLazyLoadForModel2.probs = get_all_probs_without_category_NA(useIntegrated, platform)
    probs = generateLazyLoadForModel2.probs

    random.shuffle(probs)
    train_set = tuple([prob.modified_description for prob in probs])

    prob_class = []
    for prob in probs:
        prob_class.append(1.0 if category in prob.category else 0.0)

    print 'Test Size: ' + str((test_size))
    print 'Total: ' + str((len(probs)))
    print 'Train Set Length: ' + str(len(train_set))

    timeStart = time.time()

    if os.path.isfile(PlatformType.platformString[platform] + '_tfidfMatrix_'+ '.pickle'):
        print('Loading tfidf matrix from pickle')
        with open(PlatformType.platformString[platform] + '_tfidfMatrix_'+ '.pickle', 'rb') as f:
            tf_idf_matrix = pickle.load(f)
    else:
        print('Building tfidf matrix and dumping in pickle')
        count_vectorizer = CountVectorizer(stop_words = 'english')
        count_vectorizer.fit_transform(train_set)
        freq_term_matrix = count_vectorizer.transform(train_set)
        tfidf = TfidfTransformer(norm="l2")
        tfidf.fit(freq_term_matrix)
        tf_idf_matrix = tfidf.transform(freq_term_matrix)
        with open(PlatformType.platformString[platform] + '_tfidfMatrix_' + '.pickle', 'wb') as f:
            pickle.dump(tf_idf_matrix, f)

    # print(str(tf_idf_matrix))
    numpyAr = tf_idf_matrix.toarray()
    np.set_printoptions(threshold = 'nan')
    print 'Tfidf Feature Size: ' + str(len(numpyAr[0]) + 1)
    list_of_features_needed = []
    keepPercentage = 0.05

    if os.path.isfile(PlatformType.platformString[platform]+'_list_of_features_aftertfidf_'+str(keepPercentage)+'.pickle'):
        print('List of features after tfidf already found, reading from there')
        with open(PlatformType.platformString[platform] + '_list_of_features_aftertfidf_' + str(keepPercentage) + '.pickle', 'rb') as f:
            list_of_features_needed = pickle.load(f)
    else:
        print('Making List of features after tfidf and dumping as pickle')
        for cat in categories:
            list_of_features_needed = list_of_features_needed + get_categorywise_features(numpyAr, cat, probs, keepPercentage)

        list_of_features_needed = list(set(list_of_features_needed))
        list_of_features_needed.sort()
        with open(PlatformType.platformString[platform]+'_list_of_features_aftertfidf_'+str(keepPercentage)+'.pickle', 'wb') as f:
            pickle.dump(list_of_features_needed, f)

    # print(str(list_of_features_needed))
    numpyArrayList = []
    for i in range(len(numpyAr)):
        newRowList = []
        for j in list_of_features_needed:
            newRowList.append(numpyAr[i][j])
        numpyArrayList = numpyArrayList + [np.array(newRowList)]
    numpyAr = np.array(numpyArrayList)
    print(numpyAr.shape)

    #Applying SVD to reduce features
    # svd = TruncatedSVD(int(0.1*len(numpyAr[0] + 1)))
    # lsa = make_pipeline(svd, Normalizer(copy = False))
    # reduced_lsa_features = lsa.fit_transform(tf_idf_matrix)
    # numpyAr = reduced_lsa_features
    #
    print 'Reduced Feature Size: ' + str(len(numpyAr[0]) + 1)
    print('Time taken for generating data: '+ str(time.time() - timeStart))
    if not os.path.exists('data/' + category):
        os.makedirs('data/' + category)
    print('Currently on cat: '+str(category))
    with open('data/' + category + '/' + dataFileConvention + '_dataset.csv', 'w') as f:
        print('Writing ' + 'data/' + category + '/' + dataFileConvention + '_dataset.csv')
        writer = csv.writer(f)
        i = 0
        for row in numpyAr:
            writer.writerow(list(row) + [prob_class[i]])
            i += 1

generateLazyLoad.probs = []
generateLazyLoadForModel2.probs = []

def get_categorywise_features(numpyAr, category, probs, keepPercentage):
    temp_numpy_arr = np.array([0.0 for i in range(len(numpyAr[0]))])
    index = 0
    for prob in probs:
        if category in prob.category:
            temp_numpy_arr = temp_numpy_arr + numpyAr[index]
        index += 1
    featureDict = {}
    index = 0
    for value in temp_numpy_arr:
        featureDict[index] = value
        index += 1
    listOfSortedtuples = sorted(featureDict.items(), key = operator.itemgetter(1), reverse = True)
    featureIndices = []
    index = 0
    for feature in listOfSortedtuples:
        if index > keepPercentage*len(listOfSortedtuples):
            break
        featureIndices.append(feature[0])
        index += 1

    return featureIndices

if __name__ == '__main__':
    pass
