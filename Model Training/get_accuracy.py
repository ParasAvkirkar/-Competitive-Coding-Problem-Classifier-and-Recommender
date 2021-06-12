from gensim import models
import pickle
import os
import operator
import sys
import copy
import csv
import numpy as np

from sqlalchemy.sql.functions import user

from sorting import sort_by_date_difficulty, sort_by_date
from generate_users_dataset import generateLazyLoad, generateLazyLoadAll, get_probCodeToObjects
from get_probs import get_difficulty, get_category, get_all_probs_without_category_NA
from user_level_limits import get_categorywise_difficulty_limits, get_difficulty_limits_without_category

from recommend_popular import get_popular

sys.path.append('Utilities/')

from constants import PlatformType, categories, stddifficultyLevels, codechefDifficultyLevels

tp = 0
tn = 0
fp = 0
fn = 0


def get_word2vec_recommendation(uniqueFileConvention, submissionsDict, prev_sub, no_recomm):
    model = models.Word2Vec.load(uniqueFileConvention)
    sorted_submissions = sort_by_date(submissionsDict)

    submission_sentence = []
    [submission_sentence.append(row[0]) for row in sorted_submissions[-prev_sub:]]

    # Word2Vec function call to give recommendations
    recommendation = model.most_similar(positive=submission_sentence, topn=no_recomm)

    return recommendation


def recommender(uniqueFileConvention, userObjects, username, prev_sub, no_recomm, no_test):
    global tp, tn, fp, fn

    submissionsDict = userObjects.problemMappings

    evalsubmissions = []
    for x in sort_by_date(submissionsDict)[-no_test:]:
        evalsubmissions.append(x[0])

    for prob_code in evalsubmissions:
        del submissionsDict[prob_code]

    final_recommendation = []

    # prev_sub = 5
    # no_recomm = 50
    if len(submissionsDict) >= prev_sub:

        recommendation = get_word2vec_recommendation(uniqueFileConvention, submissionsDict, prev_sub, no_recomm)
        for row in recommendation:
            final_recommendation.append(row[0])

        for prob_code in final_recommendation:
            if prob_code in evalsubmissions:
                tp += 1
            else:
                fp += 1

        for prob_code in evalsubmissions:
            if prob_code not in final_recommendation:
                fn += 1

    # print final_recommendation
    # print evalsubmissions



def get_recommendations(username, prev_sub, no_recomm, no_test):
    uniqueFileConvention = 'users_codechef'
    # uniqueFileConvention = 'users_codechef_all_probs'
    platform = PlatformType.Codechef

    userObjects = generateLazyLoad(uniqueFileConvention, platform, username)
    recommender(uniqueFileConvention, userObjects, username, prev_sub, no_recomm, no_test)


if __name__ == '__main__':

    user_list = []
    uniqueFileConvention = 'users_codechef'
    # uniqueFileConvention = 'users_codechef_all_probs'

    with open("users_ids.txt", 'rb') as f:
        user_list = f.readlines()

    with open('accuracy_val.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['prev_sub', 'no_recomm', 'no_test', 'tp', 'tn', 'fp', 'fn', 'precision', 'recall', 'f1_score'])

        prev_sub = 5
        no_recomm = 10
        for no_test in range(20,21,10):
            for prev_sub in range(5,6,5):
                for no_recomm in range(10, 11, 10):

                    print str(no_test)+ " " + str(prev_sub) + " " + str(no_recomm)
                    tp = tn = fp = fn = 0
                    for username in user_list:
                        if os.path.isfile('users/' + uniqueFileConvention + '_' + username.strip() + '.pickle'):
                            get_recommendations(username.strip(), prev_sub, no_recomm, no_test)

                    print str(tp) + " " + str(fn)
                    print str(fp) + " " + str(tn)

                    tp = tp * 1.0
                    precision = tp/(tp + fp)
                    recall = tp/(tp + fn)
                    f1_score = 2 * precision * recall / (precision + recall)
                    Specificity = tn / tn + fp
                    False_Positive_Rate = fp / fp + tn
                    True_Negative_Rate = tn / tn + fp
                    False_Negative_Rate = fn / fn + tp
                    print "Precision - " + str(precision)
                    print "Recall - " + str(recall)
                    print "F1score - " + str(f1_score)

                    dat = [prev_sub, no_recomm, no_test, tp, tn, fp, fn, precision, recall, f1_score,Specificity,False_Positive_Rate,True_Negative_Rate,False_Negative_Rate]
                    writer.writerow(dat)
