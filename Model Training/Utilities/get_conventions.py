from constants import ClassifierType, PlatformType


# number of top words only applicable currently to model number
def get_problem_model_file_convention(platform, model_number, category_or_problemWise,  number_of_top_words,
                                      category, test_size, classifier):
    file_convention = PlatformType.platformString[platform] + '_' +\
                      'modelNumber:' + model_number + '_' +\
                      'catOrProb:' + category_or_problemWise + '_' + \
                      'topwords:' + number_of_top_words + '_' +\
                      'cat:' + category + '_' +\
                      'testsize:' + test_size + '_' +\
                      'class:' + ClassifierType.classifierTypeString[classifier]

    return file_convention


def get_problem_dataset_file_convention(platform, model_number, number_of_top_words, category, test_size):
    file_convention = PlatformType.platformString[platform] + '_' + \
                      'modelNumber:' + model_number + '_' + \
                      'topwords:' + number_of_top_words + '_' + \
                      'cat:' + category + '_' + \
                      'testsize:' + test_size

    return file_convention


def get_problem_metrics_file_convention(platform, model_number, number, category_or_problemWise, category,
                                      test_size, classifier, number_of_top_words):
    file_convention = PlatformType.platformString[platform] + '_' + \
                      'modelNumber:' + model_number + '_' + \
                      'catOrProb:' + category_or_problemWise + '_' + \
                      'topwords:' + number_of_top_words + '_' + \
                      'cat:' + category + '_' + \
                      'testsize:' + test_size + '_' + \
                      'class:' + ClassifierType.classifierTypeString[classifier]

    return file_convention
